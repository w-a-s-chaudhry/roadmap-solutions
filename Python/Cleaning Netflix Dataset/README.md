# Cleaning Netflix Dataset

**roadmap.sh project:** https://roadmap.sh/projects/cleaning-netflix-dataset

## What it does

Cleans the Kaggle Netflix Movies and TV Shows dataset
(`data/netflix_titles.csv`) using pandas:

- **C2 — Missing values:** fills `director`/`cast` with `"Unknown"`,
  `country`/`rating` with their mode; drops the handful of rows
  missing `date_added` or `duration`
- **C3 — Data types:** splits `duration` into `duration_value` (int)
  and `duration_unit` (str); converts `date_added` to `datetime64`
- **C4 — Export:** writes the cleaned dataframe to
  `data/netflix_titles_cleaned.csv` (8 794 rows, 14 columns)

## Setup

```bash
uv sync
uv run jupyter notebook cleaning_netflix.ipynb
```
