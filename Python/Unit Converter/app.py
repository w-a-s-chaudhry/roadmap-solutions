# Author:      Wajid Ali Saleem Chaudhry
# Description: Flask web layer for the unit converter. Serves the
#              HTML page on / and exposes POST /convert as a JSON API
#              that delegates to converter.py.

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from converter import (
  LengthConverter,
  TemperatureConverter,
  WeightConverter,
)


# --- App setup ---

# Read .env into os.environ so os.getenv() works below. Must run
# before we read any env vars.
load_dotenv()

app = Flask(__name__)

# Dispatch table: category name -> converter instance. Adding a new
# category later (mass, volume, ...) only means adding a class in
# converter.py and one line here — no route changes.
converters = {
  "length":      LengthConverter(),
  "temperature": TemperatureConverter(),
  "weight":      WeightConverter(),
}


# --- Routes ---

# GET / -> serve the single-page HTML frontend from templates/.
@app.route("/")
def home():
  return render_template("index.html")

# POST /convert -> JSON API. Expects a body like:
#   {"category": "length", "value": 100,
#    "from_unit": "km", "to_unit": "miles"}
# Returns {"result": ..., "from_unit": ..., "to_unit": ...} on
# success, or {"error": "..."} with HTTP 400 on bad input.
@app.route("/convert", methods=["POST"])
def convert():
  data = request.get_json(silent=True)
  if not data:
    return jsonify({"error": "Request body must be JSON"}), 400

  # Pull each required field; missing -> 400.
  required = ("category", "value", "from_unit", "to_unit")
  missing  = [k for k in required if k not in data]
  if missing:
    return jsonify({
      "error": f"Missing field(s): {', '.join(missing)}"
    }), 400

  # Coerce value to float; non-numeric -> 400 (don't 500).
  try:
    value = float(data["value"])
  except (TypeError, ValueError):
    return jsonify({"error": "value must be a number"}), 400

  category  = data["category"]
  from_unit = data["from_unit"]
  to_unit   = data["to_unit"]

  if category not in converters:
    return jsonify({
      "error": f"Unknown category: {category}"
    }), 400

  # Delegate to the right converter; its ValueError (unknown unit)
  # also surfaces as a 400 rather than crashing the server.
  try:
    result = converters[category].convert(value, from_unit, to_unit)
  except ValueError as e:
    return jsonify({"error": str(e)}), 400

  return jsonify({
    "result":    round(result, 6),
    "from_unit": from_unit,
    "to_unit":   to_unit,
  })


# --- Error handlers ---
# Return JSON for 404/500 too, so the frontend's fetch() always
# parses the response the same way regardless of outcome.

@app.errorhandler(404)
def not_found(_e):
  return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(_e):
  return jsonify({"error": "Internal server error"}), 500


# --- Entrypoint ---

if __name__ == "__main__":
  debug = os.getenv("FLASK_DEBUG", "False") == "True"
  app.run(debug=debug, port=5000)
