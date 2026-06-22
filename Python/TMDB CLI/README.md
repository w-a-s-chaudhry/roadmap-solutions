# TMDB CLI

A CLI that fetches and displays movies from
[The Movie Database (TMDB)](https://www.themoviedb.org/) by category —
now playing, popular, top rated, or upcoming — in a ranked table.

Solution to the [TMDB CLI](https://roadmap.sh/projects/tmdb-cli)
project from roadmap.sh.

## Install

This project uses [uv](https://docs.astral.sh/uv/). From this directory:

```bash
uv tool install .
```

That builds the package and exposes the `tmdb-app` command on your PATH.
For local development without installing globally, use `uv run tmdb-app`
from this directory instead.

## Authentication

TMDB requires an API token. The app reads it from an environment
variable named `TMDB_ACCESS_TOKEN`, sent to the API as a
`Authorization: Bearer <token>` header.

1. Create a free account at [themoviedb.org](https://www.themoviedb.org/)
   and verify your email.
2. Go to [Settings → API](https://www.themoviedb.org/settings/api) and
   request a **Developer** key.
3. Copy your **API Read Access Token** (the long token, *not* the short
   v3 API key).
4. Copy `.env.example` to `.env` and paste your token:

   ```
   TMDB_ACCESS_TOKEN=your-token-here
   ```

`.env` is gitignored, so your token is never committed.
[python-dotenv](https://pypi.org/project/python-dotenv/) loads it at
startup. A real environment variable (e.g. set in CI) works too — if
`.env` is absent, the app falls back to whatever is already in the
environment.

## Usage

```bash
tmdb-app                      # popular movies (default)
tmdb-app --type playing       # now playing in theatres
tmdb-app --type popular       # popular
tmdb-app --type top           # top rated
tmdb-app --type upcoming      # upcoming releases
```

### Options

| Flag     | Values                                      | Default   |
|----------|---------------------------------------------|-----------|
| `--type` | `playing`, `popular`, `top`, `upcoming`     | `popular` |

## Tests

```bash
uv run pytest tests/ -v
```

The tests mock the network and the environment, so they run without a
token and never make a real API call.
