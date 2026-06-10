# Author:      Wajid Ali Saleem Chaudhry
# Description: Tests for trending_repos: date helpers, parser,
#              fetch, and display output.

import requests
from datetime import date, timedelta
from unittest.mock import patch
from trending_repos import (
    days_ago,
    build_query,
    build_parser,
    fetch_repos,
    display_repos,
)


# --- Date Helpers ---


# days_ago(n) should return a string in YYYY-MM-DD format
def test_days_ago_format():
    result = days_ago(7)
    assert len(result) == 10
    assert result[4] == "-"
    assert result[7] == "-"


# days_ago(n) should return the correct date relative to today
def test_days_ago_value():
    expected = (date.today() - timedelta(days=7)).isoformat()
    assert days_ago(7) == expected


# build_query should embed the date in the GitHub search format
def test_build_query_format():
    assert build_query("2025-01-01") == "created:>2025-01-01"


# --- Parser ---


# default duration is "week", default limit is 10
def test_parser_defaults():
    args = build_parser().parse_args([])
    assert args.duration == "week"
    assert args.limit == 10


# --duration accepts valid choices and stores the value
def test_parser_duration():
    args = build_parser().parse_args(["--duration", "day"])
    assert args.duration == "day"


# --limit converts the string argument to an int
def test_parser_limit():
    args = build_parser().parse_args(["--limit", "5"])
    assert args.limit == 5


# --- Fetch ---


# On a 200 response, fetch_repos returns the items list
@patch("trending_repos.requests.get")
def test_fetch_repos_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"items": [{"full_name": "a/b"}]}
    result = fetch_repos("2025-01-01", 1)
    assert result == [{"full_name": "a/b"}]


# On a network error, fetch_repos returns None
@patch("trending_repos.requests.get")
def test_fetch_repos_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("boom")
    result = fetch_repos("2025-01-01", 1)
    assert result is None


# --- Display ---


# Empty list prints the "not found" message
def test_display_repos_empty(capsys):
    display_repos([])
    captured = capsys.readouterr()
    assert "No repositories found." in captured.out


# Header row and separator appear in output
def test_display_repos_header(capsys):
    fake = [
        {
            "full_name": "owner/repo",
            "stargazers_count": 100,
            "language": "Python",
            "description": "A test repo",
        }
    ]
    display_repos(fake)
    captured = capsys.readouterr()
    assert "Repository" in captured.out
    assert "-" * 80 in captured.out


# Repo data appears correctly in the row output
def test_display_repos_row(capsys):
    fake = [
        {
            "full_name": "owner/repo",
            "stargazers_count": 1234,
            "language": "Python",
            "description": "A test repo",
        }
    ]
    display_repos(fake)
    captured = capsys.readouterr()
    assert "owner/repo" in captured.out
    assert "1,234" in captured.out
    assert "Python" in captured.out
