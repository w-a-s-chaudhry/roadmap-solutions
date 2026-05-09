# Number Guessing Game

A CLI guessing game. The computer picks a random number from 1-100 and
you try to guess it within a per-difficulty attempt limit, with
higher/lower hints after each wrong guess.

Solution to the [Number Guessing Game](https://roadmap.sh/projects/number-guessing-game)
project from roadmap.sh.

## Run

No install step. From this directory:

```bash
python number_guessing_game.py
```

## Difficulties

| Level  | Attempts |
|--------|----------|
| easy   | 10       |
| medium | 5        |
| hard   | 3        |

## Features

- Random target between 1 and 100.
- Higher/lower feedback after each wrong guess.
- Win message reports attempt count; loss message reveals the answer.
- Replay loop — play as many rounds as you like in one session.
- Per-difficulty high score (fewest attempts) persisted to
  `highscores.json` next to the script.
