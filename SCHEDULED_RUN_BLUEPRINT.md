# Scheduled run blueprint

## Daily / frequent discovery
- Search priority Source Registry endpoints for newly published or updated official materials.
- Save results as `candidate` only.
- Compare canonical URL, title, publication/update date and content fingerprint with existing records.

## Verification
- Fetch official primary page.
- Validate metadata and every proposed fact.
- Run relevance and duplicate checks.
- Route ambiguity or contradiction to `needs_review`.

## Intelligence update
- Only `verified` records contribute to signal scoring.
- Recompute signal scores after verified changes.
- Log any STRONG/GROWING/WATCH transition.
- Preserve contradictory evidence rather than suppressing it.

## Publishing
- Update Today Brief only when verified evidence creates a meaningful change.
- Otherwise retain the prior brief and show no material change.
- Keep provenance ID and correction history for every published item.
