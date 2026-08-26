# Deployment checklist

## Frontend
- Serve `index.html` over HTTPS.
- Keep Evidence data/API separate from generated Intelligence in production.
- Add authentication if review/admin screens should not be public.

## Backend
- Persistent Evidence database with immutable record IDs.
- Candidate / needs_review / verified / rejected workflow.
- Scheduled discovery jobs based on Source Registry.
- Primary-page fetch and metadata extraction.
- Duplicate detection and canonical URLs.
- Link-health checker.
- Correction/version history.

## Intelligence
- Recompute scores only from verified Evidence.
- Keep scoring weights versioned.
- Preserve contradictory Evidence.
- Require review before major signal-strength transitions.

## QA
- Test filters/search/navigation.
- Test empty states and malformed records.
- Test inaccessible/redirected source URLs.
- Test duplicate and correction workflows.
- Maintain backup/export of Evidence registry.
