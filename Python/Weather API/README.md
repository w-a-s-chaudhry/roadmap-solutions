# Weather API

A Flask API that returns weather data for any city by proxying
[Visual Crossing](https://www.visualcrossing.com/) and caching
responses in Redis for 12 hours to avoid burning API quota.

Project page: https://roadmap.sh/projects/weather-api

## Architecture

```
Weather API/
├── .env.example      Required environment variables (copy to .env)
├── .gitignore
├── requirements.txt
└── app.py            Flask route + Redis caching + rate limiting
```

## Setup

**Prerequisites:** Redis running locally (or set `REDIS_URL` to a
remote instance). Get a free Visual Crossing API key at
https://www.visualcrossing.com/

```bash
cd "Weather API"
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env — add your Visual Crossing key
```

## Run

```bash
python app.py
```

## API

`GET /weather/<city>`

```bash
curl http://localhost:5000/weather/london
```

Returns the full Visual Crossing timeline JSON for the city.
Requests within 12 hours of a previous call are served from Redis.

| Status | Meaning |
|--------|---------|
| 200 | Weather data (live or cached) |
| 404 | City not found |
| 429 | Rate limit exceeded (30/min or 1000/day) |
| 502 | Visual Crossing unreachable |
