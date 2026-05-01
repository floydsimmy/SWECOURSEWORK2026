# Gantt Chart (text rendering)

```
               Feb 23                Mar 9                  Mar 30               Apr 13               Apr 29
               |                     |                      |                    |                    |
               |--Sprint 1 (14d)----||--Sprint 2 (21d)------||--Sprint 3 (14d)---||--Sprint 4 (17d)----|

T1  Engine API contract           [##]
T2  Models                          [##]
T3  Deck                              [#]
T4  Engine core                      [###]
T5  Pygame skeleton                  [##]
T6  Title-screen mockups               [#]
T7  Unit tests F1-F3                  [##]
T8  Move/Suggest/Refute                       [###]
T8b Grid + dice movement (BFS, board layout) [###]
T9  Accusation + win/lose                          [##]
T10 Setup/Game/End screens (incl Human/AI tog.)  [####]
T11 UI components + Board renderer               [###]
T12 System tests F4-F8                              [##]

T13 Validation guards                                              [##]
T14 F12 fix                                                          [#]
T14b AI player module + tests/test_ai.py                              [##]
T15 UI polish                                                        [##]
T16 validate_game_state                                              [#]
T17 System tests F9-F16, NF2, F20-F23                                 [##]

T18 Regression + freeze                                                              [##]
T19 Demo video                                                                         [#]
T20 Group report + peer review                                                         [##]
T21 Screenshots                                                                          [#]
T22 Submission ZIP                                                                       [##]
```

`[#]` ≈ one day of effort. Brackets show the sprint window in which the task lives, not the exact calendar day.

## Critical path

`T1 → T2 → T4 → T8 → T9 → T13 → T14 → T14b → T16 → T17 → T18 → T22`

If any of these slip, the next sprint starts late. T8 (Move / Suggest / Refute) and T8b (grid pathing) ran in parallel during Sprint 2; only T8 sits on the critical path because the GUI is meaningless without the rules. T14b (AI module) sits on the critical path in Sprint 3 because it was the largest single deliverable of the sprint after F12.

## Sprint 2 extension

The Gantt above shows Sprint 2 at its actual 21-day length. The original plan had Sprint 2 at 14 days (ending 22 March) and Sprint 3 starting 23 March. The midpoint meeting on 18 March agreed to extend Sprint 2 by one week to absorb the integration work for grid + dice movement and the keep-in-scope decision for the AI player (ADR-006). Sprint 3 and Sprint 4 windows shifted accordingly. The plan-versus-actual discussion is in `docs/planning/project_plan.md` §6.
