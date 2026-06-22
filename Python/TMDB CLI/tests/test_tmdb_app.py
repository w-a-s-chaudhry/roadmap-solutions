# Author:      Wajid Ali Saleem Chaudhry
# Description: Tests for tmdb_app: parser, token reading, fetch, and
#              display output. Network is mocked — no token needed.

import pytest
import requests
from unittest.mock import patch
from tmdb_app import (
    get_token,
    fetch_movies,
    display_movies,
    build_parser,
    TOKEN_ENV,
)


# --- Parser ---


# Default --type is "popular" when no args are given.
def test_parser_default():
    args = build_parser().parse_args([])
    assert args.type == "popular"


# --type top is parsed and stored on args.type.
def test_parser_type_top():
    args = build_parser().parse_args(["--type", "top"])
    assert args.type == "top"


# An invalid --type makes argparse exit (not return).
def test_parser_invalid_raises():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--type", "bogus"])


# --- Auth ---


# get_token returns the token when the env var is set.
def test_get_token_set(monkeypatch):
    monkeypatch.setenv(TOKEN_ENV, "abc123")
    assert get_token() == "abc123"


# get_token returns None when the env var is unset.
def test_get_token_unset(monkeypatch):
    monkeypatch.delenv(TOKEN_ENV, raising=False)
    assert get_token() is None


# --- Fetch ---


# On a 200 response, fetch_movies returns the results list.
@patch("tmdb_app.requests.get")
def test_fetch_movies_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"title": "X"}]}
    result = fetch_movies("popular", "tok")
    assert result == [{"title": "X"}]


# On a network error, fetch_movies returns None.
@patch("tmdb_app.requests.get")
def test_fetch_movies_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("boom")
    assert fetch_movies("popular", "tok") is None


# On a non-200 response, fetch_movies returns None.
@patch("tmdb_app.requests.get")
def test_fetch_movies_non_200(mock_get):
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"status_message": "bad"}
    assert fetch_movies("popular", "tok") is None


# --- Display ---


# Empty list prints the "not found" message.
def test_display_movies_empty(capsys):
    display_movies([])
    captured = capsys.readouterr()
    assert "No movies found." in captured.out


# Header row and separator appear in the output.
def test_display_movies_header(capsys):
    fake = [
        {
            "title": "Inception",
            "release_date": "2010-07-16",
            "vote_average": 7.5,
            "overview": "A thief who steals corporate secrets...",
        }
    ]
    display_movies(fake)
    captured = capsys.readouterr()
    assert "Title" in captured.out
    assert "-" * 80 in captured.out


# Movie data appears correctly in the row output.
def test_display_movies_row(capsys):
    fake = [
        {
            "title": "Inception",
            "release_date": "2010-07-16",
            "vote_average": 7.5,
            "overview": "A thief who steals corporate secrets...",
        }
    ]
    display_movies(fake)
    captured = capsys.readouterr()
    assert "Inception" in captured.out
    assert "7.5" in captured.out
