# Author:      Wajid Ali Saleem Chaudhry
# Description: Flask app exposing a small blogging platform REST API
#              with CRUD endpoints over /posts.

import os
from flask import Flask, jsonify, request, abort

import db

app = Flask(__name__)
db.init_app(app)

# --- Routes ---

# Convert a sqlite3.Row into the JSON shape we return to clients
def row_to_post(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "category": row["category"],
        "tags": row["tags"].split(",") if row["tags"] else [],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }

# Create a new blog post from the request body
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True) or {}
    required = ("title", "content", "category")
    if not all(field in data and data[field] for field in required):
        abort(400, "title, content and category are required")

    tags = ",".join(data.get("tags", []))
    conn = db.get_db()
    cursor = conn.execute(
        "INSERT INTO posts (title, content, category, tags) "
        "VALUES (?, ?, ?, ?)",
        (data["title"], data["content"], data["category"], tags),
    )
    conn.commit()

    row = conn.execute(
        "SELECT * FROM posts WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(row_to_post(row)), 201

# Update the post identified by id with fields from the request body
@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    data = request.get_json(silent=True) or {}
    conn = db.get_db()

    exists = conn.execute(
        "SELECT 1 FROM posts WHERE id = ?", (id,)
    ).fetchone()
    if exists is None:
        abort(404, f"post {id} not found")

    set_parts = []
    values = []
    for field in ("title", "content", "category"):
        if field in data:
            set_parts.append(f"{field} = ?")
            values.append(data[field])
    if "tags" in data:
        set_parts.append("tags = ?")
        values.append(",".join(data["tags"]))

    if not set_parts:
        abort(400, "no updatable fields supplied")

    set_parts.append("updated_at = CURRENT_TIMESTAMP")
    values.append(id)
    conn.execute(
        f"UPDATE posts SET {', '.join(set_parts)} WHERE id = ?",
        values,
    )
    conn.commit()

    row = conn.execute(
        "SELECT * FROM posts WHERE id = ?", (id,)
    ).fetchone()
    return jsonify(row_to_post(row))

# Delete the post identified by id
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    conn = db.get_db()
    cursor = conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    if cursor.rowcount == 0:
        abort(404, f"post {id} not found")
    return "", 204

# Return a single post by id, or 404 if missing
@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    conn = db.get_db()
    row = conn.execute(
        "SELECT * FROM posts WHERE id = ?", (id,)
    ).fetchone()
    if row is None:
        abort(404, f"post {id} not found")
    return jsonify(row_to_post(row))

# Return all posts, optionally filtered by a ?term= search query
@app.route("/posts", methods=["GET"])
def get_all_posts():
    term = request.args.get("term")
    conn = db.get_db()
    if term:
        like = f"%{term}%"
        rows = conn.execute(
            "SELECT * FROM posts "
            "WHERE title LIKE ? OR content LIKE ? OR category LIKE ? "
            "ORDER BY id DESC",
            (like, like, like),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY id DESC"
        ).fetchall()
    return jsonify([row_to_post(r) for r in rows])

# --- Entrypoint ---

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug, port=5000)
