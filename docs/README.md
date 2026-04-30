# Documentation Index — Team 53

This directory contains all process, design, testing, and reporting documentation for the Cluedo project. Documents are grouped by topic. This index maps each marking-criteria element and each submission-guidance deliverable to its actual location, so a marker can find what they need without exploring directories.

## For markers — quick map of marking criteria to evidence

| Marking element                | Folder / file                                                     |
| ------------------------------ | ------------------------------------------------------------------ |
| Planning docs (5 marks)        | `planning/project_plan.md`, `planning/gantt.md`, `planning/risk_register.md` |
| Planning — meeting notes (5)   | `meetings/` — 9 meeting minute files plus `2026-03-25_team_progress_review.md` |
| Process documentation (10)     | `sprints/sprint_1.md`, `sprint_2.md`, `sprint_3.md`, `sprint_4.md` |
| Design — high level (5)        | `design/architecture.md`                                           |
| Design — low level (5)         | `design/class_diagram.md`, `design/sequence_diagram.md`, `design/api.md` |
| Software documentation (5)     | Docstrings inside `src/game/*.py` and `src/ui/*.py`                |
| Testing documentation (10)     | `testing/system_test_report.md` plus the 116-test pytest suite in `tests/` |
| Code (50)                      | `src/`                                                              |
| Group report (5)               | `report/group_report.md`, `report/peer_review.md`                  |

## Repository layout

```
src/
  main.py                # Pygame entry point
  game/                  # Engine + AI — no Pygame imports
    models.py            # Card, Player (+ player_type, ai_notes), GameState, DetectiveNotes, RefuteResult, AccusationResult
    deck.py              # SUSPECTS, WEAPONS, ROOMS, create_deck, verify_deck
    engine.py            # All rules: dice + grid pathfinder (BFS), suggestion, accusation, F12 token tracking, validation
    ai.py                # RandomAIPlayerStrategy, take_ai_turn, run_ai_simulation, DetectiveNotes helpers
  ui/                    # Pygame screens and components
    screens.py           # MainMenu / Setup (with Human/AI toggle) / Game / End screens + ScreenManager
    components.py        # Button, TextInput, PopupSelect, MessageBox, CardDisplay
    gui.py               # Board renderer (24x24 grid, doors, tokens, dice-move highlight)
tests/
  test_models.py         # Unit tests for the data models
  test_engine.py         # Unit tests for the engine
  test_ai.py             # Unit tests for the AI player module and privacy invariants
docs/                    # This documentation pack
  README.md              # This file
  decisions.md           # Engineering Decisions Log (ADRs)
  planning/              # Project plan, Gantt, risk register
  meetings/              # 9 meeting minutes + team progress review form
  sprints/               # One document per sprint (sprint_1 through sprint_4)
  design/                # Architecture, class diagram, sequence diagram, engine API
  testing/               # System test report
  report/                # Group report, peer review, requirements
  screenshots/           # Title, gameplay, end-screen images for README
```

## Submission folder mapping

Per the Submission Guidance from Hsi-Ming Ho, the submission ZIP is organised into eight folders. The mapping from this repo to those folders is:

| Submission folder     | Source in this repo                                          |
| --------------------- | ------------------------------------------------------------ |
| Planning documents    | `docs/planning/`                                             |
| Team meeting documents| `docs/meetings/`                                             |
| Sprint cycle documents| `docs/sprints/`                                               |
| Design evidence       | `docs/design/`                                                |
| Codebase              | `src/`, `tests/`, `requirements.txt`, `pytest.ini`, `README.md`, `CLAUDE.md` |
| Testing evidence      | `docs/testing/system_test_report.md`                          |
| Video                 | (separately recorded MP4 file)                                |
| Group report          | `docs/report/group_report.md`, `docs/report/peer_review.md`   |
