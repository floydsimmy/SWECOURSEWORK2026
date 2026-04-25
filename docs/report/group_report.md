# Group Report — Cluedo (Software Engineering G6046)

> **Draft skeleton.** This document is a Sprint 4 deliverable.
> Per `CLAUDE.md` §13.5, named contributions and retrospective
> content must come from the team — they are not fabricated here.
> Replace every `[CONTRIBUTOR A–E]` and `[TEAM TO FILL IN]`
> placeholder before submission.
>
> The report is filed at `docs/report/group_report.md` to match
> the topic-subfolder layout established by ADR-002 and recorded
> as ADR-005.

---

## 1. Project overview

**What was built.** A Python + Pygame implementation of *Clue!* for
3–6 hot-seat human players. Title screen, setup screen with player
name entry and validation, gameplay screen with private hand display,
turn-based action loop (move, suggest, accuse, end turn), end screen
revealing the solution. The engine implements F1–F8 and NF1–NF2 from
the user requirements as documented in `CLAUDE.md` §6.

**What was not built (out of scope per `CLAUDE.md` §2).**
AI / autonomous players; full 2D board with grid pathing, doors, and
secret passages; networked multiplayer; save/load games; detective
notes sheet; animations and sound effects; database backend; web or
mobile build. These are documented as deliberate exclusions; F4 was
implemented as a simplified room-list selection rather than grid
movement.

**Run the build.**
```bash
pip install -r requirements.txt
python -m src.main
```

## 2. Team organisation

Per `CLAUDE.md` §13.5, names are placeholders until the team
substitutes them at submission.

| Role                                  | Member            |
| ------------------------------------- | ----------------- |
| Technical Lead & Integrator           | `[CONTRIBUTOR A]` |
| Game Logic Engineer                   | `[CONTRIBUTOR B]` |
| Product Owner                         | `[CONTRIBUTOR C]` |
| QA Lead                               | `[CONTRIBUTOR D]` |
| Scrum Master & Documentation Owner    | `[CONTRIBUTOR E]` |

**How we worked.** `[TEAM TO FILL IN]` — describe the cadence
(weekly meetings, async standups), the communication channels used,
and any process adaptations made in flight. Reference the meeting
minutes in `docs/meetings/`.

**Peer-assessment marks.**
The playbook awards 20 points per member, distributed by team
agreement.

| Member            | Marks         | Justification                                   |
| ----------------- | ------------- | ----------------------------------------------- |
| `[CONTRIBUTOR A]` | `[TO AGREE]`  | `[TEAM TO FILL IN]`                              |
| `[CONTRIBUTOR B]` | `[TO AGREE]`  | `[TEAM TO FILL IN]`                              |
| `[CONTRIBUTOR C]` | `[TO AGREE]`  | `[TEAM TO FILL IN]`                              |
| `[CONTRIBUTOR D]` | `[TO AGREE]`  | `[TEAM TO FILL IN]`                              |
| `[CONTRIBUTOR E]` | `[TO AGREE]`  | `[TEAM TO FILL IN]`                              |

If the team agrees an equal split, marks are 20 / 20 / 20 / 20 / 20.

## 3. Sprint-by-sprint progress

For each sprint, summarise the goal, what was delivered, and the
state of the test suite at sprint close. Cross-reference the
corresponding sprint document in `docs/sprints/`.

### Sprint 1 — Foundation & Engine Core
- **Goal:** Headless engine + a Pygame window that opens cleanly.
- **Delivered:** `[TEAM TO FILL IN]` — pull the bullet list from
  `docs/sprints/sprint_1.md` §7 "Summary of sprint".
- **Test state at close:** `[TEAM TO FILL IN]` — number of unit tests
  passing.

### Sprint 2 — Core Gameplay Mechanics
- **Goal:** Full game playable end-to-end through the GUI.
- **Delivered:** `[TEAM TO FILL IN]` — pull from
  `docs/sprints/sprint_2.md`.
- **Test state at close:** `[TEAM TO FILL IN]`.
- **Known carry-over bug:** F12-DOMAIN — suggestion did not move
  suspect/weapon tokens into the suggester's room. Closed in Sprint 3.

### Sprint 3 — Robustness & Validation (closure with API tightening)
- **Goal:** Hardening sprint — input validation, edge cases, no
  feature work.
- **Delivered:** `[TEAM TO FILL IN]` — pull from
  `docs/sprints/sprint_3.md`. Note the API-tightening additions
  recorded in ADR-004 (`src/__init__.py` shim) and the F12-DOMAIN
  closure (suspect/weapon token locations now tracked in
  `GameState`).
- **Test state at close:** 100 passed.

### Sprint 4 — Polish, Demo & Submission
- **Goal:** Submission-ready build; code freeze with one critical
  bugfix.
- **Delivered:** `[TEAM TO FILL IN AT SPRINT CLOSE]` — pull from
  `docs/sprints/sprint_4_end.md` once the team fills it in.
- **Test state at close:** `[TEAM TO FILL IN AT SPRINT CLOSE]`.

## 4. What went well

Prompt: include process and engineering wins. Examples to consider —
do **not** copy verbatim, write what actually happened:

- Did the engine / GUI separation (per `CLAUDE.md` §4) hold cleanly?
- Did the unit test suite catch regressions before they shipped?
- Did the sprint structure (start doc → work → end doc) help cadence?
- Were ADRs useful when scope decisions came up?

`[TEAM TO FILL IN]`

## 5. What did not go well

Prompt: be honest. The marker reads this section to assess
self-awareness as much as engineering output.

- Were any sprints under- or over-scoped?
- Did any decisions get re-litigated in a later sprint?
- Were there integration friction points between engine and GUI?
- Were any §13.5 artefacts (video, peer-assessment, screenshots)
  rushed at the end?

`[TEAM TO FILL IN]`

## 6. What we would do differently

Prompt: forward-looking, concrete. "Smaller PRs" or "earlier
integration" are good answers if true. "Better communication" without
specifics is not useful.

`[TEAM TO FILL IN]`

## 7. Outstanding issues

Document anything the marker should know that is not obvious from
running the build.

| Item                                              | Status / what we would do          |
| ------------------------------------------------- | ---------------------------------- |
| F3 Miss Scarlett primacy rule (`CLAUDE.md` §6): the engine cycles turn order clockwise correctly (verified by ST-03a–c), but does not seat Miss Scarlett first when present. This is a design choice: the implementation takes free-text player names rather than binding players to suspect characters, so the "Miss Scarlett goes first" clause is unimplementable without character-binding. The clockwise cycling rule is satisfied; the primacy rule is consciously unimplemented. | Future work would add a character-pick step to the Setup screen. |
| `[TEAM TO FILL IN]`                                | `[TEAM TO FILL IN]`                |

Examples of items that may belong here, if they apply:

- Out-of-scope features per `CLAUDE.md` §2 (AI, grid board, …) —
  not implemented by deliberate scope choice.
- Technical debt logged in `docs/decisions.md` (ADR-001 `rules.py`
  not extracted; ADR-004 `sys.path` shim).
- Any test marked Skip or any system test marked Pending evidence in
  `docs/testing/system_test_report.md`.

---

*Final read-through and sign-off by every team member is required
before submission.*
