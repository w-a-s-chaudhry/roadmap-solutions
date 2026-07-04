# Data Visualization Tutorial

A Jupyter notebook that builds five chart types — histogram, bar,
box, scatter, and heatmap — side-by-side in both Matplotlib and
Seaborn, then exports a chart as a PNG.

**roadmap.sh project:**
https://roadmap.sh/projects/data-visualization-tutorial

---

## Dataset

**Tips** — loaded directly from Seaborn via `sns.load_dataset("tips")`.
No download required. 244 restaurant bill records with columns
`total_bill`, `tip`, `sex`, `smoker`, `day`, `time`, `size`.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "data-visualization-tutorial" \
    --display-name "Python (data-visualization-tutorial)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `data_visualization.ipynb` and select the
**Python (data-visualization-tutorial)** kernel.

---

## Charts

| Cell | Chart type | Key insight |
|------|------------|-------------|
| C2 | Histogram | `total_bill` is right-skewed; most bills fall $10–$20 |
| C3 | Bar | Saturday sees the highest average tips |
| C4 | Box | Sunday has the widest tip spread; outliers on all days |
| C5 | Scatter | Positive correlation between `total_bill` and `tip` |
| C6 | Heatmap | `total_bill` ↔ `tip` strongest correlation (r ≈ 0.68) |
| C7 | Export | Heatmap saved to `outputs/heatmap.png` |
