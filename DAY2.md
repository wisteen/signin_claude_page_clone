# Day 2

Install API deps: `python -m pip install -r requirements.txt`

Run API: `$env:PORT=8000; uvicorn api.main:app --host 0.0.0.0 --port $env:PORT`

Run frontend: `npm run dev`

Optional frontend API override: `$env:VITE_API_BASE_URL="http://localhost:8000"`

Submit the form, then check saved entries at `http://localhost:8000/api/submissions`.

Entries are saved in SQLite at `api/submissions.db`.

Passwords are accepted by the API but are not logged, saved, or returned.
