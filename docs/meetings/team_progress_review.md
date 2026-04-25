# Software Engineering — Group Coursework Team Review Meeting

(Adapted from `TeamProgressMeeting.pdf`, completed for our team.)

| Field      | Value                                          |
| ---------- | ---------------------------------------------- |
| Team       | (assigned by Canvas)                           |
| Present    | Floyd, Maysarah, Member C, Member D, Member E  |
| Review by  | Module teaching team                           |
| Date       | 2026-03-08                                     |

## Quick checklist

| Question                                                   | Answer |
| ---------------------------------------------------------- | ------ |
| How many sprints have you completed?                       | 2 (working on 3) |
| Have the sprints delivered a working prototype each?       | Yes — see `docs/sprints/sprint_*.md` |
| How many active members are in your team?                  | 5      |
| How many inactive members are in your team?                | 0      |

## Q1: What planning have you undertaken so far? (PERT/Risk/resources etc)

A full PERT-style task breakdown with critical path, plus a Gantt
overview and a risk register. See `docs/planning/`.

## Q2: Have you been monitoring the Canvas discussion threads for updates from your customer?

Yes. Member C (PO) checks Canvas every Monday and Thursday and posts
relevant updates to the team Discord `#announcements` channel. No
material requirement changes from the customer to date.

## Q3: What languages and tools have you selected for your implementation?

- **Language:** Python 3.11+ (running 3.13 in CI).
- **GUI:** Pygame (chosen for cross-platform desktop and the team's
  prior familiarity).
- **Tests:** pytest with `pythonpath=src` configured in `pytest.ini`.
- **VCS / collaboration:** Git + GitHub, Discord, draw.io.
- **Justification:** Python is inclusive (every team member can run it
  on Mac and Windows without licensing), Pygame meets the desktop GUI
  requirement, and pytest is industry-standard.

## Q4: Is there a current working prototype? If so, show it.

Yes. Run `python src/main.py`. The current build supports:

- Title screen with Start / Quit
- Setup screen for 3-6 player names with validation
- Game screen with current player, hand, room display, action buttons
  (Move, Suggest, Accuse, End Turn), dropdowns, and a turn log
- End screen showing the winner (or draw) and revealing the solution

## Q5: Are there any kind of other demonstrable elements yet?

- Engine class diagram in `docs/design/class_diagram.md`
- Sequence diagram for the Suggestion / Refutation flow in
  `docs/design/sequence_diagram.md`
- Architecture overview in `docs/design/architecture.md`
- 91-case unit test suite in `tests/`
- System test report in `docs/testing/system_test_report.md`

## Q6: Is there anything you need feedback for from your customer?

- Confirmation that random AI is not required for a passing grade
  (we have descoped AI entirely; PO read the marking criteria as
  endorsing this).
- Any preference on font / colour scheme — currently using a flat
  dark-blue palette inspired by classic detective board games.

## Q7: Are there any other factors that are having an effect on your team's ability to deliver on this group project?

- Two coursework deadlines from other modules in the same week as
  Sprint 3 review. Mitigation: Sprint 3 is scoped lighter than
  Sprint 2.
- No team-internal blockers; communication and attendance have been
  consistent throughout.

January 2026
