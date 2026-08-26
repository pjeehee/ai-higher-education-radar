# Acceptance tests
1. Unofficial result -> rejected before publish.
2. Official page with missing date -> needs_review; date is never inferred.
3. Search snippet supports claim but primary page does not -> rejected.
4. Duplicate press release + original report -> original retained; duplicate merged.
5. Contradictory verified evidence -> both retained; signal flagged for review.
6. Broken source URL -> existing Evidence retained with link-health flag.
7. No new sources -> run ends with no material change.
8. Verified new source -> provenance ID assigned, signal/gap recalculated.
9. Candidate cannot appear in executive brief.
10. Intelligence text cannot overwrite source-supported fact.
