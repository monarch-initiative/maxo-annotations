import logging
import random
import typing
from collections import defaultdict
from csv import DictReader
from pathlib import Path

import click
import hpotk

from maxoa.terms import apply_term_updates, log_replacement_summary

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXISTING_ANNOT_FILE = REPO_ROOT / "data" / "poet" / "annotations.tsv"
AUTOMAXO_ANNOT_FILE = REPO_ROOT / "data" / "automaxo" / "automaxo-annotations.tsv"

ANNOT_COLUMNS = [
    "disease_id", "disease_name", "source_id", "maxo_id", "maxo_name",
    "hpo_id", "relation", "evidence", "extension_id", "extension_name",
    "comment", "other", "author", "last_updated", "created",
]


class AutomaxoEntry:
    """One annotation row from an automaxo curation TSV."""

    def __init__(self, row: dict) -> None:
        self.disease_id = row["disease_id"]
        self.disease_name = row["disease_name"]
        self.source_id = row["source_id"]
        self.maxo_id = row["maxo_id"]
        self.maxo_name = row["maxo_name"]
        self.hpo_id = row["hpo_id"]
        self.relation = row["relation"]
        self.evidence = row["evidence"]
        self.extension_id = row["extension_id"]
        self.extension_name = row["extension_name"]
        self.comment = row["comment"]
        self.other = row["other"]
        self.last_updated = row["last_updated"]
        self.created = row["created"]
        self._raw_author = row["author"]

    def __hash__(self) -> int:
        return hash((self.source_id, self.maxo_id, self.hpo_id))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AutomaxoEntry):
            return NotImplemented
        return (
            self.source_id == other.source_id
            and self.maxo_id == other.maxo_id
            and self.hpo_id == other.hpo_id
        )

    @property
    def author(self) -> str:
        orcid = self._raw_author.strip()
        if orcid and not orcid.startswith("ORCID:"):
            return f"ORCID:{orcid}"
        return orcid

    @staticmethod
    def parse_dir(directory: Path) -> typing.Dict[str, typing.List["AutomaxoEntry"]]:
        tsv_files = sorted(directory.glob("*.tsv"))
        if not tsv_files:
            raise click.ClickException(f"No *.tsv files found in {directory}")
        logger.info("Found %d automaxo files in %s", len(tsv_files), directory)

        seen: set[AutomaxoEntry] = set()
        disease_to_entries: dict[str, list[AutomaxoEntry]] = defaultdict(list)
        duplicates = 0

        for tsv_file in tsv_files:
            with open(tsv_file) as f:
                header = [col.strip() for col in f.readline().rstrip("\n").split("\t")]
                reader = DictReader(f, fieldnames=header, delimiter="\t")
                for row in reader:
                    entry = AutomaxoEntry(apply_term_updates(row))
                    if entry in seen:
                        logger.warning("Duplicate within new set: %s", row)
                        duplicates += 1
                    else:
                        seen.add(entry)
                        disease_to_entries[entry.disease_id].append(entry)

        if duplicates:
            logger.warning("Skipped %d duplicate entries within new set", duplicates)

        total = sum(len(v) for v in disease_to_entries.values())
        logger.info("Loaded %d entries across %d diseases", total, len(disease_to_entries))
        return disease_to_entries


def _get_existing_keys(path: Path) -> set[tuple]:
    keys = set()
    with open(path, newline="") as f:
        header = [c.strip() for c in f.readline().rstrip("\r\n").split("\t")]
        for row in DictReader(f, fieldnames=header, delimiter="\t"):
            keys.add((
                row["disease_id"].strip(),
                row["source_id"].strip(),
                row["maxo_id"].strip(),
                row["hpo_id"].strip(),
            ))
    return keys


