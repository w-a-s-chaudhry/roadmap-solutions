# Author:      Wajid Ali Saleem Chaudhry
# Description: Scrape job postings from the Real Python "Fake Jobs"
#              practice site and write them to a CSV file.

import csv
import requests
from bs4 import BeautifulSoup


# --- Constants ---

URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_CSV = "jobs.csv"
FIELDS = ["title", "company", "location", "url"]


# --- Fetch ---


# GET the page at url; on a network error or non-200 status, print a
# diagnostic and return None. Otherwise return the response body text.
def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        return response.text
    except requests.RequestException as e:
        print(f"Network Error: {e}")
        return None


# --- Parse ---


# Parse the listings HTML with BeautifulSoup and return a list of dicts,
# one per posting, each with the keys in FIELDS. Missing fields fall
# back to "" so a malformed card never crashes the scrape.
def parse_jobs(html):
    jobs = []
    soup = BeautifulSoup(html, "html.parser")
    for card in soup.select("div.card-content"):
        title_el = card.select_one("h2.title")
        title = title_el.get_text(strip=True) if title_el else ""
        company_el = card.select_one("h3.company")
        company = company_el.get_text(strip=True) if company_el else ""
        location_el = card.select_one("p.location")
        location = location_el.get_text(strip=True) if location_el else ""
        anchors = card.select("footer a")
        url = anchors[-1]["href"] if anchors else ""
        job = {
            "title": title,
            "company": company,
            "location": location,
            "url": url,
        }
        jobs.append(job)
    return jobs


# --- Save ---


# Write jobs (a list of dicts keyed by FIELDS) to a CSV file at path,
# with a header row followed by one row per posting.
def save_csv(jobs, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(jobs)


# --- Entry point ---


# Fetch the fixed URL, parse the postings, save them, and print a
# one-line summary of how many rows were written.
def main():
    html = fetch_page(URL)
    if html is None:
        return
    jobs = parse_jobs(html)
    save_csv(jobs, OUTPUT_CSV)
    print(f"Wrote {len(jobs)} jobs to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
