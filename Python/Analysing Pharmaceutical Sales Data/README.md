# Analysing Pharmaceutical Sales Data

A Jupyter notebook data analysis of daily pharmaceutical sales across
eight ATC drug categories, using pandas and matplotlib.

**roadmap.sh project:**
https://roadmap.sh/projects/pharmaceutical-sales-data

---

## Overview

The notebook answers six analytical questions about a historical
pharmaceutical sales dataset spanning 2014–2019. Each question is
presented with the pandas code that answers it, a chart where relevant,
and a short findings sentence.

---

## Dataset

Source: Kaggle — [milanzdravkovic/pharma-sales-data](
https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data)

Download `salesdaily.csv` and place it at:

```
data/salesdaily.csv
```

The file is gitignored and must be downloaded manually (Kaggle account
required).

**Columns:** `datum` (date), eight ATC category columns
(`M01AB`, `M01AE`, `N02BA`, `N02BE`, `N05B`, `N05C`, `R03`, `R06`),
plus `Year`, `Month`, `Hour`, `Weekday Name`.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "pharma-sales" \
    --display-name "Python (pharma-sales)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `pharma_sales.ipynb` and select the **Python (pharma-sales)**
kernel.

---

## Findings

1. **Total sales by category** — N02BE dominates with 63,005 total
   units; N05C is the lowest at 1,249.

2. **Highest-selling category** — **N02BE** (analgesics/antipyretics —
   pyrazolones & anilides).

3. **Top 3 by month** — N02BE topped all three target months. Second
   and third: Jan 2015 → N05B, R03; Jul 2016 → N05B, M01AB;
   Sep 2017 → N05B, R03.

4. **Most sold drug in 2017** — **N02BE**.

5. **Highest average daily sales** — **N02BE** (~29.9 units/day, over
   three times the next category N05B at ~8.9 units/day).

6. **R03 seasonal pattern** — respiratory drug sales peak in winter
   (December highest at ~7.9 units/day) and dip sharply in summer
   (July lowest at ~3.0 units/day), reflecting cold-weather demand.
