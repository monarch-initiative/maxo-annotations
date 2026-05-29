# maxo-annotations

Repository for Medical Action Ontology (MAxO) therapeutic annotations for rare diseases, sourced from manual curation and automated pipelines.

## Repository Structure

```
annotations/
  maxo-annotations.tsv       # Primary annotations pulled from POET curation system
  automaxo-annotations.tsv   # Annotations derived from automaxo pipeline
  merged-annotations.tsv     # Merged output of all sources (generated)
  maxo_diagnostic_annotations.tsv

automaxo/
  maxo_<Disease>.tsv         # Per-disease automaxo curation files

scripts/
  summarize_automaxo.py      # Converts automaxo/ files → automaxo-annotations.tsv
  merge_annotations.py       # Merges all annotation sources → merged-annotations.tsv
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

Replace `annotations/maxo-annotations.tsv` with the latest export from the POET curation system.

### 2. Generate automaxo annotations

```bash
python scripts/summarize_automaxo.py -a automaxo/
```

Reads all `automaxo/*.tsv` files, deduplicates, and writes `annotations/automaxo-annotations.tsv`. Also writes a per-disease summary to `am_summary.tsv`.

Add `--dry-run` to check for overlaps without writing.

### 3. Merge

```bash
python scripts/merge_annotations.py
```

Merges `maxo-annotations.tsv` and `automaxo-annotations.tsv`, deduplicating on `(disease_id, source_id, maxo_id, hpo_id)`. Reports any overlaps. Writes `annotations/merged-annotations.tsv`.

Custom output path:

```bash
python scripts/merge_annotations.py path/to/output.tsv
```
