# Author:      Wajid Ali Saleem Chaudhry
# Description: Flask backend for the Field Notes personal blog.
#              Serves the React SPA and exposes a JSON CRUD API at
#              /api/articles backed by a single JSON file on disk.

from flask import (
  Flask, render_template, request, jsonify, abort, redirect, Response,
)
from dotenv import load_dotenv
from functools import wraps
from pathlib import Path
import hmac
import json
import os
import re
import shutil


# --- App setup ---

load_dotenv()
app = Flask(__name__)

# Paths are resolved relative to this file so the working directory
# doesn't matter when launching the app.
ROOT = Path(__file__).parent
SEED_PATH    = ROOT / "seed.json"
STORAGE_PATH = ROOT / "articles.json"

# Admin credentials for the Basic Auth gate. Read from .env so they
# never end up in source. Missing/blank values fail closed below.
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")


# --- Authentication ---

# Constant-time compare on both fields so a wrong username doesn't
# fail faster than a wrong password.
def _check_credentials(user, pw):
  if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    return False
  ok_user = hmac.compare_digest(user, ADMIN_USERNAME)
  ok_pw   = hmac.compare_digest(pw,   ADMIN_PASSWORD)
  return ok_user and ok_pw

# Decorator that gates a view behind HTTP Basic Auth. The 401 +
# WWW-Authenticate response makes the browser pop its built-in
# credential prompt on the first hit; the browser then caches the
# credentials for the origin and replays them on later requests,
# including the SPA's fetch() writes.
def requires_auth(fn):
  @wraps(fn)
  def wrapped(*args, **kwargs):
    auth = request.authorization
    if not auth or not _check_credentials(
      auth.username or "", auth.password or ""
    ):
      return Response(
        "Authentication required",
        401,
        {"WWW-Authenticate": 'Basic realm="Field Notes admin"'},
      )
    return fn(*args, **kwargs)
  return wrapped


# --- Storage helpers ---

# Ensure articles.json exists. On first run we copy seed.json over,
# so the blog has content immediately. Subsequent runs leave the
# live data alone.
def ensure_storage():
  if not STORAGE_PATH.exists():
    shutil.copy(SEED_PATH, STORAGE_PATH)

# Load the full list of articles from disk. Always returns a list.
def load_articles():
  ensure_storage()
  with STORAGE_PATH.open("r", encoding="utf-8") as f:
    return json.load(f)

# Write the full list back to disk. Pretty-printed so the file
# stays diff-friendly if anyone ever inspects it by hand.
def save_articles(articles):
  with STORAGE_PATH.open("w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

# Find the next available a-NNN id by scanning every existing id
# and incrementing the largest numeric suffix. This survives
# deletions — we never reuse an id once it's been assigned.
def next_id(articles):
  highest = 0
  for a in articles:
    m = re.match(r"a-(\d+)$", a.get("id", ""))
    if m:
      n = int(m.group(1))
      if n > highest:
        highest = n
  return f"a-{highest + 1:03d}"

# Validate an incoming article payload. Returns (cleaned_dict, None)
# on success or (None, error_message) on failure. We accept the
# fields the frontend sends and ignore anything extra.
def validate_payload(data):
  if not isinstance(data, dict):
    return None, "Body must be a JSON object"

  title = (data.get("title") or "").strip()
  if not title:
    return None, "title is required"

  date = (data.get("date") or "").strip()
  if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
    return None, "date must be YYYY-MM-DD"

  body = data.get("body")
  if not isinstance(body, list):
    return None, "body must be a list of blocks"

  cleaned = {
    "title": title,
    "date":  date,
    "lede":  (data.get("lede") or "").strip(),
    "body":  body,
  }
  return cleaned, None


# --- Page route ---

# GET / -> serve the React SPA. All other in-app navigation is
# client-side hash routing.
@app.route("/")
def home():
  return render_template("index.html")

# GET /admin -> Basic Auth gate, then bounce to the SPA's admin
# hash route. The browser caches credentials for the origin, so
# subsequent write API calls authenticate automatically without
# re-prompting.
@app.route("/admin")
@requires_auth
def admin_entry():
  return redirect("/#/admin")


# --- JSON API: /api/articles ---

# GET /api/articles -> list every article. The frontend sorts.
@app.route("/api/articles", methods=["GET"])
def list_articles():
  return jsonify(load_articles())

# GET /api/articles/<id> -> single article, 404 if missing.
@app.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
  articles = load_articles()
  for a in articles:
    if a["id"] == article_id:
      return jsonify(a)
  return jsonify({"error": f"Article {article_id} not found"}), 404

# POST /api/articles -> create. Server assigns the id; client
# input for `id` is ignored.
@app.route("/api/articles", methods=["POST"])
@requires_auth
def create_article():
  cleaned, err = validate_payload(request.get_json(silent=True))
  if err:
    return jsonify({"error": err}), 400

  articles = load_articles()
  cleaned["id"] = next_id(articles)
  articles.append(cleaned)
  save_articles(articles)
  return jsonify(cleaned), 201

# PUT /api/articles/<id> -> replace an existing article. The id in
# the URL wins; any id in the body is ignored.
@app.route("/api/articles/<article_id>", methods=["PUT"])
@requires_auth
def update_article(article_id):
  cleaned, err = validate_payload(request.get_json(silent=True))
  if err:
    return jsonify({"error": err}), 400

  articles = load_articles()
  for i, a in enumerate(articles):
    if a["id"] == article_id:
      cleaned["id"] = article_id
      articles[i] = cleaned
      save_articles(articles)
      return jsonify(cleaned)
  return jsonify({"error": f"Article {article_id} not found"}), 404

# DELETE /api/articles/<id> -> remove. Idempotent: deleting a
# missing id still returns 404 so the client knows nothing changed.
@app.route("/api/articles/<article_id>", methods=["DELETE"])
@requires_auth
def delete_article(article_id):
  articles = load_articles()
  new_list = [a for a in articles if a["id"] != article_id]
  if len(new_list) == len(articles):
    return jsonify({"error": f"Article {article_id} not found"}), 404
  save_articles(new_list)
  return ("", 204)


# --- Error handlers ---
# Always return JSON for API errors so the frontend's fetch() can
# parse the response the same way regardless of outcome.

@app.errorhandler(404)
def not_found(_e):
  return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(_e):
  return jsonify({"error": "Internal server error"}), 500


# --- Entrypoint ---

if __name__ == "__main__":
  debug = os.getenv("FLASK_DEBUG", "False") == "True"
  app.run(debug=debug, port=5000)
