# Exploring the Iris Dataset

A Jupyter notebook exploratory data analysis of the classic Iris
flower dataset, using pandas, matplotlib, and seaborn.

**roadmap.sh project:**
https://roadmap.sh/projects/exploring-iris-dataset

---

## Overview

The notebook investigates which features best distinguish the three
Iris species (*setosa*, *versicolor*, *virginica*):

- **1** — Setup & load data
- **2** — Class balance (species counts)
- **3** — Univariate distributions: histograms & box plots per feature
- **4** — Pairplot across all features, colored by species
- **5** — Correlation matrix as a heatmap
- **6** — Summary of findings

---

## Dataset

Source: the built-in copy bundled with Seaborn
(`sns.load_dataset("iris")`) — no download or account required.

**Columns:** `sepal_length`, `sepal_width`, `petal_length`,
`petal_width`, `species`.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "exploring-iris-dataset" \
    --display-name "Python (exploring-iris-dataset)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `iris_exploration.ipynb` and select the
**Python (exploring-iris-dataset)** kernel.

---

## Findings

- The dataset is perfectly balanced: 50 rows for each of *setosa*,
  *versicolor*, and *virginica*.
- **Petal measurements** (`petal_length`, `petal_width`) separate the
  species far better than sepal measurements. *setosa* is almost
  perfectly linearly separable from the other two on petal features
  alone.
- *versicolor* and *virginica* overlap more but remain distinguishable
  by petal length/width, with *virginica* skewing larger.
- `sepal_width` is the weakest predictor and the only feature
  negatively correlated with the rest (-0.12 to -0.43).
- `petal_length` and `petal_width` are almost perfectly correlated
  (0.96), so one could largely substitute for the other in a
  simplified model.
