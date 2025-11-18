
# FastAPI Calculator + Users — CI tests (coverage not enforced)

## Local run
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://127.0.0.1:8000
```

## Tests
```powershell
pytest
```
Coverage is reported but not enforced to 100% (gate removed).

## Docker (Postgres + pgAdmin)
```powershell
copy .env.example .env
docker compose up --build -d
# App:     http://localhost:8000
# pgAdmin: http://localhost:5050  (admin@local.dev / admin123)
# Host DB: localhost:5433 (inside compose use db:5432)
```

## CI
GitHub Actions workflow runs tests on push/PR.
