# Render deployment

This package is ready for a Render Web Service.

- Runtime: Python
- Build: `pip install -r requirements.txt`
- Start: `gunicorn backend.app:app`
- Health check: `/health`
- Blueprint: `render.yaml`

## Important database note
The bundled `radar.db` is suitable for the initial read-oriented deployment.
Render's default filesystem is ephemeral, so runtime writes to SQLite will not persist across redeploys/restarts.
For a production write-enabled version, use Render Postgres or a paid persistent disk and set `RADAR_DB_PATH` to a path on that disk.

## GitHub → Render
1. Push this folder to a GitHub repository.
2. In Render choose New → Blueprint or Web Service.
3. Connect the repository. Render detects `render.yaml`.
4. Deploy.
