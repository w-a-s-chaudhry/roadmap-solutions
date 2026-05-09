# Author:      Wajid Ali Saleem Chaudhry
# Description: roadmap.sh Expense Tracker CLI — add/update/delete/list
#              expenses, monthly summaries, per-month budgets, and CSV
#              export. State persists to expenses.json in the cwd.

import sys
import json
import os
import csv
from datetime import datetime

DATA_FILE = "expenses.json"
CSV_FILE = "expenses.csv"
CATEGORIES = ["food", "transport", "housing", "entertainment",
              "health", "shopping", "other"]

COMMANDS = {
  "add": "--description <text> --amount <num> [--category <cat>]",
  "list": "[--category <cat>]",
  "update": "<id> [--description <text>] [--amount <num>] [--category <cat>]",
  "delete": "<id>",
  "summary": "[--month <1-12>]",
  "budget": "--month <1-12> --amount <num>",
  "export": "",
  "help": ""
}

# In-memory store; loaded from disk by load(), persisted by save()
data = {"expenses": [], "budgets": {}}


# --- Persistence ---

# Persist the in-memory store to expenses.json (overwrite)
def save():
  with open(DATA_FILE, 'w') as f:
    json.dump(data, f, indent=2)

# Load expenses.json into the in-memory store, creating it if absent
def load():
  global data
  if not os.path.exists(DATA_FILE):
    save()
    return
  with open(DATA_FILE, 'r') as f:
    data = json.load(f)
  # Backfill missing top-level keys for older data files
  data.setdefault("expenses", [])
  data.setdefault("budgets", {})


# --- Argument parsing ---

# Parse ["--key", "value", ...] into {"key": "value"}; (kwargs, err) tuple
def parse_flags(tokens):
  kwargs = {}
  i = 0
  while i < len(tokens):
    tok = tokens[i]
    if not tok.startswith("--"):
      return None, f"Expected --flag, got '{tok}'"
    if i + 1 >= len(tokens):
      return None, f"Missing value for {tok}"
    kwargs[tok[2:]] = tokens[i + 1]
    i += 2
  return kwargs, None

# Convert raw amount string to a positive float; returns None on failure
def parse_amount(s):
  try:
    val = float(s)
  except (TypeError, ValueError):
    print(f"Invalid amount: {s}")
    return None
  if val <= 0:
    print(f"Amount must be positive: {s}")
    return None
  return round(val, 2)

# Convert raw month string to int in [1, 12]; returns None on failure
def parse_month(s):
  try:
    m = int(s)
  except (TypeError, ValueError):
    print(f"Invalid month: {s}")
    return None
  if m < 1 or m > 12:
    print(f"Month must be 1-12: {s}")
    return None
  return m

# Validate category against the allowed list; returns None on failure
def parse_category(s):
  c = s.lower()
  if c not in CATEGORIES:
    print(f"Invalid category: {s}. "
          f"Valid: {', '.join(CATEGORIES)}")
    return None
  return c


# --- Lookup ---

# Find expense by id; prints diagnostic and returns None on bad/missing id
def find_expense(expense_id):
  try:
    expense_id = int(expense_id)
  # int("abc") raises ValueError; int(None) raises TypeError
  except (TypeError, ValueError):
    print(f"Invalid id: {expense_id}")
    return None
  for e in data["expenses"]:
    if e["id"] == expense_id:
      return e
  print(f"Expense {expense_id} not found")
  return None


# --- Expense operations ---

# Append a new expense and persist; warns if monthly budget exceeded
def add_expense(description, amount, category="other"):
  today = datetime.now().strftime("%Y-%m-%d")
  expense = {
    "id": max((e["id"] for e in data["expenses"]), default=0) + 1,
    "date": today,
    "description": description,
    "amount": amount,
    "category": category
  }
  data["expenses"].append(expense)
  save()
  print(f"Expense added (ID: {expense['id']})")
  _check_budget(int(today[5:7]))

# Print all expenses, optionally filtered by category
def list_expenses(category_filter=None):
  rows = data["expenses"]
  if category_filter:
    rows = [e for e in rows if e["category"] == category_filter]
  if not rows:
    print("(no expenses)")
    return
  print(f"{'ID':<4} {'Date':<12} {'Category':<14} "
        f"{'Amount':>10}  Description")
  for e in rows:
    print(f"{e['id']:<4} {e['date']:<12} {e['category']:<14} "
          f"${e['amount']:>9.2f}  {e['description']}")

# Update one or more fields on an existing expense by id
def update_expense(id, description=None, amount=None, category=None):
  expense = find_expense(id)
  if expense is None:
    return
  if description is not None:
    expense["description"] = description
  if amount is not None:
    expense["amount"] = amount
  if category is not None:
    expense["category"] = category
  save()
  print(f"Expense {expense['id']} updated")

# Remove an expense by id
def delete_expense(id):
  expense = find_expense(id)
  if expense is None:
    return
  data["expenses"] = [e for e in data["expenses"]
                      if e["id"] != expense["id"]]
  save()
  print(f"Expense {expense['id']} deleted")

