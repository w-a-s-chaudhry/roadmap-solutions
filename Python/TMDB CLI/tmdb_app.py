# Author:      Wajid Ali Saleem Chaudhry
# Description: CLI tool to display movies from the TMDB API by category
#              (now playing, popular, top rated, upcoming).

import os
import sys
import argparse
import requests
from dotenv import load_dotenv


# --- Environment ---

# Load key=value pairs from a local .env file into the process
# environment, so os.environ.get below can read TMDB_ACCESS_TOKEN.
# Does nothing if .env is absent, so a real env var (CI) still works.
load_dotenv()


# --- Constants ---

BASE_URL = "https://api.themoviedb.org/3"
TOKEN_ENV = "TMDB_ACCESS_TOKEN"
TYPES = ("playing", "popular", "top", "upcoming")
TYPE_ENDPOINTS = {
    "playing": "/movie/now_playing",
    "popular": "/movie/popular",
    "top": "/movie/top_rated",
    "upcoming": "/movie/upcoming",
}


# --- Auth ---


# Read the TMDB read access token from the environment.
# Return the token string, or None (after a diagnostic) if it is unset.
def get_token():
    token = os.environ.get(TOKEN_ENV)
    if token is not None:
        return token
    print(f"Error: {TOKEN_ENV} not set")


# --- API ---


# Fetch movies for the given type using the bearer token.
# Returns a list of result dicts on success, or None on any error.
# Prints a human-readable diagnostic before returning None.
def fetch_movies(movie_type, token):
    url = BASE_URL + TYPE_ENDPOINTS[movie_type]

    try:
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
            },
            timeout=10,
        )

    except requests.RequestException as e:
        print(f"Network Error: {e}")
        return None

    if response.status_code != 200:
        msg = response.json().get("status_message", response.reason)
        print(f"API error {response.status_code}: {msg}")
        return None

    return response.json()["results"]


# --- Display ---


# Print a ranked table of movies to stdout.
# movies is the raw results list from fetch_movies.
def display_movies(movies):
    if not movies:
        print("No movies found.")
        return
    print(f"{'#':<4} {'Title':<35} {'Released':<12}  {'Rating':>6}  Overview")
    print("-" * 80)
    for i, movie in enumerate(movies, start=1):
        title = movie["title"]
        released = movie["release_date"]
        rating = movie["vote_average"]
        overview = (
            (movie["overview"] or "")[:18]
            .encode("ascii", errors="replace")
            .decode("ascii")
        )
        print(f"{i:<4} {title:<35} {released:<12}  {rating:>6.1f}  {overview}")


# --- CLI ---


# Build and return the configured ArgumentParser
def build_parser():
    parser = argparse.ArgumentParser(prog="tmdb-app")
    parser.add_argument("--type", choices=TYPES, default="popular")
    return parser


# Entry point: parse args, read token, fetch, display
def main():
    args = build_parser().parse_args()
    token = get_token()
    if token is None:
        sys.exit(1)
    movies = fetch_movies(args.type, token)
    if movies is None:
        sys.exit(1)
    display_movies(movies)


if __name__ == "__main__":
    main()
