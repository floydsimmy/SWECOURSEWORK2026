# CURRENT_STATE — Cluedo (Team 53)

Snapshot date: 2026-04-30 (submission day, 16:00 deadline).
Source of truth: working tree at `~/Desktop/SWECOURSEWORK2026`.
Local branch: `removing-ai-slop` (no commits past `main` yet — all rewrites described below are **uncommitted working-tree changes**: 34 files modified, 866 insertions / 668 deletions vs. `HEAD`/`main`).
Remote: `floydsimmy/SWECOURSEWORK2026`. Default branch on GitHub: `main`.

This document describes the codebase as it actually exists on disk right now, not the GitHub `main` snapshot. Many earlier descope claims have been reversed by ADR-006 (grid + dice + AI kept in scope), and the project pack has grown accordingly.

---

## 1. Build and runtime status (verified just now)

- `python -m pytest -q` → **114 passed in ~0.05s** (verified 2026-04-30).
  - `tests/test_models.py` — 18 tests
  - `tests/test_engine.py` — 83 tests (includes new dice/grid + typed-signature regressions, plus a Sprint 4 dice-fairness test `test_roll_die_fairness_seeded`)
  - `tests/test_ai.py` — 13 tests (new file — AI behaviour, privacy, refutation invariants)
- `pytest.ini` configures `pythonpath = src`, `testpaths = tests`.
- `python -m src.main` opens a Pygame window at 1200 × 800 (top-level `README.md`, line 36).
- Both entry-points (`python -m src.main` and `python src/main.py`) work via the `src/__init__.py` shim (ADR-004 — present and unchanged).
- Engine has zero Pygame imports (asserted in `architecture.md`, NF4 in `requirements.md`).
- `requirements.txt` pins `pygame==2.6.1`, `pytest==9.0.3`. Python 3.10+ supported, developed on 3.13.

## 2. Project window (per planning docs)

| Sprint | Window                  | Length  | Lead       |
| ------ | ----------------------- | ------- | ---------- |
| 1      | 2026-02-23 → 2026-03-08 | 14 days | Maysarah   |
| 2      | 2026-03-09 → 2026-03-29 | 21 days | Floyd (extended one week at midpoint to absorb grid + AI integration) |
| 3      | 2026-03-30 → 2026-04-12 | 14 days | Maysarah   |
| 4      | 2026-04-13 → 2026-04-29 | 17 days | Floyd (code-freeze) |

## 3. Team and roles

| Member       | Role                                              | Meetings (of 9) |
| ------------ | ------------------------------------------------- | --------------- |
| Floyd        | Technical Lead & Integrator                       | 9/9             |
| Maysarah     | Game Logic Engineer                               | 8/9 (illness 2026-04-08) |
| Adam         | Scrum Master, Documentation Lead & Product Owner  | 9/9             |
| Nasser       | UI/GUI Engineer                                   | 5/9 (coursework clashes) |
| Abdurrahman  | QA Lead                                           | 4/9 (coursework clashes) |

Peer review split agreed at the final review meeting: equal 20/20/20/20/20 (recorded in `docs/report/peer_review.md`).

## 4. Repository layout (as on disk)

