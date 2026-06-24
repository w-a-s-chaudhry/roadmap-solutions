# Job Listings Scraper

A web scraper that collects job postings from the Real Python
[Fake Jobs](https://realpython.github.io/fake-jobs/) practice site and
writes them to a CSV file. Each posting yields four fields — title,
company, location, and the detail-page URL.

Solution to the [Job Listings Scraper](https://roadmap.sh/projects/job-listings-scraper)
project from roadmap.sh.

## Install

This project uses [uv](https://docs.astral.sh/uv/). From this directory:

```bash
uv sync
```

That creates the virtual environment and installs `requests` and
`beautifulsoup4`, and exposes the `job-scraper` command.

## Usage

```bash
uv run job-scraper
```

There are no flags. The source URL and output path are fixed module
constants, so the command always scrapes the Fake Jobs page and writes
the results to `jobs.csv` in the current directory:

```
Wrote 100 jobs to jobs.csv
```

The CSV has a header row followed by one row per posting:

```
title,company,location,url
Senior Python Developer,"Payne, Roberts and Davis","Stewartbury, AA",https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html
...
```

## How it works

The scrape is three small steps, one function each:

1. **Fetch** — `fetch_page` issues a `GET` with a 10-second timeout. On a
   network error or a non-200 status it prints a diagnostic and returns
   `None` (the run stops cleanly); otherwise it returns the page HTML.
2. **Parse** — `parse_jobs` hands the HTML to BeautifulSoup and iterates
   each `div.card-content`, pulling `h2.title`, `h3.company`,
   `p.location`, and the posting's detail link (the last `<a>` in the
   card footer). A missing field falls back to `""` rather than crashing.
3. **Save** — `save_csv` writes the list of dicts with `csv.DictWriter`,
   a header row followed by the postings.

## Tests

```bash
uv run pytest tests/ -v
```

The tests mock the network and use a temporary directory for file
output, so they run without internet access and leave no files behind.
