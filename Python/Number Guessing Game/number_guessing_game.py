# Author:      Wajid Ali Saleem Chaudhry
# Description: Number Guessing Game CLI: pick a difficulty, guess the
#              random number, and persist per-difficulty best scores.

import json
import os
import random

# --- Configuration ---

DIFFICULTIES = {
  1: ["easy",10],   # [label, max_attempts]
  2: ["medium",5],
  3: ["hard",3]
}

# --- High Scores ---

SCORES_PATH = os.path.join(
  os.path.dirname(os.path.abspath(__file__)), "highscores.json"
)

# Load high scores from disk; return {} if file is missing, malformed,
# or stores something other than a JSON object
def load_highscores():
  try:
    with open(SCORES_PATH) as f:
      data = json.load(f)
  except (FileNotFoundError, json.JSONDecodeError):
    return {}
  return data if isinstance(data, dict) else {}

# Persist high scores dict to disk as JSON
def save_highscores(scores):
  with open(SCORES_PATH, "w") as f:
    json.dump(scores, f, indent=2)

# Print current high score for each difficulty
def show_highscores(scores):
  print("\nHigh scores (fewest attempts):")
  for d in DIFFICULTIES:
    name = DIFFICULTIES[d][0]
    best = scores.get(name)
    if best is None:
      print(f"  {name}: --")
    else:
      print(f"  {name}: {best}")

# Update score if attempts beats record; returns True if new best
def maybe_update_highscore(scores, difficulty_name, attempts):
  best = scores.get(difficulty_name)
  if best is None or attempts < best:
    scores[difficulty_name] = attempts
    save_highscores(scores)
    return True
  return False

# --- Input Helpers ---

# Prompt until user enters a whole number that maps to a difficulty key
def read_difficulty():
  while True:
    raw = input("\nEnter your choice (1-3): ")
    try:
      choice = int(raw)
    except ValueError:
      print("Please enter a whole number.")
      continue
    if choice not in DIFFICULTIES:
      print("Please enter 1, 2, or 3.")
      continue
    return choice

# Prompt until user enters a whole number between 1 and 100
def read_guess():
  while True:
    raw = input("\nEnter your guess: ")
    try:
      guess = int(raw)
    except ValueError:
      print("Please enter a whole number in digits.")
      continue
    if not 1 <= guess <= 100:
      print("Please enter a number between 1 and 100.")
      continue
    return guess

# --- Game Loop ---

# Run welcome, difficulty selection, guessing rounds, and replay loop;
# updates persisted high scores when a winning run beats the record
def main():
  print("Welcome to the number guessing game!")
  scores = load_highscores()
  show_highscores(scores)
  while True:
    print("\nPlease Select the difficulty:")

    for d in DIFFICULTIES:
      print(f"{d}: {DIFFICULTIES[d][0]} \t({DIFFICULTIES[d][1]} chances)")

    choice = read_difficulty()
    diff_name = DIFFICULTIES[choice][0]

    print(
      f"\nGreat you selected the {diff_name} "
      "difficulty level.\nLet's start the game!\n\n"
      "I am thinking of a number between 1 and 100."
    )

    ans = random.randint(1,100)

    for i in range(0,DIFFICULTIES[choice][1]):
      guess = read_guess()

      if guess == ans:
        attempts = i + 1
        print(
          f"Congratulations! You guessed the correct "
          f"number in {attempts} attempts."
        )
        if maybe_update_highscore(scores, diff_name, attempts):
          print(f"New high score for {diff_name}!")
        break
      if i == DIFFICULTIES[choice][1]-1:
        print(f"Incorrect! The correct answer was {ans}.")
        break
      if guess < ans:
        print(f"Incorrect! The number is greater than {guess}.")
      else:
        print(f"Incorrect! The number is lower than {guess}.")

    again = input("\nWould you like to play again (y/n)?: ")
    if again.strip().lower() not in ("y", "yes"):
      print()
      return

if __name__ == "__main__":
  try:
    main()
  except (KeyboardInterrupt, EOFError):
    print("\nGoodbye!")