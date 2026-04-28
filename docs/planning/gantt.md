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
T9  Accusation + win/lose                          [##]
T10 Setup/Game/End screens                       [####]
T11 UI components                                [###]
T12 System tests F4-F8                              [##]

T13 Validation guards                                              [##]
T14 F12 fix                                                          [#]
T15 UI polish                                                        [##]
T16 validate_game_state                                              [#]
T17 System tests F9-F16, NF2                                          [##]

T18 Regression + freeze                                                              [##]
T19 Demo video                                                                         [#]
T20 Group report + peer review                                                         [##]
T21 Screenshots                                                                          [#]
T22 Submission ZIP                                                                       [##]
```

`[#]` ≈ one day of effort. Brackets show the sprint window in which the task lives, not the exact calendar day.

## Critical path

`T1 → T2 → T4 → T8 → T9 → T13 → T14 → T16 → T17 → T18 → T22`

If any of these slip, the next sprint starts late. T8 (Move / Suggest / Refute) and T10 (screens) ran in parallel during Sprint 2, but only T8 is on the critical path because the GUI is meaningless without it.

## Sprint 2 extension

The Gantt above shows Sprint 2 at its actual 21-day length. The original plan had Sprint 2 at 14 days (ending 22 March) and Sprint 3 starting 23 March. The midpoint meeting on 18 March agreed to extend Sprint 2 by one week to absorb integration work; Sprint 3 and Sprint 4 windows were shifted accordingly. The plan-versus-actual discussion is in `docs/planning/project_plan.md` §6.
