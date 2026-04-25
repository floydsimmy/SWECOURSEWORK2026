# CLAUDE.md — Project Context for Claude Code

> **Read this file in full before doing anything.** This is the source of truth for what we are building. If a request conflicts with anything here, stop and ask before proceeding. Do not infer scope from your training data — infer it only from this document and the user's explicit instructions.

---

## 1. What this project IS

A **Cluedo (Clue!) game in Python with a Pygame GUI**, built as a university Software Engineering coursework deliverable by a 5-person team across **4 sprints**. The grading is on the engineering process (sprints, tests, design docs) as much as the code itself.

- **Language:** Python 3.10+
- **GUI:** Pygame (only — no Tkinter, no PyQt, no web framework, no Unity, no Java port)
- **Tests:** pytest
- **Players:** 3–6 **local human** players, turn-based, hot-seat on one machine
- **Architecture:** strict separation between a **rules engine** (pure Python, no Pygame imports) and a **Pygame GUI layer** that calls the engine's API

## 2. What this project is NOT (do not add these)

These are **out of scope for the MVP**. Do not add them, do not scaffold for them, do not write "TODO: AI player" comments, do not import libraries for them.

- ❌ AI / autonomous players (the spec mentions one, but it is **explicitly deferred** until MVP passes system tests)
- ❌ Full 2D board movement with coordinate grid, doors, secret passages, dice-distance pathing
- ❌ Network / online multiplayer
- ❌ Save/load games
- ❌ Detective notes sheet
- ❌ Animations, sound effects, sprite art, particle effects
- ❌ Database backend, ORM, SQL
- ❌ Any web technology (Flask, FastAPI, React, HTML)
- ❌ Mobile build
- ❌ Any language other than Python

If the user asks for one of the above, confirm explicitly that they want to extend the MVP scope, and update `docs/decisions.md` before writing code.

## 3. Repo structure (do not reorganise without asking)

```
cluedo/
  src/
    game/
      models.py        # Card, Player, GameState, RefuteResult, AccusationResult
      engine.py        # new_game, move_to_room, make_suggestion, make_accusation, next_turn
      deck.py          # create_deck, deal, solution selection
      rules.py         # rule predicates / validators
    ui/
      gui.py           # Pygame app shell + main loop
      screens.py       # title, setup, main game, end screen
      components.py    # buttons, card widgets, hand display
      assets/
    main.py            # entrypoint
  tests/
    test_engine.py
    test_models.py
  docs/
    requirements.md
    architecture.md
    decisions.md
    system_test_report.md
    meetings/
    sprints/
  README.md
  pyproject.toml (or requirements.txt)
```

## 4. Architectural rules (non-negotiable)

1. **`src/game/` must not import `pygame` or anything from `src/ui/`.** The engine is headless and must be runnable and testable without a display.
2. **`src/ui/` must not contain game rules.** No card-dealing, no refutation logic, no win checks in the UI layer. UI calls engine functions and renders results.
3. **All engine functions are deterministic given a seed.** Use `random.Random(seed)` injected into `new_game` for reproducible tests.
4. **No global state.** Pass `GameState` through function calls.
5. **Type hints everywhere** in `src/game/`. The engine API is the contract between the two programmers.

## 5. Engine API (this is the contract — do not change signatures without updating `docs/architecture.md`)

```python
new_game(player_names: list[str], seed: int | None = None) -> GameState
get_hand(state: GameState, player: Player) -> list[Card]
move_to_room(state: GameState, player: Player, room: Room) -> None
make_suggestion(state: GameState, player: Player, suspect: Card, weapon: Card) -> RefuteResult
make_accusation(state: GameState, player: Player, suspect: Card, weapon: Card, room: Card) -> AccusationResult
next_turn(state: GameState) -> None
```

## 6. Functional requirements (cite these IDs in commit messages and tests)

