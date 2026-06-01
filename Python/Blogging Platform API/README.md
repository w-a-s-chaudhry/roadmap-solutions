# Blogging Platform API

A Flask REST API for managing blog posts, backed by SQLite.

Project page: https://roadmap.sh/projects/blogging-platform-api

## Architecture

```
Blogging Platform API/
├── .gitignore
├── requirements.txt
├── schema.sql        Table definition — run once to initialise the DB
├── db.py             SQLite connection management (Flask g pattern)
└── app.py            Flask routes + request validation
```

## Setup

```bash
cd "Blogging Platform API"
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

`posts.db` is created automatically on first run.

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | /posts | Create a post |
| GET | /posts | List all posts (supports `?term=` search) |
| GET | /posts/\<id\> | Get one post |
| PUT | /posts/\<id\> | Replace a post |
| DELETE | /posts/\<id\> | Delete a post |

**Request body (create / update):**

```json
{
  "title":    "My first post",
  "content":  "Hello, world.",
  "category": "general",
  "tags":     ["intro", "hello"]
}
```

`title`, `content`, and `category` are required. `tags` is optional.

**Search:**

```bash
curl "http://localhost:5000/posts?term=hello"
```

Matches against `title`, `content`, and `category`.
