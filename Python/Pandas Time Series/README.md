# Pandas Time Series

A Jupyter notebook that pulls U.S. light vehicle sales data directly
from FRED (`ALTSALES`) and applies core Pandas time series tools —
`DatetimeIndex`, `pd.date_range`, `.resample()`, `.shift()`,
`.diff()`, and `.rolling()` — to study monthly and quarterly trends
from 1976 through mid-2026.

**roadmap.sh project:**
https://roadmap.sh/projects/pandas-time-series

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "pandas-time-series" \
    --display-name "Python (pandas-time-series)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `pandas_time_series.ipynb` and select the
**Python (pandas-time-series)** kernel.

---

## Analysis

| Section | Topic | Detail |
|---|---|---|
| Load data | Data acquisition | `pd.read_csv` from the FRED CSV endpoint — 606 monthly rows, 1976-01 → 2026-06 |
| Date processing | `DatetimeIndex` | `observation_date` parsed and set as index |
| Date range creation | `pd.date_range` | Month-start range confirms zero missing months |
| Resampling | `.resample()` | Monthly (no-op, 606 rows) and quarterly mean (202 rows) |
| Time shift | `.shift()` / `.diff()` | Prior-month value, absolute and % month-over-month change |
| Visualization | `.rolling()` | Monthly series vs. 12-month rolling mean |

---

## Findings

- The series is a clean monthly `DatetimeIndex` with no gaps against
  `pd.date_range(freq="MS")`, so no reindexing/filling was needed
  before resampling.
- Quarterly resampling smooths the sharp month-to-month swings
  visible in the raw series, making longer cycles easier to read.
- Month-over-month `%` change is highly volatile and noisy — useful
  for spotting shocks (e.g. the 2020 COVID collapse, visible as an
  ~8.6M-unit trough) but not for reading the underlying trend on its
  own.
- The 12-month rolling mean is the clearest way to see the trend: it
  removes seasonal noise and confirms why differencing/rolling
  matters before comparing periods in sales data — the raw series
  alone obscures the 1980, 1991, 2001, 2008–09, and 2020 downturns
  that the rolling mean makes obvious.
