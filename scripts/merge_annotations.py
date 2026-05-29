"""
Merge maxo-annotations.tsv (POET) with automaxo-annotations.tsv.
Deduplicates on (disease_id, source_id, maxo_id, hpo_id) and reports overlaps.
Usage: python scripts/merge_annotations.py [output_file]
"""

import sys
from csv import DictReader
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POET_FILE = REPO_ROOT / "annotations" / "maxo-annotations.tsv"
AUTOMAXO_FILE = REPO_ROOT / "annotations" / "automaxo-annotations.tsv"
DEFAULT_OUT = REPO_ROOT / "annotations" / "merged-annotations.tsv"

DEDUP_KEY = ("disease_id", "source_id", "maxo_id", "hpo_id")


def read_tsv(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="") as f:
        header = f.readline().rstrip("\r\n")
        fieldnames = [c.strip() for c in header.split("\t")]
        rows = list(DictReader(f, fieldnames=fieldnames, delimiter="\t"))
    return header, rows


def row_key(row: dict) -> tuple:
    return tuple(row.get(k, "").strip() for k in DEDUP_KEY)


if __name__ == "__main__":
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT

    poet_header, poet_rows = read_tsv(POET_FILE)
    _, automaxo_rows = read_tsv(AUTOMAXO_FILE)

    seen = {row_key(r) for r in poet_rows}

    overlaps = [r for r in automaxo_rows if row_key(r) in seen]
    new_rows = [r for r in automaxo_rows if row_key(r) not in seen]

    if overlaps:
        print(f"Overlaps (skipped): {len(overlaps)}")
        for r in overlaps:
            print(f"  {r['disease_id']}  {r['source_id']}  {r['maxo_id']}  {r['hpo_id']}")
    else:
        print("No overlaps")

    with open(out_path, "w") as f:
        f.write(poet_header + "\n")
        for r in poet_rows:
            f.write("\t".join(r.values()) + "\n")
        for r in new_rows:
            f.write("\t".join(r.values()) + "\n")

    print(f"POET:     {len(poet_rows)}")
    print(f"Automaxo: {len(automaxo_rows)}")
    print(f"Merged:   {len(poet_rows) + len(new_rows)}")
    print(f"Written:  {out_path}")
