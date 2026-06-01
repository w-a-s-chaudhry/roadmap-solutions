# Author:      Wajid Ali Saleem Chaudhry
# Description: SQLite connection helpers and schema initialization
#              for the blogging platform API.

import os
import sqlite3
from flask import g

# --- Configuration ---

DB_PATH = os.path.join(os.path.dirname(__file__), "posts.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

# --- Connection management ---

# Return the per-request SQLite connection, opening one if needed
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        # Rows behave like dicts: row["title"] instead of row[1]
        g.db.row_factory = sqlite3.Row
        # Enforce foreign keys (no-op now, useful later)
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

# Close the per-request connection at the end of the request
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# --- Schema setup ---

# Create tables from schema.sql if they don't already exist
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH) as f:
            conn.executescript(f.read())

# Register db lifecycle hooks on the Flask app
def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
