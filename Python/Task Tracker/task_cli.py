import json
import sys
import os
from datetime import datetime

data_dict = {"tasks":[]}

def add_task(description):
  now = datetime.now().strftime("%Y-%m-%d %H:%M")
  task = {
    "id": max((t["id"] for t in data_dict["tasks"]), default=0) + 1,
    "description": description,
    "status": "todo",
    "createdAt": now,
    "updatedAt": now
  }

  data_dict["tasks"].append(task)
  update_json()

def find_task(task_id):
  try:
    task_id = int(task_id)
  except (TypeError, ValueError):
    print(f"Invalid id: {task_id}")
    return None
  for task in data_dict["tasks"]:
    if task["id"] == task_id:
      return task
  print(f"Task {task_id} not found")
  return None

def update_task_description(id, description):
  task = find_task(id)
  if task is None:
    return
  task["description"] = description
  task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
  update_json()

def delete_task(id):
  if find_task(id) is None:
    return
  task_id = int(id)
  data_dict["tasks"] = [t for t in data_dict["tasks"] if t["id"] != task_id]
  update_json()

def _set_status(id, status):
  task = find_task(id)
  if task is None:
    return
  task["status"] = status
  task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
  update_json()

def mark_in_progress(id):
  _set_status(id, "in-progress")

def mark_done(id):
  _set_status(id, "done")

def _print_task(task):
  print(f"[{task['id']}] ({task['status']}) {task['description']}")

def list_tasks_by_type(type):
  matches = [t for t in data_dict["tasks"] if t["status"] == type]
  if not matches:
    print("(no tasks)")
    return
  for t in matches:
    _print_task(t)

def list_tasks():
  if not data_dict["tasks"]:
    print("(no tasks)")
    return
  for t in data_dict["tasks"]:
    _print_task(t)

def update_json():
  with open('data.json', 'w') as f:
    json.dump(data_dict,f,indent=2)


def main():
  global data_dict

  if not os.path.exists('data.json'):
    update_json()

  else:
    with open('data.json','r') as f:
      data_dict = json.load(f)

  args = sys.argv[1:]

  if not args:
    print("Usage: task-cli <command>")
    return
  
  command = args[0]
  if command == "add":
    if len(args) < 2:
      print("Usage: task-cli add <description>")
      return
    add_task(args[1])
  elif command == "update":
    if len(args) < 3:
      print("Usage: task-cli update <id> <description>")
      return
    update_task_description(args[1], args[2])
  elif command == "delete":
    if len(args) < 2:
      print("Usage: task-cli delete <id>")
      return
    delete_task(args[1])
  elif command == "mark-in-progress":
    if len(args) < 2:
      print("Usage: task-cli mark-in-progress <id>")
      return
    mark_in_progress(args[1])
  elif command == "mark-done":
    if len(args) < 2:
      print("Usage: task-cli mark-done <id>")
      return
    mark_done(args[1])
  elif command == "list":
    if len(args) < 2:
      list_tasks()
    elif args[1] == "todo":
      list_tasks_by_type("todo")
    elif args[1] == "in-progress":
      list_tasks_by_type("in-progress")
    elif args[1] == "done":
      list_tasks_by_type("done")
    else:
      print(f"Unknown list filter: {args[1]}. Valid: todo, in-progress, done")
  else:
    print(f"Unknown command: {command}")

if __name__ == "__main__":
  main()