def _get_disease_summary_row(
    annot_list: typing.List[AutomaxoEntry], hpo: hpotk.Ontology
) -> typing.List[str]:
    unique_maxo = {e.maxo_id for e in annot_list}
    unique_hpo = {e.hpo_id for e in annot_list}
    example = random.choice(annot_list)
    disease_str = f"{example.disease_name} ({example.disease_id})"
    maxo_str = f"{example.maxo_name} ({example.maxo_id})"
    hpo_id = example.hpo_id
    if hpo_id not in hpo:
        raise ValueError(f"HPO term not found: {hpo_id}")
    hpo_str = disease_str if hpo_id == "HP:0000118" else f"{hpo.get_term(hpo_id).name} ({hpo_id})"
    return [disease_str, str(len(annot_list)), str(len(unique_maxo)), str(len(unique_hpo)), maxo_str, example.relation, hpo_str]


def _write_annotations(disease_to_entries: typing.Dict[str, typing.List[AutomaxoEntry]], path: Path) -> int:
    written = 0
    with open(path, "w") as f:
        f.write("\t".join(ANNOT_COLUMNS) + "\n")
        for entries in disease_to_entries.values():
            for e in entries:
                row = [
                    e.disease_id, e.disease_name, e.source_id, e.maxo_id, e.maxo_name,
                    e.hpo_id, e.relation.lower(), e.evidence, e.extension_id,
                    e.extension_name, e.comment, e.other, e.author, e.last_updated, e.created,
                ]
                f.write("\t".join(row) + "\n")
                written += 1
    return written


@click.group()
def generate() -> None:
    """Generate annotation files from curation sources."""


@generate.command()
@click.option("-a", "--automaxo-dir", default=str(REPO_ROOT / "data" / "automaxo"), show_default=True, type=click.Path(exists=True, file_okay=False, path_type=Path), help="Directory containing automaxo *.tsv files")
@click.option("-o", "--out", default=str(REPO_ROOT / "data" / "reports" / "automaxo_report.tsv"), type=click.Path(path_type=Path), show_default=True, help="Summary output file")
@click.option("--dry-run", is_flag=True, help="Check overlaps and write summary without writing annotations file")
def automaxo(automaxo_dir: Path, out: Path, dry_run: bool) -> None:
    """Generate automaxo-annotations.tsv from automaxo curation files."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    disease_to_entries = AutomaxoEntry.parse_dir(automaxo_dir)

    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()

    summary_rows = sorted(
        [_get_disease_summary_row(v, hpo) for v in disease_to_entries.values()],
        key=lambda x: x[0].lower(),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as fh:
        fh.write("\t".join(["Mondo", "annotations", "MAxO (n)", "HPO (n)", "example MAxO", "example relation", "Example HPO"]) + "\n")
        for row in summary_rows:
            fh.write("\t".join(row) + "\n")
    click.echo(f"Summary written to {out}")

    unique_maxo: set[str] = set()
    unique_hpo: set[str] = set()
    total = 0
    for entries in disease_to_entries.values():
        for e in entries:
            unique_maxo.add(e.maxo_id)
            unique_hpo.add(e.hpo_id)
            total += 1
    click.echo(f"Total annotations: {total}  |  Unique HPO: {len(unique_hpo)}  |  Unique MAxO: {len(unique_maxo)}")

    existing_keys = _get_existing_keys(EXISTING_ANNOT_FILE)
    overlapping = [e for entries in disease_to_entries.values() for e in entries
                   if (e.disease_id, e.source_id, e.maxo_id, e.hpo_id) in existing_keys]

    if overlapping:
        click.echo(f"Warning: {len(overlapping)} entries already in {EXISTING_ANNOT_FILE.name} — will still be written to {AUTOMAXO_ANNOT_FILE.name}", err=True)
        for e in overlapping:
            click.echo(f"  {e.disease_id}  {e.source_id}  {e.maxo_id}  {e.hpo_id}", err=True)
    else:
        click.echo("No overlaps with existing annotations")

    log_replacement_summary()

    if dry_run:
        click.echo(f"Dry run — skipping write of {AUTOMAXO_ANNOT_FILE}")
        return

    written = _write_annotations(disease_to_entries, AUTOMAXO_ANNOT_FILE)
    click.echo(f"Wrote {written} annotations to {AUTOMAXO_ANNOT_FILE}")