- **F1** Game setup selects 1 suspect + 1 weapon + 1 room as the hidden solution
- **F2** Remaining 18 cards are dealt evenly clockwise to players (some may get one more — that is allowed)
- **F3** Turn order cycles correctly clockwise; Miss Scarlett goes first if present
- **F4** Player can move to a room (simplified — pick a room from a list, no grid pathing)
- **F5** Player can make a suggestion using their **current room** (room card is implicit, suspect + weapon chosen)
- **F6** Other players, in clockwise order from the suggester, refute by showing **one** matching card if they have any of the three suggested cards. Refutation is private to the suggester.
- **F7** Player can make an accusation; correct accusation wins the game
- **F8** Wrong accusation eliminates the player from making further accusations, but they remain in play to refute others' suggestions
- **NF1** Pygame GUI is usable: clear prompts, buttons, error messages, readable fonts
- **NF2** Game runs without crashing on any valid user action

## 7. Domain rules from the user requirements

- 6 suspects: Col Mustard, Prof Plum, Rev Green, Mrs Peacock, Miss Scarlett, Mrs White
- 6 weapons: dagger, candlestick, revolver, rope, lead piping, spanner
- 9 rooms: Study, Hall, Lounge, Library, Billiard Room, Dining Room, Conservatory, Ballroom, Kitchen
- 21 cards total → 3 go in the murder envelope → 18 are dealt
- A suggestion **moves the named suspect and weapon into the suggester's current room** and they stay there (this was a known fail in Sprint 2 — must be fixed)
- Players cannot retire from the game
- Privacy: a player's hand is never shown to other players. The GUI must hide hands except for the active player.

## 8. Current state of the project

A previous Claude Code session drifted out of scope, so the codebase may be partially correct, fully unusable, or empty. **Do not assume.** At the start of every session, ask the user:

1. Which sprint are we in (1, 2, 3, or 4)?
2. What is the state of the codebase — empty / partial / runnable?
3. Are there known open bugs to carry forward?

Only then proceed. The full sprint plan is in §13. The most commonly-carried bug to be aware of is **F12**: when a suggestion is made, the named suspect and weapon must move into the suggester's current room and remain there afterwards. If the user reports this is unfixed, slot it into the current sprint.

## 9. How to behave when working on this codebase

- **Before writing code**, restate in one or two sentences which requirement ID(s) the change addresses and which sprint it belongs to. If you can't, ask.
- **One change at a time.** Don't refactor while adding a feature. Don't add features while fixing a bug.
- **Tests are part of done.** A new engine function ships with pytest tests in the same change. A new GUI screen ships with at least one entry in `docs/system_test_report.md`.
- **Do not invent requirements.** If the user asks for something that isn't in §6 or §7, ask whether to add it to `docs/decisions.md` first.
- **Do not delete or rename existing engine functions** without asking — the GUI calls them and the QA tests reference them.
- **When unsure about scope, default to LESS, not more.** A smaller working change is always better than a larger speculative one.
- **No "improvements" the user did not ask for.** No swapping Pygame for another library, no "while I was here I also...", no premature optimisation, no adding type-checkers / linters / CI configs unless explicitly requested.

## 10. Definition of Done (for any task)

A change is done only when:

1. It matches the acceptance criteria of a specific requirement ID
2. Unit tests exist for engine changes (pytest, in `tests/`)
3. A system test case exists in `docs/system_test_report.md` for user-visible changes
4. `main` still runs (`python -m src.main` launches the game without error)
5. The relevant sprint doc in `docs/sprints/` is updated with what was delivered

## 11. If you are about to do any of the following, STOP and ask first

- Adding a dependency to `requirements.txt` / `pyproject.toml`
- Creating a new top-level directory
- Importing pygame inside `src/game/`
- Touching files in `docs/sprints/` for a sprint that is already closed
- Writing more than ~150 lines of code in a single response without checkpoints
- Anything labelled "out of scope" in §2

## 12. Standard prompts the user will send — recognise and respond to these

The user has a small set of prompts they reuse across sessions. When you see one, treat it as a direct instruction grounded in this file. Do not treat any of them as casual conversation.

### 12.1 The session opener

The user will start most sessions with a message that asks you to read `CLAUDE.md` in full, then:
1. Confirm you have read it.
2. State which requirement ID (F1–F8 / NF1–NF2) or known bug you understand them to be asking about.
3. Flag anything in their request that conflicts with §2 (out of scope) or §4 (architectural rules).
4. **Wait for explicit confirmation before writing code.**

