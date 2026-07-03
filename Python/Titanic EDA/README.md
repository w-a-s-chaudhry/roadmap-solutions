# Titanic EDA

A Jupyter notebook exploratory data analysis of survival patterns from
the Kaggle Titanic dataset, using pandas, matplotlib, and seaborn.

**roadmap.sh project:**
https://roadmap.sh/projects/titanic-eda-python

---

## Overview

The notebook investigates which passenger groups were most likely to
survive the Titanic disaster. Each analysis dimension is presented with
pandas code, a chart, and a short written interpretation.

- **C1** — Setup & initial exploration (shape, dtypes, missing values)
- **C2** — Survival by gender
- **C3** — Survival by passenger class
- **C4** — Age distribution histogram + survival rate by age group
- **C5** — Summary of key findings

---

## Dataset

Source: Kaggle — [Titanic: Machine Learning from Disaster](
https://www.kaggle.com/c/titanic/data)

Download `train.csv` and place it at:

```
data/train.csv
```

The file is gitignored and must be downloaded manually (Kaggle account
required).

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "titanic-eda" \
    --display-name "Python (titanic-eda)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `titanic_eda.ipynb` and select the **Python (titanic-eda)** kernel.

---

## Findings

- **Gender** was the strongest predictor: females survived at 74.2%
  vs 18.9% for males — nearly 4x higher.
- **Passenger class** showed a clear gradient: 1st (63.0%),
  2nd (47.3%), 3rd (24.2%), reflecting wealth and deck proximity to
  lifeboats.
- **Age** followed evacuation priority: children 0–12 (58.0%) fared
  best, seniors 60+ (26.9%) fared worst.
- **Relative frequencies were essential** — raw counts mislead because
  cohort sizes differ significantly across all three dimensions.