```
SWECOURSEWORK2026/
├── README.md                  # project home page (install/run/screenshots/AI mention)
├── CLAUDE.md                  # Claude Code project playbook (preserves descope language; ADR-006 supersedes it)
├── CURRENT_STATE.md           # this file (untracked)
├── REPO_LINK.txt              # untracked, holds the GitHub URL
├── code_review.md             # untracked, output of an earlier review pass
├── pytest.ini                 # pythonpath=src, testpaths=tests
├── requirements.txt           # pygame==2.6.1, pytest==9.0.3
├── .gitignore
├── .venv/                     # untracked local virtualenv used to run pytest
├── submission_docx/           # untracked, generated docx tree (README.docx + docs/)
├── submission_docx.zip        # untracked, packaged submission archive
├── Cluedo_Team53_Documentation_docx/  # untracked, second docx tree
├── src/
│   ├── __init__.py            # path shim (ADR-004) — three lines, unchanged
│   ├── main.py                # 47 lines — Pygame entry point; imports `from ui.screens`
│   ├── game/                  # engine — no Pygame imports
│   │   ├── __init__.py
│   │   ├── models.py          # 96 lines — Card, DetectiveNotes, Player, GameState, RefuteResult, AccusationResult; HUMAN_PLAYER / AI_PLAYER / PLAYER_TYPES constants
│   │   ├── deck.py            # 73 lines — SUSPECTS, WEAPONS, ROOMS, EXPECTED_DECK_SIZE, create_deck, verify_deck
│   │   ├── engine.py          # 713 lines — full rules incl. dice + grid (ROOM_LAYOUT, ROOM_DOORS, CHARACTER_START_TILES, BOARD_GRID_SIZE=24)
│   │   └── ai.py              # 245 lines — RandomAIPlayerStrategy, AITurnResult, take_ai_turn, run_ai_simulation, ensure_ai_notes, record_known_card, record_suggestion_result, choose_refutation_card
│   └── ui/                    # Pygame screens
│       ├── __init__.py
│       ├── screens.py         # 1357 lines — MainMenu, Setup, Game, End + ScreenManager
│       ├── components.py      # 519 lines — Button, TextInput, DropdownMenu, MessageBox, CardDisplay
│       └── gui.py             # 548 lines — board rendering helpers
├── tests/
│   ├── test_models.py         # 192 lines — 18 tests
│   ├── test_engine.py         # 1379 lines — 83 tests
│   └── test_ai.py             # 239 lines — 13 tests (new this branch)
└── docs/                      # full submission documentation pack (28 markdown files, see §5)
    ├── README.md              # marker-facing index
    ├── decisions.md           # 6 ADRs (ADR-001 .. ADR-006)
    ├── planning/              # 3 files — project_plan, gantt, risk_register
    ├── design/                # 4 files — architecture, class_diagram, sequence_diagram, api
    ├── meetings/              # 10 files — kickoff + 4× midpoint + 4× review + 1× async progress
    ├── sprints/               # 4 files — sprint_1..sprint_4
    ├── report/                # 3 files — requirements, group_report, peer_review
    └── testing/               # 1 file — system_test_report
```

**Note:** `docs/screenshots/` is **not** a directory on disk. `README.md` and `system_test_report.md` reference `docs/screenshots/title.png`, `gameplay.png`, `end.png`, and `f12_evidence.png`. Capturing those PNGs is a Nasser-side outstanding artefact (§9).

## 5. Documentation inventory (detailed)

### 5.1 Top-level

#### `README.md` (105 lines)
Public entry-point readme. Sections: install (`pip install -r requirements.txt`), run (`python -m src.main` or `python src/main.py`, both open 1200 × 800 window), player setup (3–6 names, **Human / AI toggle per slot, mixed games supported**, empty/duplicate names rejected), controls table (**Roll Dice → highlighted corridor tiles + reachable rooms via doors → click to move**, suggestion in room, accusation, end turn, quit). Notes that AI slots auto-resolve in the GUI and that the in-game suggestion log surfaces F12 token movement. Screenshots block (title/gameplay/end). `pytest -q` block: **"Expected output: 114 passed."** Pointer to `docs/`. Team table.

#### `CLAUDE.md` (root, frozen)
Project playbook. **Preserves the original descope language** (AI ❌, grid ❌). A note at the top of the file flags that ADR-006 in `docs/decisions.md` supersedes those descope decisions. Not in `docs/` and not converted to docx. Filed under "codebase" per `docs/README.md` submission mapping.

### 5.2 `docs/README.md` — marker-facing index

Maps every marking-criteria element to its location:

| Marking element                | File(s)                                                            |
| ------------------------------ | ------------------------------------------------------------------ |
| Planning docs (5)              | `planning/{project_plan,gantt,risk_register}.md`                   |
| Meeting notes (5)              | `meetings/` (10 files — see §5.6)                                  |
| Process docs (10)              | `sprints/sprint_{1,2,3,4}.md`                                       |
| Design — high level (5)        | `design/architecture.md`                                            |
| Design — low level (5)         | `design/{class_diagram,sequence_diagram,api}.md`                    |
| Software docs (5)              | docstrings inside `src/game/*.py`, `src/ui/*.py`                    |
| Testing docs (10)              | `testing/system_test_report.md` + 114-test pytest suite             |
| Code (50)                      | `src/`                                                              |
| Group report (5)               | `report/{group_report,peer_review}.md`                              |

