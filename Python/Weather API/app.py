from flask import Flask, jsonify
from dotenv import load_dotenv
import requests
import os
import redis
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute", "1000 per day"],
    storage_uri=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)


WEATHER_API_KEY = os.getenv("VISUAL_CROSSING_KEY","")

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)

# --- Errors ---

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "rate limit exceeded", "detail": str(e.description)}), 429

# --- Routes ---

# Fetch weather for a city from Visual Crossing and return as JSON
@app.route("/weather/<city>")
def get_weather(city):
  key = f"weather:{city.lower()}"

  try:
    cached = redis_client.get(key)
    if cached:
      return jsonify(json.loads(cached))
  except redis.RedisError:
    pass

  url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={WEATHER_API_KEY}"
 
  try:
    response = requests.get(url)
  except requests.RequestException:
    return jsonify({"error": "upstream weather service unavailable"}), 502
 
  if response.status_code != 200:
    return jsonify({"error": "city not found"}), 404
  
  data = response.json()

  try:
    redis_client.setex(key,43200,json.dumps(data))
  except redis.RedisError:
    pass

  return jsonify(data)

# --- Entrypoint ---

if __name__ == "__main__":
  debug = os.getenv("FLASK_DEBUG", "False") == "True"
  app.run(debug=debug, port=5000)

