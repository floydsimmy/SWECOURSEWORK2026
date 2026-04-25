# Engineering Decisions Log

This file records deliberate deviations from the reference structure in `CLAUDE.md` and the project playbook (`4_sprints.pdf`), along with the engineering reasoning behind them. Each entry follows an ADR (Architecture Decision Record) format so that markers and future maintainers can audit our intent rather than infer it.

Decisions are append-only. If a decision is later reversed, add a new ADR with status `Superseded by ADR-NNN` rather than editing the original.

---

## ADR-001 — Rules logic remains inlined in `engine.py`

- **Status:** Accepted
- **Sprint:** 3 (closure)
- **References:** `CLAUDE.md` §3, §11; project playbook §5

### Context

The reference repository structure in `CLAUDE.md` §3 specifies a separate `src/game/rules.py` module alongside `src/game/engine.py`. In our codebase the rule predicates (move validity, suggestion eligibility, refutation order, accusation correctness) are implemented inline within `engine.py`.

### Decision

Defer the extraction of `rules.py` until after submission. `engine.py` will retain the inlined rule predicates for the remainder of Sprint 3 and through Sprint 4 code freeze.

### Rationale

1. Ninety-one unit tests currently pass against the inlined structure. A module split immediately before code freeze is a high-risk, zero-functional-gain change.
2. Sprint 3 per `CLAUDE.md` §13 is explicitly a hardening sprint. Sprint 4 is explicitly a freeze sprint. Refactoring belongs in neither.
3. The cohesion problem the split would solve — separating pure predicates from state-mutating operations — is real but low-impact at the current file size.
4. The class diagram in `docs/design/architecture.md` reflects the actual implementation, so the design documentation does not misrepresent the code.

### Consequences

- This is recorded as known technical debt. Future contributors extending the rule set should add to `engine.py` and consider the extraction at that point.
- If a marker requires the strict §3 layout, the refactor is mechanical: each rule predicate is already a free-standing function and can be moved with imports updated in a single pull request post-submission.

---

## ADR-002 — Documentation organised under topic subfolders

- **Status:** Accepted
- **Sprint:** 3 (closure)
- **References:** `CLAUDE.md` §3; project playbook §8

### Context

The reference structure in `CLAUDE.md` §3 specifies a flat `docs/` directory containing `requirements.md`, `architecture.md`, `decisions.md`, `system_test_report.md`, `meetings/`, and `sprints/`. Our actual layout groups documents by topic:

```
docs/
  planning/      # project plan, risks, resourcing
  design/        # architecture, class diagrams, sequence diagrams
  testing/       # unit and system test reports
  report/        # group report, peer assessment template
  meetings/      # meeting minutes (flat)
  sprints/       # sprint start and end docs (flat)
  decisions.md   # this file
```

### Decision

Retain the topic-subfolder structure. Add `docs/README.md` as an index mapping each playbook deliverable to its actual path, so any reader unfamiliar with our layout can locate documents without exploring directories.

### Rationale

1. The topic structure was established in Sprint 1 and is referenced from existing meeting minutes, sprint documents, commit messages, and pull request descriptions. Flattening at sprint close would invalidate cross-references project-wide.
2. The marking criteria (`Refined_Marking_Criteria.pdf`) assesses the *content* and *evidence* of each document type, not the directory layout.
3. An index file gives the discoverability benefit of a flat layout without the cost of rewriting cross-references.

### Consequences

- `docs/README.md` is now a required Sprint 4 deliverable.
- New documents must be filed under the correct topic subfolder and registered in the index.
- The reverse migration is a `git mv` plus index update; reversible if explicitly required.

---

## ADR-003 — Hand privacy interpreted in hot-seat context

- **Status:** Accepted
- **Sprint:** 3 (closure)
- **References:** `CLAUDE.md` §2, §7; user requirements document §7

### Context

The user requirements state that *"a player's hand is never shown to other players"* and `CLAUDE.md` §7 reiterates *"GUI must hide hands except for the active player."* Our `GameScreen` displays the active player's hand during their turn, on a single monitor shared with all players (hot-seat play).

### Decision

Treat the active-player-only display as a correct implementation of the privacy requirement in a hot-seat context. Non-active players' hands are never rendered. The privacy boundary is the turn boundary.

