"""
Merge automaxo curation annotations into annotations/maxo-annotations.tsv.

Reads all *.tsv files from the automaxo directory, checks for duplicates
within the new set and against the existing annotations, then appends
non-overlapping entries and writes a per-disease summary TSV.
"""

import argparse
import logging
import random
import sys
import typing
from collections import defaultdict
from csv import DictReader
from pathlib import Path

import hpotk

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
EXISTING_ANNOT_FILE = REPO_ROOT / "annotations" / "maxo-annotations.tsv"
AUTOMAXO_ANNOT_FILE = REPO_ROOT / "annotations" / "automaxo-annotations.tsv"
EXISTING_HEADER_LINES = 1  # POET export: one column header, no comment lines

# Column names match POET export format exactly so files can be concatenated directly.
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
    def parse_automaxo_dir(
        directory: Path,
    ) -> typing.Dict[str, typing.List["AutomaxoEntry"]]:
        """Parse all *.tsv files in directory, return dict of disease_id → entries."""
        tsv_files = sorted(directory.glob("*.tsv"))
        if not tsv_files:
            logger.error("No *.tsv files found in %s", directory)
            sys.exit(1)
        logger.info("Found %d automaxo files in %s", len(tsv_files), directory)

        seen: set[AutomaxoEntry] = set()
        disease_to_entries: dict[str, list[AutomaxoEntry]] = defaultdict(list)
        duplicates = 0

        for tsv_file in tsv_files:
            with open(tsv_file) as f:
                header = [col.strip() for col in f.readline().rstrip("\n").split("\t")]
                reader = DictReader(f, fieldnames=header, delimiter="\t")
                for row in reader:
                    entry = AutomaxoEntry(row)
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


class ExistingAnnot:
    """One annotation row from the existing maxo-annotations.tsv (POET export format)."""

    def __init__(self, row: dict) -> None:
        self._disease_id = row["disease_id"].strip()
        self._source_id = row["source_id"].strip()
        self._maxo_id = row["maxo_id"].strip()
        self._hpo_id = row["hpo_id"].strip()

    def overlaps(self, entry: AutomaxoEntry) -> bool:
        return (
            entry.maxo_id == self._maxo_id
            and entry.disease_id == self._disease_id
            and entry.hpo_id == self._hpo_id
            and entry.source_id == self._source_id
        )

    @staticmethod
    def ingest(path: Path = EXISTING_ANNOT_FILE) -> typing.List["ExistingAnnot"]:
        entries: list[ExistingAnnot] = []
        with open(path, newline="") as f:
            header = [col.strip() for col in f.readline().rstrip("\r\n").split("\t")]
            reader = DictReader(f, fieldnames=header, delimiter="\t")
            for row in reader:
                entries.append(ExistingAnnot(row))
        logger.info("Loaded %d existing annotations", len(entries))
        return entries


def get_disease_summary_row(
    annot_list: typing.List[AutomaxoEntry], hpo: hpotk.Ontology
) -> typing.List[str]:
    n_entries = len(annot_list)
    unique_maxo = {e.maxo_id for e in annot_list}
    unique_hpo = {e.hpo_id for e in annot_list}
    example = random.choice(annot_list)

    disease_str = f"{example.disease_name} ({example.disease_id})"
    maxo_str = f"{example.maxo_name} ({example.maxo_id})"

    hpo_id = example.hpo_id
    if hpo_id not in hpo:
        raise ValueError(f"HPO term not found: {hpo_id}")
    if hpo_id == "HP:0000118":
        hpo_str = disease_str
    else:
        term = hpo.get_term(hpo_id)
        hpo_str = f"{term.name} ({hpo_id})"

    return [
        disease_str,
        str(n_entries),
        str(len(unique_maxo)),
        str(len(unique_hpo)),
        maxo_str,
        example.relation,
        hpo_str,
    ]


def print_total_stats(disease_to_entries: typing.Dict[str, typing.List[AutomaxoEntry]]) -> None:
    unique_maxo: set[str] = set()
    unique_hpo: set[str] = set()
    total = 0
    for entries in disease_to_entries.values():
        for e in entries:
            unique_maxo.add(e.maxo_id)
            unique_hpo.add(e.hpo_id)
            total += 1
    logger.info("Total new annotations: %d", total)
    logger.info("Unique HPO terms: %d", len(unique_hpo))
    logger.info("Unique MAxO terms: %d", len(unique_maxo))


def has_overlap(entry: AutomaxoEntry, existing: typing.List[ExistingAnnot]) -> bool:
    return any(ea.overlaps(entry) for ea in existing)


def write_automaxo_annotations(
    disease_to_entries: typing.Dict[str, typing.List[AutomaxoEntry]],
    path: Path = AUTOMAXO_ANNOT_FILE,
) -> int:
    """Write all automaxo entries to a standalone annotations file. Returns count written."""
    written = 0
    with open(path, "w") as f:
        f.write("\t".join(ANNOT_COLUMNS) + "\n")
        for entries in disease_to_entries.values():
            for e in entries:
                row = [
                    e.disease_id,
                    e.disease_name,
                    e.source_id,
                    e.maxo_id,
                    e.maxo_name,
                    e.hpo_id,
                    e.relation.upper(),
                    e.evidence,
                    e.extension_id,
                    e.extension_name,
                    e.comment,
                    e.other,
                    e.author,
                    e.last_updated,
                    e.created,
                ]
                f.write("\t".join(row) + "\n")
                written += 1
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Merge automaxo annotations into maxo-annotations.tsv"
    )
    ap.add_argument(
        "-a",
        "--automaxo-dir",
        required=True,
        type=Path,
        help="Path to directory containing automaxo *.tsv files",
    )
    ap.add_argument(
        "-o",
        "--out",
        default="am_summary.tsv",
        type=Path,
        help="Output summary file (default: am_summary.tsv)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Check for overlaps and write summary but do not append to annotations file",
    )
    args = ap.parse_args()

    disease_to_entries = AutomaxoEntry.parse_automaxo_dir(args.automaxo_dir)

    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()

    summary_rows = []
    for annot_list in disease_to_entries.values():
        summary_rows.append(get_disease_summary_row(annot_list=annot_list, hpo=hpo))

    summary_rows.sort(key=lambda x: x[0].lower())

    with open(args.out, "w") as fh:
        header = ["Mondo", "annotations", "MAxO (n)", "HPO (n)", "example MAxO", "example relation", "Example HPO"]
        fh.write("\t".join(header) + "\n")
        for row in summary_rows:
            fh.write("\t".join(row) + "\n")
    logger.info("Summary written to %s", args.out)

    print_total_stats(disease_to_entries)

    existing = ExistingAnnot.ingest()
    overlapping = [
        e
        for entries in disease_to_entries.values()
        for e in entries
        if has_overlap(e, existing)
    ]

    if overlapping:
        logger.warning(
            "%d automaxo entries already exist in %s — they will still be written to %s",
            len(overlapping),
            EXISTING_ANNOT_FILE,
            AUTOMAXO_ANNOT_FILE,
        )
        for e in overlapping:
            logger.warning("  Overlap: %s %s %s %s", e.disease_id, e.source_id, e.maxo_id, e.hpo_id)
    else:
        logger.info("No overlaps with existing annotations")

    if args.dry_run:
        logger.info("Dry run — skipping write of %s", AUTOMAXO_ANNOT_FILE)
        sys.exit(0)

    written = write_automaxo_annotations(disease_to_entries)
    logger.info("Wrote %d annotations to %s", written, AUTOMAXO_ANNOT_FILE)
