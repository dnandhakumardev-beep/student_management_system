# Student Management System

Manage student records with search, add, edit and delete features.

## Features
- Add records with required-field validation
- Search across stored fields
- View record counts and all saved records
- Delete records with confirmation
- SQLite persistence and automatic sample-data initialization
- Responsive HTML interface

## Requirements
- Python 3.11+
- pip

## Run locally

```bash
python -m venv .venv
```

Activate the environment:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

The database and sample records are created automatically on first run.
To reset demo data, stop the server and delete `app.db`, then restart.

## Project structure

- `app.py` - Flask routes and database operations
- `config.py` - Project fields and demo records
- `templates/index.html` - User interface
- `requirements.txt` - Python dependency
- `.gitignore` - Local files excluded from Git

## GitHub upload

Create a new empty repository on GitHub, then run these commands inside this folder:

```bash
git init
git add .
git commit -m "Add Student Management System"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace the example remote URL with your repository URL.

## Limitations and next steps

This is a portfolio starter, not a production deployment. Before production use,
add authentication, CSRF protection, stronger field validation, automated tests,
and production server configuration. Never expose a development server publicly.
