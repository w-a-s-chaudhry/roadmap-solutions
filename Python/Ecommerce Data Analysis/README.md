# E-Commerce Data Analysis

A Jupyter notebook that cleans a 10% sample of the UCI Online Retail
dataset (~540K UK online-retailer transactions) with pandas, computes
per-line revenue, and visualizes the top 10 countries by total
revenue with seaborn.

**roadmap.sh project:**
https://roadmap.sh/projects/ecommerce-data-analysis

---

## Dataset

Source: [UCI Machine Learning Repository — Online Retail](
https://archive.ics.uci.edu/ml/datasets/online+retail)

Download the file and place it at:

```
data/online_retail.xlsx
```

The file is gitignored (23 MB) and downloads directly with no
account required:

```bash
curl -L -o data/online_retail.xlsx \
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
```

**Columns:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`,
`InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "ecommerce-data-analysis" \
    --display-name "Python (ecommerce-data-analysis)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `ecommerce_data_analysis.ipynb` and select the
**Python (ecommerce-data-analysis)** kernel.

---

## Analysis

| Step | Detail |
|------|--------|
| Sampling | 10% of 541,909 rows -> 54,191 rows (seed 42) |
| Cleaning | Dropped null `CustomerID`/`Description`; removed returns (`InvoiceNo` starting with `C`) and non-positive `Quantity`/`UnitPrice` -> 39,635 rows |
| Revenue | `Revenue = Quantity * UnitPrice`, computed per order line |
| Top countries | Grouped by `Country`, summed `Revenue`, took the top 10 |
| Visualization | Horizontal bar chart, `outputs/top_10_countries_revenue.png` |

---

## Findings

| Rank | Country | Total Revenue |
|------|---------|---------------:|
| 1 | United Kingdom | 768,682.56 |
| 2 | Netherlands | 27,435.83 |
| 3 | EIRE | 24,340.42 |
| 4 | France | 23,606.73 |
| 5 | Germany | 22,389.51 |
| 6 | Australia | 12,429.99 |
| 7 | Spain | 5,600.90 |
| 8 | Switzerland | 5,383.19 |
| 9 | Belgium | 3,593.51 |
| 10 | Portugal | 3,244.31 |

The United Kingdom dominates total revenue by more than 25x the
next-highest country, reflecting the retailer's home market. The rest
of the top 10 are neighboring European markets (Netherlands, EIRE,
France, Germany), the retailer's primary export destinations.
