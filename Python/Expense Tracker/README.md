# Expense Tracker

A simple CLI to track expenses, with categories, monthly budgets, and CSV
export. State is persisted to `expenses.json` in the current working
directory.

Solution to the [Expense Tracker](https://roadmap.sh/projects/expense-tracker)
project from roadmap.sh.

## Install

This project uses [uv](https://docs.astral.sh/uv/). From this directory:

```bash
uv tool install .
```

That builds the package and exposes the `expense-cli` command on your PATH.
For local development without installing globally, use `uv run expense-cli`
from this directory instead.

## Usage

```bash
expense-cli add --description "lunch" --amount 12.50 --category food
expense-cli add --description "uber" --amount 8 --category transport
expense-cli add --description "movie" --amount 15

expense-cli list                         # all expenses
expense-cli list --category food         # filter by category

expense-cli update <id> --amount 9.75 --description "uber pool"
expense-cli delete <id>

expense-cli summary                      # total across all expenses
expense-cli summary --month 5            # total for May (current year)

expense-cli budget --month 5 --amount 200
expense-cli export                       # writes expenses.csv

expense-cli help
```

`expenses.json` is created in the current working directory on first use.
`expenses.csv` is written there by `export`.

## Categories

`food`, `transport`, `housing`, `entertainment`, `health`, `shopping`,
`other`. Defaults to `other` when `--category` is omitted on `add`.

## Budgets

`budget --month <1-12> --amount <num>` sets a monthly cap (current year
implied). When `add` pushes that month's total over the cap, the CLI
prints a warning showing the overage but still records the expense.