When you see this opener, do exactly that. Do not skip step 4. Do not start coding "to save time". A one-line acknowledgement plus the task restatement is the entire correct response — nothing more.

### 12.2 The drift-correction prompt

If the user sends something like *"Stop. Re-read `CLAUDE.md` §2 and §9. Tell me which rule you were about to break, then propose a smaller change that stays inside scope,"* it means you have started to drift — almost certainly by expanding scope, refactoring unprompted, or breaking the engine/UI boundary in §4.

Respond by:
1. Stopping all in-progress work immediately.
2. Naming the specific rule from §2, §4, §9, or §11 you were about to violate.
3. Proposing a strictly smaller change that addresses only the originally-requested requirement ID.
4. Waiting for confirmation before continuing.

Do not defend the previous direction. Do not argue that the larger change is "cleaner" or "more idiomatic". The user has decided it is out of scope; that decision is final unless they reverse it in writing.

### 12.3 The Definition-of-Done check

If the user sends something like *"Check the change against `CLAUDE.md` §10. List which of the 5 criteria are met and which are not,"* go through §10 item by item — `1.` acceptance criteria, `2.` unit tests, `3.` system test entry, `4.` `main` still runs, `5.` sprint doc updated — and answer met / not met / partial for each, with a one-line justification per item. Do not declare the change done if any item is "not met" or "partial".

### 12.4 Anything else

Treat any prompt that explicitly references a `CLAUDE.md` section number (e.g. "per §5", "see §7") as a direct quote from this file. Re-read the cited section before answering.

## 13. Sprint-by-sprint scope (do not jump ahead)

Claude Code is driving all four sprints. **Complete each sprint fully and get explicit user sign-off before starting the next.** If the user is mid-sprint, stay in that sprint's scope until they confirm it is closed.

### Sprint 1 — Foundation & Engine Core

**Goal:** A headless Cluedo engine that sets up a game and cycles turns, plus a blank Pygame window that opens and closes cleanly.

**Allowed to create / modify in this sprint:**
- `src/game/models.py`, `src/game/deck.py`, `src/game/engine.py`, `src/game/rules.py`
- `src/main.py` and a skeleton `src/ui/gui.py` (blank window + game loop only)
- `tests/test_models.py`, `tests/test_engine.py` (covering F1–F3)
- `docs/architecture.md`, `docs/requirements.md`, `docs/decisions.md`
- `docs/sprints/sprint_1_start.md`, `docs/sprints/sprint_1_end.md`
- `docs/system_test_report.md` (initial entries for F1–F3)
- `pyproject.toml` or `requirements.txt`, `README.md`

**Must produce:**
- The full engine API from §5, fully type-hinted
- `new_game(player_names, seed=None)` returns a valid `GameState` with solution chosen and remaining cards dealt
- `next_turn(state)` cycles players in correct clockwise order, Miss Scarlett first if present
- `python -m src.main` opens and cleanly closes a Pygame window
- Pytest suite green for F1–F3
- Sprint 1 start and end docs filled in

**Done when:** `pytest` passes, the window runs, F1–F3 are recorded as Pass in the system test report, and the user confirms.

**Do not in this sprint:** suggestions, refutations, accusations, GUI screens beyond the blank window, anything from §2.

### Sprint 2 — Core Gameplay Mechanics

**Goal:** A complete game playable end-to-end through the Pygame GUI with 3–6 hot-seat players.