# Print total spending; if month given, restrict to that month of this year
def summary(month=None):
  if month is None:
    total = sum(e["amount"] for e in data["expenses"])
    print(f"Total expenses: ${total:.2f}")
    return
  year = datetime.now().year
  prefix = f"{year}-{month:02d}-"
  rows = [e for e in data["expenses"] if e["date"].startswith(prefix)]
  total = sum(e["amount"] for e in rows)
  month_name = datetime(year, month, 1).strftime("%B")
  print(f"Total expenses for {month_name} {year}: ${total:.2f}")

# Set the spending budget for `month` (current year) and persist
def set_budget(month, amount):
  data["budgets"][str(month)] = amount
  save()
  month_name = datetime(datetime.now().year, month, 1).strftime("%B")
  print(f"Budget for {month_name}: ${amount:.2f}")

# If current spending in `month` exceeds its budget, print a warning
def _check_budget(month):
  budget = data["budgets"].get(str(month))
  if budget is None:
    return
  year = datetime.now().year
  prefix = f"{year}-{month:02d}-"
  spent = sum(e["amount"] for e in data["expenses"]
              if e["date"].startswith(prefix))
  if spent > budget:
    over = spent - budget
    month_name = datetime(year, month, 1).strftime("%B")
    print(f"Warning: {month_name} spending (${spent:.2f}) "
          f"exceeds budget (${budget:.2f}) by ${over:.2f}")


# --- Export ---

# Write all expenses to expenses.csv in the current directory
def export_csv():
  if not data["expenses"]:
    print("(no expenses to export)")
    return
  with open(CSV_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "date", "description", "amount", "category"])
    for e in data["expenses"]:
      writer.writerow([e["id"], e["date"], e["description"],
                       f"{e['amount']:.2f}", e["category"]])
  print(f"Exported {len(data['expenses'])} expenses to {CSV_FILE}")


# --- Help / dispatch ---

# Print the command list and category reference
def help():
  print("Expense Tracker - Commands")
  print("-" * 42)
  for c in COMMANDS:
    print(f"{c}\t{COMMANDS[c]}")
  print()
  print(f"Categories: {', '.join(CATEGORIES)}")
  print("--: required information\n<>: input options\n[]: optional command")

# Print a usage hint for `command` based on the COMMANDS table
def _usage(command):
  print(f"Usage: expense-cli {command} {COMMANDS[command]}")

# Route a parsed command + its remaining argv tokens to the right handler
def dispatch(command, args):
  if command == "add":
    flags, err = parse_flags(args)
    if err:
      _usage("add")
      print(err)
      return
    if "description" not in flags or "amount" not in flags:
      _usage("add")
      return
    amount = parse_amount(flags["amount"])
    if amount is None:
      return
    category = "other"
    if "category" in flags:
      category = parse_category(flags["category"])
      if category is None:
        return
    add_expense(flags["description"], amount, category)
    return

  if command == "list":
    flags, err = parse_flags(args)
    if err:
      _usage("list")
      print(err)
      return
    cat = None
    if "category" in flags:
      cat = parse_category(flags["category"])
      if cat is None:
        return
    list_expenses(cat)
    return

  if command == "update":
    if not args:
      _usage("update")
      return
    expense_id = args[0]
    flags, err = parse_flags(args[1:])
    if err:
      _usage("update")
      print(err)
      return
    if not flags:
      print("No fields to update")
      return
    amount = None
    if "amount" in flags:
      amount = parse_amount(flags["amount"])
      if amount is None:
        return
    category = None
    if "category" in flags:
      category = parse_category(flags["category"])
      if category is None:
        return
    update_expense(expense_id,
                   description=flags.get("description"),
                   amount=amount,
                   category=category)
    return

  if command == "delete":
    if not args:
      _usage("delete")
      return
    delete_expense(args[0])
    return

  if command == "summary":
    flags, err = parse_flags(args)
    if err:
      _usage("summary")
      print(err)
      return
    month = None
    if "month" in flags:
      month = parse_month(flags["month"])
      if month is None:
        return
    summary(month)
    return

  if command == "budget":
    flags, err = parse_flags(args)
    if err:
      _usage("budget")
      print(err)
      return
    if "month" not in flags or "amount" not in flags:
      _usage("budget")
      return
    month = parse_month(flags["month"])
    if month is None:
      return
    amount = parse_amount(flags["amount"])
    if amount is None:
      return
    set_budget(month, amount)
    return

  if command == "export":
    export_csv()
    return


# --- CLI ---

# CLI entry point: load state, parse argv, dispatch
def main():
  load()
  args = sys.argv[1:]

  if not args or args[0] in ("help", "--help", "-h"):
    help()
    return

  command = args[0]
  if command not in COMMANDS:
    print(f"Error: Invalid command '{command}'. "
          f"See command list below.")
    help()
    return

  dispatch(command, args[1:])


if __name__ == "__main__":
  main()
