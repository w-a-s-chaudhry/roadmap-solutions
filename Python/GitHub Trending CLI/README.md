# GitHub Trending CLI

A CLI that fetches and displays trending GitHub repositories for a given
time window, sorted by stars. Uses the GitHub Search API with a
`created:>DATE` proxy since no official trending endpoint exists.

Solution to the [GitHub Trending](https://roadmap.sh/projects/github-trending-cli)
project from roadmap.sh.

## Install

This project uses [uv](https://docs.astral.sh/uv/). From this directory:

```bash
uv tool install .
```

That builds the package and exposes the `trending-repos` command on your
PATH. For local development without installing globally, use
`uv run trending-repos` from this directory instead.

## Usage

```bash
trending-repos                          # top 10 repos this week
trending-repos --duration day           # trending today
trending-repos --duration month         # trending this month
trending-repos --duration year          # trending this year
trending-repos --duration week --limit 5
```

### Options

| Flag         | Values                      | Default |
|--------------|-----------------------------|---------|
| `--duration` | `day`, `week`, `month`, `year` | `week`  |
| `--limit`    | any positive integer        | `10`    |

## Rate limit

The GitHub Search API allows 60 unauthenticated requests per hour.
