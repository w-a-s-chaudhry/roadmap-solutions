# Author:      Wajid Ali Saleem Chaudhry
# Description: CLI tool to display GitHub trending repositories using
#              the Search API sorted by recent star activity.

import sys
import argparse
import requests
from datetime import date, timedelta


# --- Constants ---

BASE_URL = "https://api.github.com/search/repositories"
DURATIONS = ("day", "week", "month", "year")
DURATION_DAYS = {"day": 1, "week": 7, "month": 30, "year": 365}


# --- Date Helpers ---


# Return ISO date string N days before today (YYYY-MM-DD)
def days_ago(n):
    return (date.today() - timedelta(days=n)).isoformat()


# Build the `q` query string for the GitHub Search API
def build_query(since_date):
    return f"created:>{since_date}"


# --- API ---


# Fetch repos created since `since_date`, up to `limit` results.
# Returns a list of item dicts on success, or None on any error.
# Prints a human-readable diagnostic before returning None.
def fetch_repos(since_date, limit):
    params = {
        "q": build_query(since_date),
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10,
            headers={"Accept": "application/vnd.github+json"},
        )
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None

    if response.status_code != 200:
        msg = response.json().get("message", response.reason)
        print(f"API error {response.status_code}: {msg}")
        return None

    return response.json()["items"]


# --- Display ---


# Print a ranked table of repos to stdout.
# repos is the raw items list from fetch_repos.
def display_repos(repos):
    if not repos:
        print("No repositories found.")
        return
    print(f"{'#':<4} {'Repository':<35} {'Stars':>8}  {'Lang':<12}  Description")
    print("-" * 80)
    for i, item in enumerate(repos, start=1):
        name = item["full_name"]
        stars = item["stargazers_count"]
        lang = item["language"] or "N/A"
        desc = (
            (item["description"] or "")[:18]
            .encode("ascii", errors="replace")
            .decode("ascii")
        )
        print(f"{i:<4} {name:<35} {stars:>8,}  {lang:<12}  {desc}")


# --- CLI ---


# Build and return the configured ArgumentParser
def build_parser():
    parser = argparse.ArgumentParser(prog="trending-repos")
    parser.add_argument(
        "--duration",
        choices=DURATIONS,
        default="week",
        help="Time range for trending repos (default: week)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        metavar="N",
        help="Number of repos to display (default: 10)",
    )
    return parser


# Entry point: parse args, compute cutoff date, fetch, display
def main():
    args = build_parser().parse_args()
    if args.limit <= 0:
        print("Error: --limit must be a positive integer.")
        sys.exit(1)
    since = days_ago(DURATION_DAYS[args.duration])
    repos = fetch_repos(since, args.limit)
    if repos is None:
        sys.exit(1)
    display_repos(repos)


if __name__ == "__main__":
    main()
