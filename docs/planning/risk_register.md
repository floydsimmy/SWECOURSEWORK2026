# Risk Register

Risks are scored on a 1-3 scale (1 = low, 3 = high). Score = L x I.
Anything scoring >= 6 was actively monitored every sprint review.

| ID  | Risk                                          | L | I | S | Mitigation                                                                    | Status (end of project) |
| --- | --------------------------------------------- | - | - | - | ----------------------------------------------------------------------------- | ----------------------- |
| R1  | Only two coders bottleneck delivery           | 3 | 3 | 9 | QA writes system tests; PO + Scrum produce all docs; devs only write code     | Held; non-coders wrote tests + docs in parallel |
| R2  | Engine / GUI integration breaks late          | 2 | 3 | 6 | Engine API frozen in Sprint 1; integration smoke-test on every PR             | Held; integration was clean from Sprint 2 onwards |
| R3  | Pygame quirks on Windows                      | 2 | 2 | 4 | Use built-in default font; develop on Windows; SDL_VIDEODRIVER=dummy in tests | Held; no platform issues |
| R4  | Scope creep (board grid, AI, save games)      | 3 | 2 | 6 | PO owns backlog; stretch goals are explicitly out of MVP                      | Held; grid + AI descoped in Sprint 2 with PO sign-off |
| R5  | Documentation gap at the end                  | 2 | 3 | 6 | DoD requires doc update each sprint                                            | Held; submission pack assembled progressively |
| R6  | Team member inactive                          | 2 | 3 | 6 | Meeting notes record attendance; tasks reassignable each sprint               | Held; full attendance throughout |
| R7  | Tests rot as engine evolves                   | 1 | 2 | 2 | `pytest -x -q` gates every merge to main                                      | Held; 91 tests green at submission |
| R8  | Marker cannot run the code                    | 2 | 3 | 6 | One-line install (`python -m pip install pygame pytest`); README spells it out    | Mitigated; instructions in `docs/README.md` |

## Risks that fired

- **R4 (scope creep)** fired mid-Sprint-2 when one team member started
  building grid-based movement. The PO closed it the same week and
  re-scoped to dropdown room selection. No code was lost (the work
  lives on a feature branch that did not merge).

- **R7 (tests rot)** fired once during Sprint 3 when a bug fix to
  `next_turn` broke the elimination test. Caught on the next `pytest`
  run before merge.

No other risk fired with material impact.
