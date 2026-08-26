# Live backend handoff
1. Schedule Source Registry searches.
2. Save discovered URLs as candidates only.
3. Fetch primary pages and extract metadata.
4. Run verification queue; do not publish failed/ambiguous records.
5. Canonicalize URL/title and deduplicate.
6. Store verified Evidence separately from generated Signal/Implication text.
7. Recompute signal strength only from verified records.
8. Keep source URL and verification timestamp for every record.
9. Surface corrections/version history instead of silently overwriting.
10. Run periodic source-link health checks.
