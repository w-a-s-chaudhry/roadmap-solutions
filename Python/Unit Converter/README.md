# Unit Converter

A small Flask web app that converts between units of length
(metres, kilometres, miles, feet, inches) and temperature
(Celsius, Fahrenheit, Kelvin).

Project page: https://roadmap.sh/projects/unit-converter

## Architecture

```
Unit Converter/
├── .env              FLASK_DEBUG and other config
├── .gitignore
├── requirements.txt
├── app.py            Flask routes + JSON API
├── converter.py      Pure-Python conversion classes
└── templates/
    └── index.html    Single-page frontend (HTML + JS + CSS)
```

- `converter.py` contains the maths and knows nothing about Flask.
- `app.py` handles HTTP, validates input, and delegates to the
  converter classes.
- `templates/index.html` is served on `GET /` and talks to the
  backend via `POST /convert` using `fetch()`.

## Setup

```bash
cd "Unit Converter"

python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open <http://localhost:5000> in your browser.

## API

`POST /convert`

Request body:

```json
{
  "category":  "length",
  "value":     100,
  "from_unit": "km",
  "to_unit":   "miles"
}
```

Success response (HTTP 200):

```json
{
  "result":    62.137119,
  "from_unit": "km",
  "to_unit":   "miles"
}
```

Error response (HTTP 400):

```json
{ "error": "value must be a number" }
```

Quick test from the command line while the server is running:

```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d "{\"category\":\"length\",\"value\":100,\"from_unit\":\"km\",\"to_unit\":\"miles\"}"
```

## Supported units

| Category    | Units                                |
|-------------|--------------------------------------|
| length      | `millimeters`, `centimeters`, `meters`, `kilometers`, `inches`, `feet`, `yards`, `miles` |
| temperature | `celsius`, `fahrenheit`, `kelvin`    |
| weight      | `mg`, `g`, `kg`, `oz`, `lb`          |
