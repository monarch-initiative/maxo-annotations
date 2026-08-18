from csv import DictReader
from pathlib import Path

import click

from maxoa.terms import apply_term_updates, log_replacement_summary

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
POET_FILE = REPO_ROOT / "data" / "poet" / "annotations.tsv"
AUTOMAXO_FILE = REPO_ROOT / "data" / "automaxo" / "automaxo-annotations.tsv"
DEFAULT_OUT = REPO_ROOT / "data" / "maxo-annotations.tsv"

DEDUP_KEY = ("disease_id", "source_id", "maxo_id", "hpo_id")


def _read_tsv(path: Path) -> tuple[str, list[dict]]:
    with open(path, newline="") as f:
        header = f.readline().rstrip("\r\n")
        fieldnames = [c.strip() for c in header.split("\t")]
        rows = list(DictReader(f, fieldnames=fieldnames, delimiter="\t"))
    return header, rows


def _row_key(row: dict) -> tuple:
    return tuple(row.get(k, "").strip() for k in DEDUP_KEY)


def _normalize(row: dict) -> dict:
    row["relation"] = row.get("relation", "").strip().lower()
    return row


@click.command()
@click.argument("output", default=str(DEFAULT_OUT), type=click.Path(path_type=Path))
def merge(output: Path) -> None:
    """Merge all annotation sources into a single deduplicated file.

    OUTPUT defaults to data/maxo-annotations.tsv.
    """
    poet_header, poet_rows = _read_tsv(POET_FILE)
    _, automaxo_rows = _read_tsv(AUTOMAXO_FILE)

    poet_rows = [apply_term_updates(_normalize(r)) for r in poet_rows]
    automaxo_rows = [apply_term_updates(_normalize(r)) for r in automaxo_rows]

    seen = {_row_key(r) for r in poet_rows}
    overlaps = [r for r in automaxo_rows if _row_key(r) in seen]
    new_rows = [r for r in automaxo_rows if _row_key(r) not in seen]

    if overlaps:
        click.echo(f"Overlaps (skipped): {len(overlaps)}", err=True)
        for r in overlaps:
            click.echo(f"  {r['disease_id']}  {r['source_id']}  {r['maxo_id']}  {r['hpo_id']}", err=True)
    else:
        click.echo("No overlaps")

    with open(output, "w") as f:
        f.write(poet_header + "\n")
        for r in poet_rows:
            f.write("\t".join(r.values()) + "\n")
        for r in new_rows:
            f.write("\t".join(r.values()) + "\n")

    log_replacement_summary()

    click.echo(f"POET:     {len(poet_rows)}")
    click.echo(f"Automaxo: {len(automaxo_rows)}")
    click.echo(f"Merged:   {len(poet_rows) + len(new_rows)}")
    click.echo(f"Written:  {output}")
