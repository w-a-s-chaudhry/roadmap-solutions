# Task Tracker

A simple CLI to track tasks. Stores state in `data.json` in the current working directory.

Solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) project from roadmap.sh.

## Install

From this directory:

```bash
pip install -e .
```

(For an isolated install on Windows, `pipx install .` is recommended once the package is in a stable shape.)

## Usage

```bash
task-cli add "buy milk"
task-cli update <id> "new description"
task-cli delete <id>
task-cli mark-in-progress <id>
task-cli mark-done <id>
task-cli list                 # all tasks
task-cli list todo
task-cli list in-progress
task-cli list done
```

`data.json` is created in the current working directory on first use.
