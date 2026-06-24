# Author:      Wajid Ali Saleem Chaudhry
# Description: Tests for job_scraper: fetch_page (mocked network),
#              parse_jobs (inline HTML), and save_csv (tmp_path round-trip).

import csv
from unittest.mock import patch

import job_scraper


# --- Sample HTML ---

# A tiny stand-in for the real page: two complete cards. parse_jobs
# should turn this into two dicts. Mirrors the real markup the C1
# selectors target:
#   div.card-content > h2.title, h3.company, p.location, footer a (href)
SAMPLE_HTML = """
<div class="card-content">
    <h2 class="title">Senior Python Dev</h2>
    <h3 class="company">Acme Corp</h3>
    <p class="location">Remote</p>
    <footer>
        <a href="https://example.com/learn">Learn</a>
        <a href="jobs/senior-python-dev.html">Apply</a>
    </footer>
</div>
<div class="card-content">
    <h2 class="title">Junior Dev</h2>
    <h3 class="company">Kainos</h3>
    <p class="location">Remote</p>
    <footer>
        <a href="https://example.com/learn">Learn</a>
        <a href="jobs/junior-dev.html">Apply</a>
    </footer>
</div>
"""

# Like SAMPLE_HTML but ONE card with a field missing (no h3.company)
# so the "" fallback path is exercised.
MISSING_FIELD_HTML = """
<div class="card-content">
    <h2 class="title">Senior Web Dev</h2>
    <p class="location">Remote</p>
    <footer>
        <a href="https://example.com/learn">Learn</a>
        <a href="jobs/senior-web-dev.html">Apply</a>
    </footer>
</div>
"""


# --- fetch_page ---


# A 200 response: fetch_page should return the response body text.
# The @patch swaps job_scraper.requests.get for a fake (mock_get) for
# the duration of this test. Configure what the fake call returns, then
# assert.
@patch("job_scraper.requests.get")
def test_fetch_page_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html>hi</html>"
    result = job_scraper.fetch_page("http://x")
    assert result == "<html>hi</html>"


# A non-200 response (e.g. 404): fetch_page should return None.
@patch("job_scraper.requests.get")
def test_fetch_page_non_200(mock_get):
    mock_get.return_value.status_code = 404
    result = job_scraper.fetch_page("http://x")
    assert result is None


# A network failure: requests.get raises RequestException -> None.
# Use mock_get.side_effect to make the fake raise instead of return.
@patch("job_scraper.requests.get")
def test_fetch_page_request_exception(mock_get):
    mock_get.side_effect = job_scraper.requests.RequestException("boom")
    result = job_scraper.fetch_page("http://x")
    assert result is None


# --- parse_jobs ---


# Two well-formed cards -> a list of two dicts with all four fields.
def test_parse_jobs_basic():
    jobs = job_scraper.parse_jobs(SAMPLE_HTML)
    assert len(jobs) == 2
    assert jobs[0]["title"] == "Senior Python Dev"
    assert jobs[0]["company"] == "Acme Corp"
    assert jobs[0]["location"] == "Remote"
    assert jobs[0]["url"] == "jobs/senior-python-dev.html"


# A card missing one field -> that key falls back to "", no crash.
def test_parse_jobs_missing_field():
    jobs = job_scraper.parse_jobs(MISSING_FIELD_HTML)
    assert jobs[0]["company"] == ""
    assert jobs[0]["title"] == "Senior Web Dev"
    assert jobs[0]["url"] == "jobs/senior-web-dev.html"


# --- save_csv ---


# Round-trip: write jobs to a file under tmp_path, read it back with
# csv.DictReader, and assert header + rows survive intact.
def test_save_csv(tmp_path):
    jobs = [
        {
            "title": "Dev",
            "company": "Acme",
            "location": "Remote",
            "url": "http://x/1",
        },
    ]
    path = tmp_path / "jobs.csv"
    job_scraper.save_csv(jobs, path)
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames == job_scraper.FIELDS
        rows = list(reader)
        assert rows == jobs