Submission ZIP folder mapping (per Hsi-Ming Ho's submission guidance): planning / meetings / sprints / design / codebase / testing / video / group-report.

### 5.3 `docs/decisions.md` — Engineering Decisions Log (6 ADRs)

Append-only ADR log.

- **ADR-001 — Rules logic remains inlined in `engine.py`.** Status: Accepted, Sprint 3. Defers extraction of `rules.py` post-submission.
- **ADR-002 — Documentation organised under topic subfolders.** Status: Accepted, Sprint 3. Retains `docs/{planning,design,testing,report,meetings,sprints}/` rather than the flat layout in `CLAUDE.md` §3.
- **ADR-003 — Hand privacy interpreted in hot-seat context.** Active player's hand shown to active player only.
- **ADR-004 — `src/__init__.py` shim to support both run commands.** "91-test green suite" preserved as the decision-moment snapshot; a Sprint 4 cleanup note records that the suite grew to 113 in Sprint 3 and 114 by submission.
- **ADR-005 — Group report at `docs/report/group_report.md`.** Maintains ADR-002 layout instead of `CLAUDE.md` §13.5's flat path.
- **ADR-006 — Keep grid + dice movement and the AI player in scope.** Status: Accepted, Sprint 2 midpoint, reaffirmed at Sprint 3 close. Reverses the descope language in `CLAUDE.md` §2 and §13. Rationale: marking-criteria upper code band requires the AI deliverable; dice + grid is the actual Cluedo movement rule. Records that Sprint 2 ran 21 days, Sprint 3 closed at 113 tests (87 engine + 13 AI + 18 model + 5 typed-signature/regression), and the AI lives in `src/game/ai.py`.

### 5.4 `docs/planning/` (3 files)

#### `project_plan.md`
Roles table; sprint schedule table (the four windows above); PERT-style task breakdown with durations, predecessors, owners; critical path; resources (~120 person-hours); plan-vs-actual section flags Sprint 2's one-week extension and the **decision to keep grid + AI in scope** (ADR-006). No descope language remaining.

#### `gantt.md`
Text-rendered Gantt across the four sprint windows. Same task list as the project plan with `[#]`-style time bars. Critical path identical. Reflects the Sprint 2 extension.

#### `risk_register.md`
9 risks (R1–R9) on a 1–3 likelihood × impact scale. Anything ≥6 actively monitored. Risks that fired at material level: **R3 (scope creep)** during Sprint 2 with the grid integration — managed via the one-week extension rather than dropped; **R6 (test rot)** once in Sprint 3 (caught by `pytest` before merge); **R9 (attendance)** across the project. R8 (submission upload) mitigated with a 22-hour buffer to deadline.

### 5.5 `docs/design/` (4 files)

#### `architecture.md`
Component overview ASCII diagram showing UI ↔ Engine boundary, with the AI module sitting alongside `tests/` and `src/ui/` as a third consumer of the engine API. Boundaries section: engine has no Pygame, UI implements no rules, deck constants single-source, **AI uses only public-knowledge inputs**. Module dependency graph (no cycles). Data flow for a single human turn and a single AI turn. **Out-of-scope list** now: save/load, networked multiplayer, animations, sound, mobile, web, detective-notes sheet rendered for human players. Grid + AI are no longer listed as descoped.

#### `class_diagram.md`
ASCII class diagrams for `Card`, `DetectiveNotes`, `Player` (now with `player_type`, `character`, `board_position`, `ai_notes` fields), `GameState` (with `suspect_locations`, `weapon_locations`), `RefuteResult`, `AccusationResult`. Engine API listing for `engine.py`. AI module classes (`AITurnResult`, `RandomAIPlayerStrategy`). `ScreenManager` + `Screen` hierarchy with subclasses (`MainMenu`, `Setup`, `Game`, `End`); component list (`Button`, `TextInput`, `DropdownMenu`, `MessageBox`, `CardDisplay`). Diagram-to-codebase mapping table giving file:line refs.

#### `sequence_diagram.md`
Sequence diagrams in ASCII for: (1) game setup `new_game` (with AI-slot note initialisation), (2) suggestion + refutation `make_suggestion` with refutation walk invariants, (3) accusation `make_accusation`, (4) **AI turn — `take_ai_turn` round trip** including dice roll, legal-move computation, suggestion, optional accusation.

#### `api.md`
Engine public-surface reference. Functions documented (signature + behaviour + error conditions): `new_game`, `reset_game`, `get_current_player`, `next_turn`, `get_game_status`, `get_turn_summary`, `roll_die`, `legal_moves_for_roll`, `move_by_dice`, `move_to_room`, `make_suggestion`, `make_accusation`, `check_for_winner`, `validate_game_state`, `verify_deck`. AI helpers documented separately: `take_ai_turn`, `run_ai_simulation`, `RandomAIPlayerStrategy.{roll_die, choose_room, choose_suggestion, choose_refutation_card, choose_accusation}`. Common contract: all functions raise `ValueError` (not bare `Exception`) on illegal input.

### 5.6 `docs/meetings/` (10 files)

All follow the same template: header table (team, members present, members absent, format, date/time, coordinator); §1 matters from last meeting; §2 issues discussed; §3 decisions agreed; §4 date of next meeting.

| File                                            | Date       | Coordinator | Present              | Format       |
| ----------------------------------------------- | ---------- | ----------- | -------------------- | ------------ |
| `2026-02-25_kickoff.md`                         | 2026-02-25 | Adam        | All 5                | Google Meet  |
| `2026-03-04_sprint1_midpoint.md`                | 2026-03-04 | Adam        | 4 (Nasser absent)    | Google Meet  |
| `2026-03-09_sprint1_review.md`                  | 2026-03-09 | Floyd       | 4 (Abdurrahman absent) | Google Meet |
| `2026-03-18_sprint2_midpoint.md`                | 2026-03-18 | Adam        | 3 (Nasser/Abdurrahman absent) | Google Meet |
| `2026-03-25_team_progress_review.md`            | 2026-03-25 | n/a         | All 5 (async sign-off via Discord) | Async |
| `2026-03-30_sprint2_review.md`                  | 2026-03-30 | Floyd       | All 5                | Google Meet  |
| `2026-04-08_sprint3_midpoint.md`                | 2026-04-08 | Adam        | 2 (Maysarah ill, others clash) | Google Meet |
| `2026-04-13_sprint3_review.md`                  | 2026-04-13 | Maysarah    | 4 (Abdurrahman exam) | Google Meet  |
| `2026-04-22_sprint4_midpoint.md`                | 2026-04-22 | Adam        | 3 (Nasser/Abdurrahman async) | Google Meet |
| `2026-04-28_final_review.md`                    | 2026-04-28 | Adam        | All 5                | Hybrid (Adam + Floyd in person, others via Meet) |

Key decisions threaded through (post-ADR-006 reconciliation):
- Kickoff (2026-02-25): Python + Pygame + pytest tooling, roles assigned, two-week sprints with mid-point + review per cycle.
- Sprint 1 midpoint (2026-03-04): engine API to be frozen by sprint end; engine functions raise `ValueError`; `Card`/`Player`/`GameState` as dataclasses.
- Sprint 1 review (2026-03-09): Sprint 1 goal met, move to Sprint 2; Floyd takes Sprint 2 lead; deal-bug fixed live during demo.
- **Sprint 2 midpoint (2026-03-18): grid + dice and AI player KEPT in scope; Sprint 2 extended one week to absorb integration.** This is the meeting that ADR-006 documents.
- Team progress review (2026-03-25): self-assessment form; AI work in flight; team confirms with the customer that the AI deliverable is targeted at the upper code band.
- Sprint 2 review (2026-03-30): Sprint 2 goal met; 3 bugs found and fixed in-meeting (wrong-turn on `move_to_room`, eliminated-suggest order, draw-path on EndScreen).
- Sprint 3 midpoint (2026-04-08): **F12 token-position bug identified by Adam** as a real domain bug, added to Sprint 3 scope.
- Sprint 3 review (2026-04-13): F12 fix landed; AI work integrated; test count reached 113; move to Sprint 4.
- Sprint 4 midpoint (2026-04-22): video script and submission pack structure agreed; 18:00 2026-04-28 upload target.
- Final review (2026-04-28): peer review marks agreed (equal 20s); ZIP built and unzip-tested; final regression 114/114 (one dice-fairness test added during submission prep took the count from 113 to 114); tag `submission-2026-04-28` post-upload.

### 5.7 `docs/sprints/` (4 files, identical 7-section structure)

#### `sprint_1.md` — Foundation & Engine Core (2026-02-23 → 03-08)
Lead Maysarah. Stories F1–F3. Task cards TC1–TC5. Test count: 33 unit tests passing at sprint end. Bugs: deal-and-solution dropping solution cards back into deal pool — fixed live in review demo.

#### `sprint_2.md` — Core Gameplay Mechanics (2026-03-09 → 03-29, extended)
Lead Floyd. Stories F4–F8 plus the ADR-006 scope decision. Task cards TC6–TC11 cover human gameplay, dice + grid, and AI. Cumulative ~63 tests at sprint end. Three bugs fixed in-sprint (wrong-turn on `move_to_room`, eliminated-suggest order, EndScreen draw path). One-week sprint extension.

#### `sprint_3.md` — Robustness & Validation (2026-03-30 → 04-12)
Lead Maysarah. Stories F9–F16, F20–F24, NF2. Task cards TC12–TC20. **TC18 is the F12 token-position fix** (`GameState.suspect_locations` and `GameState.weapon_locations` dicts populated in `make_suggestion`). Test count reaches 113 (87 engine + 13 AI + 18 model + 5 typed-signature/regression). One regression caught (`next_turn` skip-count) before merge.

#### `sprint_4.md` — Polish, Demo & Submission (2026-04-13 → 04-29)
Lead Floyd. Code-freeze sprint with one critical bugfix permitted: **TC-25 — 3-line addition to `GameScreen._execute_suggestion` in `src/ui/screens.py`** that surfaces the F12 token movement in the in-game suggestion log. Final regression run on 2026-04-27 (113/113), then a Sprint 4 dice-fairness test (`test_roll_die_fairness_seeded`) was added during submission prep to cover the spec §7 fair-dice integrity requirement, taking the final count to **114**. Re-run on the unpacked submission ZIP also 114/114. Demo video took two attempts. Equal 20/20/20/20/20 peer review agreed without dispute.

### 5.8 `docs/report/` (3 files)

#### `requirements.md`
- Functional mandatory ("shall") F1–F16 plus **F4a** (door-tile rule: a player can only enter a room by ending their dice move on one of that room's defined door tiles, and cannot enter and exit the same room within a single dice move). F12 specifies token movement and persistence after refutation.
- **AI / autonomous-player requirements F20–F24:** Setup-screen toggle (F20), full automatic turn (F21), public-knowledge-only constraint (F22), single-candidate accusation rule (F23), TC-25 visibility line (F24).
- Functional desirable ("should") F17–F19 (EndScreen reveals solution, Play Again from EndScreen, `turn_history` records moves).
- Non-functional NF1 (clear prompts, errors surfaced), NF2 (no crash), NF3 (`pytest -q` < 5s), NF4 (engine no Pygame).
- Domain D1–D5 (21 cards, dealer puts one of each in envelope, suggestion uses room, one accusation per player, eliminated still refute).
- **Out-of-scope list:** save/load; networked multiplayer; animations / sound / mobile / web; detective-notes sheet rendered for human players. Grid + AI are no longer in this list.
- Final paragraph: "The total at submission is **114 unit tests** passing in well under one second."

#### `group_report.md` (8 sections)
§1 Project overview now describes the **AI player as delivered**, not descoped. §2 Team and roles + attendance table. §3 Sprint-by-sprint progress (Sprint 1 closed at 33 tests, Sprint 2 ~63 tests with one-week extension, Sprint 3 113 tests with F12 fix and AI integration, Sprint 4 freeze with TC-25 visibility bugfix and dice-fairness test addition for 114). §4 What went well (engine/UI/AI three-consumer architecture; clean ADR-006 scope decision; doc-pace-with-code; async process). §5 What did not go well (Sprint 2 needed an extension to absorb scope; uneven attendance; no automated GUI tests; demo retake). §6 What we would do differently (smaller PRs by layer; pin Python from Sprint 1; cohort-wide calendar; Pygame smoke test; continuous docstrings). §7 Outstanding issues lists F3 Miss Scarlet primacy (known limitation), no-automated-GUI-tests, and the canonical out-of-scope items from `requirements.md`. §8 Closing.

#### `peer_review.md`
Equal 20/20/20/20/20 split. Explicit non-zero confirmation for every member. Per-member contribution evidence pulled from sprint contribution tables. Sign-off recorded as agreed at the 2026-04-28 final review.

### 5.9 `docs/testing/system_test_report.md`

Conventions block. Requirement matrix (F1–F16, F4a, F17–F24, NF1, NF2 with one-line descriptions). System test rows (`ST-01` through `ST-NF2c` plus AI rows) covering every requirement, each with: Steps / Expected / Actual / Pass-Fail / Unit refs columns. F12 row `ST-12d-GUI` references screenshot `f12_evidence.png`. AI rows reference `tests/test_ai.py`.

---

## 6. Domain constants (canonical names — verified in `src/game/deck.py`)

- **Suspects (6):** Miss Scarlet, Colonel Mustard, Professor Plum, Reverend Green, Mrs. Peacock, Mrs. White.
  *(Not "Miss Scarlett" / "Col Mustard" / "Prof Plum" / "Rev Green" / "Mrs Peacock" / "Mrs White" as in the early `CLAUDE.md` §7.)*
- **Weapons (6):** Knife, Candlestick, Revolver, Rope, Lead Pipe, Wrench.
  *(Not "dagger" / "lead piping" / "spanner" as in `CLAUDE.md` §7. The team adopted the canonical Hasbro names; this is reflected in deck.py and across the requirements/system-test rows but `CLAUDE.md` itself is not edited.)*
- **Rooms (9):** Kitchen, Ballroom, Conservatory, Dining Room, Billiard Room, Library, Lounge, Hall, Study.

## 7. Key claims threaded across all docs (consistency map)

These claims appear in multiple documents and must remain consistent:

| Claim                                                                                  | Files asserting it                                            |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| 114 unit tests passing at submission                                                   | `README.md`, `sprint_4.md` §6, `report/requirements.md`, `report/group_report.md`, `testing/system_test_report.md`, `decisions.md` ADR-006 closing note |
| Sprint 3 closed at 113 tests; +1 dice-fairness test in Sprint 4 → 114                   | `sprint_3.md`, `sprint_4.md`, `decisions.md` ADR-004 cleanup note + ADR-006 |
| Engine has zero Pygame imports                                                         | `architecture.md`, `sprint_1.md`, `requirements.md` (NF4)     |
| Grid + dice movement and AI player KEPT in scope (reverses earlier descope draft)      | `decisions.md` ADR-006, `2026-03-18_sprint2_midpoint.md`, `sprint_2.md`, `architecture.md`, `requirements.md`, `group_report.md`, `project_plan.md` |
| F12 token-position bug identified Sprint 3 midpoint by Adam, fixed by Maysarah         | `2026-04-08_sprint3_midpoint.md`, `sprint_3.md` §3 TC18 + §5, `2026-04-13_sprint3_review.md`, `peer_review.md` |
| TC-25 Sprint 4 visibility bugfix in `src/ui/screens.py` (3-line `_execute_suggestion`)  | `sprint_4.md` §3 + §5, `peer_review.md`                       |
| Equal 20/20/20/20/20 peer review                                                       | `peer_review.md`, `group_report.md` §8, `2026-04-28_final_review.md` |
| Submission upload 18:00 2026-04-28 (22-hour buffer to 16:00 2026-04-30 deadline)        | `2026-04-22_sprint4_midpoint.md`, `2026-04-28_final_review.md`, `risk_register.md` (R8) |

## 8. Git state (snapshot taken 2026-04-30)

- Default branch on GitHub: `main`. PRs #8 and #9 (`ai-gamelog`) merged earlier added the AI module and the dice/grid engine extensions; commit `318f386 dice` was a follow-up on top.
- Local working tree is on `removing-ai-slop`, which has **no commits past `main`** but holds 34 files of uncommitted modifications (866 insertions / 668 deletions). These changes contain the doc rewrites described in §5 above and the corresponding code adjustments in `src/`. Nothing on this branch has been pushed.
- Untracked at repo root: `CURRENT_STATE.md` (this file), `code_review.md`, `REPO_LINK.txt`, `submission_docx/`, `submission_docx.zip`, `Cluedo_Team53_Documentation_docx/`, `.venv/`.
- The `removing-ai-slop` branch name is a working title from an earlier reconciliation pass; the doc/code rewrite that actually lives in the working tree **keeps the AI in scope** in line with ADR-006, despite the branch name.

## 9. Outstanding human-only artefacts

These were flagged in the handover as still pending at submission time. Status as of 2026-04-30:

- `docs/screenshots/` — `title.png`, `gameplay.png`, `end.png`, `f12_evidence.png`. Referenced from `README.md` and `system_test_report.md` (ST-12d-GUI). **Directory does not yet exist on disk.** Capturer: Nasser.
- Demo video (MP4). Recorder: Adam.
- Submission ZIP build, integrity check, Canvas upload. Driver: Adam. (`submission_docx.zip` exists but has not been verified against the submission spec by a human.)

## 10. Outstanding documented limitations (not blocking)

- **F3 Miss Scarlet primacy rule** not implemented — engine accepts free-text names, so the "Miss Scarlet goes first if present" tie-break is not enforced beyond first-listed-player. Documented in `group_report.md` §7.
- ADR-001: `rules.py` extraction deferred post-submission.
- ADR-004: `src/__init__.py` shim is deliberate technical debt with a remediation path.
- No automated GUI tests; engine + AI fully covered.
- `CLAUDE.md` itself was not edited as part of the ADR-006 reconciliation. The note at the top of `CLAUDE.md` (preserved verbatim) directs readers to `docs/decisions.md` ADR-006 for the current scope position.

---

## 11. Reconciliation instruction for Claude Code

**Goal:** confirm that the local working tree at `~/Desktop/SWECOURSEWORK2026` matches the canonical state described in this document, and decide whether to commit the `removing-ai-slop` working-tree edits before the 16:00 2026-04-30 deadline.

**Procedure:**

1. From the repo root, capture local state:
   ```
   git status
   git diff --stat HEAD
   ```
   Expected: branch `removing-ai-slop`; ~34 files modified vs `HEAD`; untracked entries match §4.
2. Verify the build:
   ```
   python -m pytest -q
   ```
   Expected: `114 passed`.
3. Verify the GUI launches:
   ```
   python -m src.main
   ```
   Expected: 1200 × 800 Pygame window opens at the title screen.
4. Confirm the running game matches the in-scope claims in §6 and §7:
   - Setup screen accepts 3–6 player names; **Human / AI toggle is present per slot**; mixed games allowed.
   - Game screen has a **Roll Dice button** that highlights reachable corridor tiles and reachable rooms via doors.
   - Suggestion log includes a token-movement line per TC-25 (e.g. "→ Miss Scarlet token moved to Kitchen").
   - In a mixed or all-AI game, the GUI auto-resolves AI turns and prints public actions to the log without leaking hand contents.
5. Confirm `docs/decisions.md` contains 6 ADRs (ADR-001 … ADR-006) and the Sprint 4 cleanup note about the 91 → 113 → 114 test-count drift.
6. If steps 2–5 pass, the working tree is at submission-ready state. Decide whether to:
   (a) commit the `removing-ai-slop` edits onto a fresh branch and merge to `main` before the deadline, or
   (b) ship the GitHub `main` snapshot as-is (note: that snapshot does **not** include the doc rewrites in §5).
7. Continue to the human-only artefacts in §9 (screenshots, demo video, ZIP upload).