### Rationale

1. `CLAUDE.md` §2 explicitly excludes networked multiplayer from MVP. There is no separate per-player display surface to hide hands on.
2. The original board game has the same property: a player's hand is held in their physical hands, and players are expected to look away during another player's turn. The software cannot enforce this and is not required to.
3. Hiding the active player's hand from the active player would make the game unplayable.

### Consequences

- An optional inter-turn "pass the device to the next player" splash screen could be added in Sprint 4 as a polish item if time allows. It is not required to satisfy §7.
- This interpretation is documented so that markers do not read the always-on display of the active player's hand as a privacy bug.
- Strict per-player hidden displays would require networked multiplayer, which is out of MVP scope per `CLAUDE.md` §2.

---

## ADR-004 — `src/__init__.py` shim to support both run commands

- **Status:** Accepted
- **Sprint:** 3 (closure)
- **References:** `CLAUDE.md` §10 (Definition of Done item 4), §5

### Context

`CLAUDE.md` §10 item 4 specifies the canonical run command as `python -m src.main`. Our internal imports use bare absolute form (`from game.X import Y`, `from ui.X import Y`) rather than package-rooted form (`from src.game.X import Y`), because:

- `pytest.ini` configures `pythonpath = src`, which puts `src/` on the path during testing and lets the bare imports resolve.
- Running `python src/main.py` works for the same reason: Python adds the script's directory to `sys.path`.

However, `python -m src.main` runs from the project root with the project root on `sys.path`, not `src/`, so bare imports fail.

Switching every import to `from src.game.X import Y` would touch every source and test file at sprint close, with significant regression risk on a green test suite.

### Decision

Add a three-line shim to `src/__init__.py` that prepends the `src/` directory to `sys.path` on package import:

```python
"""Package shim: lets bare imports (`from game.X`, `from ui.X`) resolve
when the project is run as `python -m src.main` from the repository root.
Tests do not use this path because pytest.ini sets pythonpath = src directly."""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
```

### Rationale

1. Both `python -m src.main` (Definition of Done canonical) and `python src/main.py` (developer convenience) now work from a clean shell.
2. `pytest` configuration is unchanged. The 91-test green suite is unaffected.
3. The change is contained to a single file. No source or test imports change.
4. The shim is honest about its purpose: the docstring explains exactly what is happening for any reader.

### Consequences

- The shim mutates `sys.path` at import time, which is generally a code smell. We accept this trade-off because the alternative — a project-wide import refactor at code freeze — carries higher risk.
- If a future contributor refactors imports to `from src.game.X` form throughout, the shim becomes redundant and should be removed.
- This is recorded as deliberate technical debt with a clear remediation path.

---

## ADR-005 — Group report filed at `docs/report/group_report.md`, not `docs/group_report.md`

- **Status:** Accepted
- **Sprint:** 4
- **References:** `CLAUDE.md` §13 (Sprint 4 deliverables); ADR-002

### Context

`CLAUDE.md` §13 lists the Sprint 4 group report at the path `docs/group_report.md`. ADR-002 already established a topic-subfolder layout for `docs/`, with submission-final reporting under `docs/report/`.

### Decision

File the group report at `docs/report/group_report.md`, consistent with ADR-002.

### Rationale

Maintains the established layout; avoids relitigating ADR-002 at sprint close. Discoverability is preserved by the cross-reference table in `docs/README.md`, which maps the playbook's flat names to their actual subfolder locations.

### Consequences

A reader following `CLAUDE.md` §13 literally will not find `docs/group_report.md`; they need to consult `docs/README.md` once. If this is unacceptable to a marker, a one-line redirect file at the playbook path is a trivial future fix.

### Note (Sprint 4 cleanup) — test count drift since ADR-004

ADR-004 records the 91-test green suite as it stood when the `src/__init__.py` shim decision was made. The suite grew from 91 to 100 during Sprint 3's API-tightening work (F12 token-locations, seeded `new_game`, `Card`-typed signatures), and remained at 100 through Sprint 4. Per this file's append-only rule, ADR-004's "91" is preserved as a snapshot of the decision moment and is not retroactively edited.

---

*Future ADRs append below this line.*
