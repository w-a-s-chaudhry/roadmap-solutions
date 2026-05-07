# GitHub User Activity

A simple CLI that fetches a GitHub user's recent public activity from the
events API and prints a human-readable summary. Consecutive events of the
same type on the same repo are collapsed into a single line.

Solution to the [GitHub User Activity](https://roadmap.sh/projects/github-user-activity)
project from roadmap.sh.

## Install

From this directory:

```bash
pip install -e .
```

This installs the `requests` dependency and exposes the `github-activity`
command on your PATH.

## Usage

```bash
github-activity <username>
```

Example:

```bash
github-activity kamranahmedse
```

Sample output:

```
Output:
pushed 3 commit(s) to kamranahmedse/developer-roadmap
opened/closed PRs repo: kamranahmedse/developer-roadmap
starred a repo repo: some-user/some-repo
```

## Errors

The CLI prints a diagnostic and exits cleanly for the common failure modes:

- **Invalid username** — `Username Error: <name> not found` (HTTP 404).
- **Rate limited or other API error** — `API error <code>: <message>`,
  using GitHub's `message` field when present.
- **Network failure** — `Network error: <details>` (DNS, refused
  connection, timeout, etc.). Requests time out after 10 seconds.

## Notes

- No external dependencies beyond `requests`.
- Uses the unauthenticated GitHub events endpoint, which is rate-limited
  to 60 requests per hour per IP.
