"""Fetch obsolete MAxO term replacements from the live ontology via pronto."""

import logging
import ssl
import urllib.request
from collections import defaultdict
from functools import lru_cache

import certifi
import pronto

logger = logging.getLogger(__name__)

MAXO_OBO_URL = "http://purl.obolibrary.org/obo/maxo.owl"

_replacement_counts: dict[str, int] = defaultdict(int)


@lru_cache(maxsize=1)
def _build_replacement_map() -> dict[str, tuple[str, str]]:
    """Load MAxO OBO and return {obsolete_id: (current_id, current_name)}."""
    logger.info("Loading MAxO ontology from %s", MAXO_OBO_URL)
    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_ctx))
    urllib.request.install_opener(opener)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ont = pronto.Ontology(MAXO_OBO_URL)
    replacements: dict[str, tuple[str, str]] = {}
    for term in ont.terms():
        if term.obsolete and term.replaced_by:
            for replacement in term.replaced_by:
                replacements[term.id] = (replacement.id, replacement.name or "")
                break  # take first replacement
    logger.info("Found %d obsolete terms with replacements", len(replacements))
    return replacements


def apply_term_updates(row: dict) -> dict:
    """Replace obsolete maxo_id/maxo_name in a row dict in-place."""
    replacement_map = _build_replacement_map()
    maxo_id = row.get("maxo_id", "")
    if maxo_id in replacement_map:
        new_id, new_name = replacement_map[maxo_id]
        _replacement_counts[f"{maxo_id} → {new_id}"] += 1
        row["maxo_id"] = new_id
        if new_name:
            row["maxo_name"] = new_name
    return row


def log_replacement_summary() -> None:
    """Log total obsolete term replacements made. Call once after processing."""
    total = sum(_replacement_counts.values())
    logger.info("Obsolete MAxO term replacements: %d", total)
