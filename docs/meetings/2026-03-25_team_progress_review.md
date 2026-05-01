# Software Engineering — Group Coursework Team Review Meeting

(Internal team self-assessment, completed using the form from `TeamProgressMeeting.pdf`. Not a formal meeting with the module convenor.)

| Field      | Value                                          |
| ---------- | ---------------------------------------------- |
| Team       | 53                                             |
| Present    | Adam, Floyd, Maysarah, Nasser, Abdurrahman     |
| Format     | Async — completed in `#decisions` channel on Discord, signed off by all members |
| Date       | 2026-03-25                                     |

## Quick checklist

| Question                                                   | Answer |
| ---------------------------------------------------------- | ------ |
| How many sprints have you completed?                       | 1 (working on Sprint 2, which is currently extended) |
| Have the sprints delivered a working prototype each?       | Yes — Sprint 1 closed with a working engine and a title screen. Sprint 2 will deliver the full gameplay loop. |
| How many active members are in your team?                  | 5      |
| How many inactive members are in your team?                | 0 — all members contributing, though attendance at scheduled meetings varies (Nasser and Abdurrahman work more asynchronously via Discord). |

## Q1: What planning have you undertaken so far? (PERT/Risk/resources etc)

A PERT-style task breakdown with a critical path covering all four sprints, a Gantt-style overview, and a risk register scoring each risk on likelihood × impact. See `docs/planning/`. The plan was reviewed at the kickoff meeting on 2026-02-25 and is updated at each sprint review.

## Q2: Have you been monitoring the Canvas discussion threads for updates from your customer?

Yes. Adam (Product Owner) checks Canvas every Monday and Thursday and posts relevant updates to the team Discord `#announcements` channel. No material requirement changes from the customer to date.

## Q3: What languages and tools have you selected for your implementation?

- **Language:** Python 3.10+ (developing on 3.13).
- **GUI library:** Pygame.
- **Test framework:** pytest, with `pythonpath=src` configured in `pytest.ini`.
- **Version control / collaboration:** Git + GitHub, Discord for async coordination, Google Meet for scheduled meetings, draw.io for diagrams.
- **Justification:** Python is cross-platform without licensing concerns, every team member already had it installed, and Pygame meets the desktop GUI requirement. pytest is industry-standard.

## Q4: Is there a current working prototype? If so, show it.

Yes. The current build supports a Pygame window with a title screen and basic game flow. The full gameplay loop (Move, Suggest, Accuse, EndScreen) lands at the end of the current Sprint 2.

## Q5: Are there any kind of other demonstrable elements yet?

- Engine class diagram in `docs/design/class_diagram.md`
- Sequence diagram for the Suggestion / Refutation flow in `docs/design/sequence_diagram.md`
- Architecture overview in `docs/design/architecture.md`
- Unit test suite in `tests/` (passing)
- System test report skeleton in `docs/testing/system_test_report.md`

## Q6: Is there anything you need feedback for from your customer?

- Confirmation that the AI player's behaviour as the team plans to ship it (random over what the AI legally knows; accuse only on single-candidate notes; never reads the hidden solution) is what the customer expects from "an autonomous-player option". The team committed to ship the AI in Sprint 3 (ADR-006); a sanity check on behaviour expectations would be welcome before then.
- Any preference on font / colour scheme — currently using a flat dark-blue palette.

## Q7: Are there any other factors that are having an effect on your team's ability to deliver on this group project?

- Two team members (Nasser, Abdurrahman) have heavier coursework loads from other modules; they contribute primarily asynchronously via Discord rather than at every scheduled meeting. Both are delivering on their assigned tasks.
- Sprint 2 has been extended by one week to absorb integration work that ran longer than estimated.
- No team-internal blockers; communication is consistent.

Signed off by all five members on Discord, 2026-03-25.
