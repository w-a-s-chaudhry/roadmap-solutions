# Author:      Wajid Ali Saleem Chaudhry
# Description: Fetch a GitHub user's recent public activity from the
#              events API and print a human-readable summary.

import requests
import sys

# --- Event Type Labels ---

# Maps GitHub event types to the phrase used in the output line.
# PushEvent is handled separately so we can print the commit count.
EVENT_TYPES = {
    "PullRequestEvent":        "opened/closed PRs",
    "IssuesEvent":             "opened/closed issues",
    "IssueCommentEvent":       "commented on issues",
    "CreateEvent":             "created branch/tag/repo",
    "DeleteEvent":             "deleted branch/tag",
    "ForkEvent":               "forked a repo",
    "WatchEvent":              "starred a repo",
    "ReleaseEvent":            "published a release",
    "PullRequestReviewEvent":  "reviewed a PR",
}

# --- API ---

# Fetch user's public events; prints diagnostic and returns None on error
def get_user_events(username):
  url = f"https://api.github.com/users/{username}/events"
  try:
    r = requests.get(url, timeout=10)
  except requests.RequestException as e:
    # Connection refused, DNS failure, timeout, etc.
    print(f"Network error: {e}")
    return None
  if r.status_code == 404:
    print(f"Username Error: {username} not found")
    return None
  if r.status_code != 200:
    # GitHub puts a human message in the JSON body (e.g. rate limit
    # text); fall back to the HTTP reason phrase if the body isn't JSON
    try:
      msg = r.json().get("message", r.reason)
    except ValueError:
      msg = r.reason
    print(f"API error {r.status_code}: {msg}")
    return None
  try:
    return r.json()
  except ValueError:
    print("API error: response was not valid JSON")
    return None

# --- Output ---

# Print events, collapsing consecutive runs of the same type+repo
def output_events(events):
  print("Output:")
  i = 0
  while i < len(events):
    # Walk j forward over the run of matching events; count = j - i
    j = i + 1
    while (j < len(events)
           and events[j]["type"] == events[i]["type"]
           and events[j]["repo"]["id"] == events[i]["repo"]["id"]):
      j += 1
    count = j - i
    repo = events[i]["repo"]["name"]
    etype = events[i]["type"]
    if etype == "PushEvent":
      print(f"pushed {count} commit(s) to {repo}")
    else:
      # Unknown event types fall back to the raw API name
      label = EVENT_TYPES.get(etype, etype)
      print(f"{label} repo: {repo}")
    i = j
  return

# --- CLI ---

# Entry point: parse argv, fetch events for the given user, print summary
def main():
  args = sys.argv[1:]

  # Require exactly the username argument
  if not args:
    print("Usage: github-activity <username>")
    return

  username = args[0]

  events = get_user_events(username)
  if events is None:
    return

  output_events(events)

if __name__ == "__main__":
  main()