# Personal Blog (Field Notes)

A personal blog called *Field Notes* — a Flask backend that serves a
React SPA and exposes a JSON CRUD API backed by a flat file on disk.
Write operations are gated behind HTTP Basic Auth.

Project page: https://roadmap.sh/projects/personal-blog

## Architecture

```
Personal Blog/
├── .env              ADMIN_USERNAME, ADMIN_PASSWORD, FLASK_DEBUG
├── requirements.txt
├── app.py            Flask routes + Basic Auth + JSON file storage
├── seed.json         Default articles (copied to articles.json on
│                     first run if it does not exist)
├── static/           Compiled React SPA (JS / CSS)
└── templates/
    └── index.html    Shell page that loads the SPA
```

## Setup

```bash
cd "Personal Blog"
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Create .env
echo ADMIN_USERNAME=admin > .env
echo ADMIN_PASSWORD=yourpassword >> .env
```

## Run

```bash
python app.py
```

Open http://localhost:5000. To reach the admin panel, go to
http://localhost:5000/admin and enter your credentials when prompted.
The browser caches them for the origin, so the SPA's write calls
authenticate automatically without re-prompting.

## API

Public endpoints require no auth. Write endpoints require HTTP
Basic Auth.

| Method | Path | Auth | Description |
|--------|------|:----:|-------------|
| GET | /api/articles | — | List all articles |
| GET | /api/articles/\<id\> | — | Get one article |
| POST | /api/articles | ✓ | Create an article |
| PUT | /api/articles/\<id\> | ✓ | Replace an article |
| DELETE | /api/articles/\<id\> | ✓ | Delete an article |
