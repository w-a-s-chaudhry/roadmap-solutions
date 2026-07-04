# Clean CSV

**roadmap.sh project:** https://roadmap.sh/projects/clean-csv

## What it does

Cleans the Kaggle [Messy Employee Dataset](https://www.kaggle.com/datasets/desolution01/messy-employee-dataset)
(`data/Messy_Employee_dataset.csv`, 1,020 rows) using pandas:

- **C2 — Load & Inspect:** loads the raw CSV and audits shape, dtypes,
  nulls (`Age`: 211 missing, `Salary`: 24 missing), and duplicates
  (none found)
- **C3 — Handle Technical Issues:** confirms the file is plain UTF-8
  with a comma delimiter (no encoding/delimiter fixes needed), then
  splits the combined `Department_Region` column (e.g.
  `"DevOps-California"`) into separate `Department` and `Region`
  columns
- **C4 — Fix Data Types:** casts `Age` to nullable `Int64` (preserves
  existing NaNs), `Salary` to `float64`, and `Performance_Score` to an
  ordered category (`Poor` < `Average` < `Good` < `Excellent`);
  `Remote_Work` is already inferred as `bool` by `read_csv`
- **C5 — Convert Dates:** parses `Join_Date` with
  `pd.to_datetime(format="%m/%d/%Y", errors="coerce")`
- **C6 — Standardize Categories:** strips whitespace and checks
  `Status`/`Department`/`Region` for case inconsistencies (none found,
  so no destructive `.str.title()` rewrite is applied — abbreviations
  like `DevOps` and `HR` are left intact)
- **C7 — Export & Audit:** re-checks dtypes/nulls and writes the
  cleaned dataframe to `data/employees_cleaned.csv` (1,020 rows, 13
  columns)

## Setup

```bash
uv sync
uv run jupyter notebook clean_csv.ipynb
```
