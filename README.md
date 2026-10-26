# StudySync: Group Study Session Planner and Task Tracker

A Flask web app where student groups schedule study sessions, assign tasks, and track progress on a shared dashboard.

## Features (must-have, implemented)
Registration/login, group create/join by code, study session CRUD, task CRUD with assignment, status tracking (To Do / In Progress / Done), group dashboard with progress, and role-based access control.

## Tech stack
Python 3, Flask, SQLAlchemy (SQLite), Flask-Login, Flask-WTF (CSRF), Flask-Migrate, Bootstrap 5, pytest, GitHub Actions.

## Project structure
```
studysync/
  app/
    __init__.py         app factory and extensions
    models.py           User, Group, Membership, StudySession, Task
    helpers.py          access-control and parsing helpers
    auth.py             register / login / logout
    groups.py           create, join, remove member, delete
    study_sessions.py   session CRUD
    tasks.py            task CRUD and status
    dashboard.py        home and group dashboard
    templates/          Jinja2 + Bootstrap pages
  tests/                pytest suite
  docs/                 GitHub setup + iteration review template
  .github/              CI workflow, issue and PR templates
  config.py  run.py  seed.py  requirements.txt  Procfile  render.yaml
```

## Getting started
```bash
git clone <your-repo-url> && cd studysync
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py                   # optional demo data
python run.py                    # http://127.0.0.1:5000
```

## Run tests
```bash
pytest --cov=app --cov-report=term-missing
```

## Deploy to Render (free tier)
1. Push the repo to GitHub.
2. On render.com: New > Blueprint (or Web Service), connect the repo. `render.yaml` sets the build/start commands.
3. Note: the free tier has an ephemeral filesystem, so the SQLite data can reset on redeploy. For a persistent database, set a `DATABASE_URL` (e.g. a free Postgres) and add `psycopg2-binary` to `requirements.txt`.
4. Alternative: PythonAnywhere, which keeps SQLite files persistent on the free tier.

## Requirements traceability
| Requirement | Code | Tests |
|---|---|---|
| FR1, FR2 | app/auth.py | tests/test_auth.py |
| FR3, FR4, FR10 | app/groups.py | tests/test_groups.py |
| FR5 | app/study_sessions.py | tests/test_sessions_tasks.py |
| FR6, FR7 | app/tasks.py | tests/test_sessions_tasks.py |
| FR8 | app/dashboard.py | tests/test_sessions_tasks.py |
| FR9 | app/helpers.py | tests/test_access.py |

## Team
Mohamed Alarbah, Mohamed Abdullah
