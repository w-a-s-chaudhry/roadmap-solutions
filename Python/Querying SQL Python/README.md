# Querying SQL Python

A Jupyter notebook that connects to the Chinook SQLite database via
Python's built-in `sqlite3` library, runs three business-focused SQL
queries, and loads the results into Pandas DataFrames with a
Matplotlib visualisation.

**roadmap.sh project:**
https://roadmap.sh/projects/querying-sql-python

---

## Database

**Chinook** — a sample database modelling a digital music store.

Included in this repo as `Chinook_Sqlite.sqlite` (v1.4.5,
[lerocha/chinook-database](https://github.com/lerocha/chinook-database)).

Key tables used: `Track`, `Album`, `Artist`, `InvoiceLine`,
`Invoice`, `Customer`, `Employee`.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Register the Jupyter kernel (one-time):

```bash
uv run python -m ipykernel install --user \
    --name "querying-sql-python" \
    --display-name "Python (querying-sql-python)"
```

---

## Running the notebook

```bash
uv run jupyter lab
```

Open `querying_sql_python.ipynb` and select the
**Python (querying-sql-python)** kernel.

---

## Queries

| # | Question | Key SQL |
|---|---|---|
| 1 | Top 10 best-selling tracks | `JOIN InvoiceLine … GROUP BY TrackId ORDER BY SUM(Quantity) DESC` |
| 2 | Top 10 countries by revenue | `GROUP BY BillingCountry ORDER BY SUM(Total) DESC` |
| 3 | Top-performing sales employee | `JOIN Customer … JOIN Invoice … GROUP BY EmployeeId` |

---

## Findings

1. **Best-selling tracks** — Multiple tracks tied at 2 units sold;
   "Balls to the Wall" (Accept) and several AC/DC tracks lead the list.

2. **Top revenue country** — **USA**, generating ~$523 across all
   invoices, followed by Canada (~$304) and France (~$195).

3. **Top sales employee** — **Jane Peacock** with $833.04 in total
   sales across 21 customers, ahead of Margaret Park ($775.40) and
   Steve Johnson ($720.16).
