# maxo-annotations

Repository for Medical Action Ontology (MAxO) therapeutic annotations for rare diseases, sourced from manual curation and automated pipelines.

## Repository Structure

```
data/
  poet/
    annotations.tsv                    # Primary annotations from POET curation system
    maxo_diagnostic_annotations.tsv
  automaxo/
    maxo_<Disease>.tsv                # Per-disease automaxo curation source files
    automaxo-annotations.tsv         # Generated from automaxo source files
  maxo-annotations.tsv                # Final merged output (generated)

src/maxoa/                            # CLI package
scripts/
  update_obsolete_maxo_terms.py
```

## Annotation Format

All annotation files share the same TSV schema (15 columns):

| Column | Description |
|---|---|
| `disease_id` | MONDO identifier |
| `disease_name` | Disease label |
| `source_id` | PMID or URL |
| `maxo_id` | MAxO term identifier |
| `maxo_name` | MAxO term label |
| `hpo_id` | HPO term identifier |
| `relation` | `TREATS`, `PREVENTS`, etc. |
| `evidence` | Evidence code (e.g. `PCS`, `TAS`) |
| `extension_id` | Optional extension term ID |
| `extension_name` | Optional extension term label |
| `comment` | Free text comment |
| `other` | Additional notes |
| `author` | Curator ORCID |
| `last_updated` | Last update date |
| `created` | Creation date |

## Workflow

### 1. Pull fresh POET annotations

Replace `data/poet/annotations.tsv` with the latest export from the POET curation system.

### 2. Generate automaxo annotations

```bash
maxoa generate automaxo
```

Reads all `data/automaxo/*.tsv` files, deduplicates, and writes `data/automaxo/automaxo-annotations.tsv`. Also writes a per-disease summary to `am_summary.tsv`.

Options:
- `-a` / `--automaxo-dir` — override source directory (default: `data/automaxo/`)
- `-o` / `--out` — override summary output path
- `--dry-run` — check overlaps without writing

### 3. Merge

```bash
maxoa merge
```

Merges POET and automaxo annotations, deduplicating on `(disease_id, source_id, maxo_id, hpo_id)`. Reports overlaps. Writes `data/maxo-annotations.tsv`.

Custom output path:

```bash
maxoa merge path/to/output.tsv
```