**Allowed to create / modify (in addition to Sprint 1's paths):**
- `src/ui/screens.py`, `src/ui/components.py` (title, setup, main game, end screen)
- `src/ui/assets/` (placeholder shapes/colours only — no commissioned art)
- Extensions to `tests/` for F4–F8
- Extensions to `docs/system_test_report.md` for F4–F8
- `docs/sprints/sprint_2_start.md`, `docs/sprints/sprint_2_end.md`

**Must produce:**
- `make_suggestion`, `make_accusation`, `move_to_room` fully working per §5
- F12 implemented correctly: suggested suspect and weapon move into the suggester's current room and stay
- Title screen, setup screen (player name entry), main game screen with private hand display + action buttons + clear turn indicator, end screen with winner
- Hand privacy: only the active player sees their hand
- ≥15 unit tests passing across the engine
- F4–F8 recorded in `system_test_report.md` with Pass/Fail and screenshots where useful

**Done when:** A full game can be played start-to-finish with no crashes, all engine tests green, F1–F8 system tests recorded, sprint end doc complete, user confirms.

**Do not in this sprint:** AI players, polish work (that is Sprint 3), end-of-game animations, save/load, anything from §2.

### Sprint 3 — Robustness & Usability

**Goal:** A stable, validated, polished MVP. Every Sprint 2 bug closed. This is a hardening sprint, not a feature sprint.

**Allowed to create / modify (in addition to Sprint 2's paths):**
- New widgets in `src/ui/components.py` for clearer feedback, error messages, button states
- Edge-case and regression tests in `tests/`
- NF1 and NF2 entries in `docs/system_test_report.md` plus a full regression pass
- `docs/sprints/sprint_3_start.md`, `docs/sprints/sprint_3_end.md`
- Updates to `docs/architecture.md` if the API genuinely changed (note any change in `docs/decisions.md`)

**Must produce:**
- Input validation on every interactive screen — invalid inputs produce a visible error, never a crash
- Clear turn summaries: who suggested what, who refuted, what happened — without leaking private information
- End-of-game screen with winner announcement and "play again" option that cleanly resets state
- Edge cases: last-player-standing wins by default; all-eliminated produces a draw
- Visual polish: consistent colour scheme, readable fonts, hover/active button states
- Every Sprint 2 bug (including F12 if still open) closed and re-tested
- NF1 and NF2 recorded as Pass

**Done when:** Full regression passes, no crashes on any valid input, all logged bugs closed, sprint end doc complete, user confirms.

**Do not in this sprint:** new features, new requirements, scope expansion, anything from §2.

### Sprint 4 — Polish, Demo & Submission

**Goal:** Submission-ready build. **Code freeze except for critical bugfixes.**

**Allowed to create / modify:**
- Critical bugfix-only changes to `src/`
- `README.md` (final polish: install, run, controls, screenshots)
- `docs/system_test_report.md` (final fill-in: every requirement Pass/Fail with evidence)
- `docs/sprints/sprint_4_start.md`, `docs/sprints/sprint_4_end.md`
- `docs/group_report.md` (draft only — see §13.5)
- A code snapshot directory if the team wants one preserved

**Must produce:**
- F1–F8 and NF1–NF2 all marked Pass in the system test report, or explicitly marked Fail with reasoning and what would be done about it
- Final `README.md` with install instructions, how to run, controls, and screenshots
- `docs/group_report.md` draft covering: what was built, sprint-by-sprint progress, what went well, what didn't, what the team would do differently, individual contributions framework (with `[TEAM TO FILL IN]` markers — see §13.5)
- A clean `main` branch that runs without warnings

**Done when:** the submission checklist in `4_sprints.pdf` §14 is complete except for items only humans can produce (see §13.5), and the user confirms the build is frozen.

**Do not in this sprint:** add features, refactor, touch anything outside bugfix and documentation scope. If a defect is too large for a bugfix, raise it to the user — do not silently scope-creep.

### 13.5 Things Claude Code cannot produce in any sprint

These require human input and **must not be fabricated**:

- **Meeting minutes.** They record real events between real people. Claude can produce blank templates with `[TEAM TO FILL IN]` markers; the team supplies actual content.
- **Peer assessment marks.** This is a team agreement. Claude can explain the playbook's distribution rule and produce a template, nothing more.
- **The video demo.** Must be recorded by a human running the game.
- **Specific named contributions.** Do not write "Floyd implemented X" or "Maysarah did Y" unless the user has explicitly stated it in this session. Use `[CONTRIBUTOR NAME]` placeholders otherwise.

If asked to fabricate any of the above, refuse and explain why.

---

**End of CLAUDE.md.** When you have read this, acknowledge with a single line stating which requirement ID or sprint task you are about to work on, then wait for confirmation before writing code. If the user's first message is the session opener from §12.1, follow §12.1 exactly. If sprint state is unclear, ask the §8 questions first.
