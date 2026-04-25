# Cluedo

A Python + Pygame implementation of the classic *Clue!* murder mystery
board game, built as a five-person Software Engineering coursework
project (G6046).

3–6 local human players take turns to deduce the murderer, the
weapon, and the room. The game is hot-seat: one machine, one screen,
players pass the device.

---

## Install

Requires **Python 3.10+** (developed and tested on 3.13).

```bash
pip install -r requirements.txt
```

`requirements.txt` pins the exact versions used in development:

```
pygame==2.6.1
pytest==9.0.3
```

---

## Run

The canonical run command (per ADR-004 in `docs/decisions.md`) is:

```bash
python -m src.main
```

An equivalent invocation is also supported:

```bash
python src/main.py
```

Both open the same Pygame window (1200 × 800).

---

## Player setup

1. From the title screen, click **Start New Game**.
2. Enter between 3 and 6 player names. Empty and duplicate names are
   rejected with a visible error.
3. Click **Start Game** to deal the cards and begin.

The engine selects one suspect, one weapon, and one room as the
hidden solution; the remaining 18 cards are dealt round-robin (some
players may receive one more card than others — this is fair per the
original game rules).

---

## Controls

The game is mouse-driven from start to finish.

| Action          | How to do it                                                                 |
| --------------- | ---------------------------------------------------------------------------- |
| Move to a room  | Click **Move to Room** → pick a room from the dropdown → **Confirm**         |
| Make a suggestion | Click **Make Suggestion** (requires being in a room) → pick suspect + weapon → **Confirm** |
| Make an accusation | Click **Make Accusation** → pick suspect + weapon + room → **Confirm**     |
| End your turn   | Click **End Turn**                                                            |
| Quit            | Close the window, or click **Quit** on the title screen                        |

Suggestions and accusations validate inputs and surface clear errors
(out of turn, eliminated, missing room) without crashing the game.

---

## Screenshots

> Per CLAUDE.md §13.5, screenshots are produced by the team running
> the build. Insert images in this section before submission.

- `[SCREENSHOT: title screen]`
- `[SCREENSHOT: gameplay]`
- `[SCREENSHOT: end screen]`

---

## Run the tests

```bash
python -m pytest -q
```

The unit test suite covers the engine's setup, dealing, turn cycling,
suggestion + refutation, accusation, and state validation. There
should be **100 passed** at submission.

---

## Documentation

Process, design, testing, and reporting documentation lives under
[`docs/`](./docs/). Start at [`docs/README.md`](./docs/README.md) for a
marker-facing index of every deliverable.

Engineering decisions and deviations from the playbook are recorded
as ADRs in [`docs/decisions.md`](./docs/decisions.md).
