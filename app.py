from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from config import PROJECT_NAME, DESCRIPTION, TABLE, FIELDS, SAMPLES

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-for-production"
DB_PATH = Path(__file__).with_name("app.db")

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def initialize():
    definitions = ", ".join(f'"{f["key"]}" TEXT' for f in FIELDS)
    with connect() as db:
        db.execute(
            f'CREATE TABLE IF NOT EXISTS "{TABLE}" '
            f'(id INTEGER PRIMARY KEY AUTOINCREMENT, {definitions})'
        )
        count = db.execute(f'SELECT COUNT(*) FROM "{TABLE}"').fetchone()[0]
        if count == 0:
            keys = ", ".join(f'"{f["key"]}"' for f in FIELDS)
            marks = ", ".join("?" for _ in FIELDS)
            db.executemany(
                f'INSERT INTO "{TABLE}" ({keys}) VALUES ({marks})',
                SAMPLES
            )

def get_values():
    values = {}
    for field in FIELDS:
        value = request.form.get(field["key"], "").strip()
        if field["required"] and not value:
            raise ValueError(f'{field["label"]} is required.')
        values[field["key"]] = value
    return values

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    with connect() as db:
        if q:
            conditions = " OR ".join(
                f'CAST("{f["key"]}" AS TEXT) LIKE ?' for f in FIELDS
            )
            params = [f"%{q}%"] * len(FIELDS)
            rows = db.execute(
                f'SELECT * FROM "{TABLE}" WHERE {conditions} ORDER BY id DESC',
                params
            ).fetchall()
        else:
            rows = db.execute(
                f'SELECT * FROM "{TABLE}" ORDER BY id DESC'
            ).fetchall()

        total = db.execute(
            f'SELECT COUNT(*) FROM "{TABLE}"'
        ).fetchone()[0]

    return render_template(
        "index.html", project=PROJECT_NAME, description=DESCRIPTION,
        fields=FIELDS, rows=rows, q=q, total=total
    )

@app.route("/add", methods=["POST"])
def add():
    try:
        values = get_values()
        columns = ", ".join(f'"{f["key"]}"' for f in FIELDS)
        marks = ", ".join("?" for _ in FIELDS)
        with connect() as db:
            db.execute(
                f'INSERT INTO "{TABLE}" ({columns}) VALUES ({marks})',
                [values[f["key"]] for f in FIELDS]
            )
        flash("Record added successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    with connect() as db:
        db.execute(f'DELETE FROM "{TABLE}" WHERE id = ?', (record_id,))
    flash("Record deleted.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    initialize()
    app.run(debug=True)
