# Stock Price Time Series

A Jupyter notebook that downloads three years of historical stock
data for Apple (AAPL) and Microsoft (MSFT) via `yfinance`, then
applies Pandas time series techniques — date indexing, resampling,
and rolling moving averages — to compare their performance over
2022–2024.

**roadmap.sh project:**
https://roadmap.sh/projects/stock-price-time-series

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "stock-price-time-series" \
    --display-name "Python (stock-price-time-series)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `stock_price_time_series.ipynb` and select the
**Python (stock-price-time-series)** kernel.

---

## Analysis

| Cell | Topic | Detail |
|------|-------|--------|
| C04 | Data acquisition | `yf.download` — 752 trading days, 2022-01-03 → 2024-12-30 |
| C06 | Data preparation | `DatetimeIndex` confirmed; `Close` and `Volume` sliced |
| C08 | Closing prices | Line chart — AAPL vs MSFT daily adjusted close |
| C10 | Resampling | Weekly (157 rows) and monthly (36 rows) mean close |
| C12 | Moving averages | 20-day & 200-day rolling mean per ticker |
| C14 | Volume comparison | Daily shares traded — AAPL vs MSFT |

---

## Findings

| Metric | AAPL | MSFT |
|--------|------|------|
| Period return (2022–2024) | +40.8% | +30.2% |
| Max closing price | $257.38 | $460.33 |
| Avg daily volume | 68.1M shares | 26.5M shares |

AAPL outperformed MSFT on total return over the period and trades
roughly 2.6× more shares per day, reflecting its larger retail
investor base.
