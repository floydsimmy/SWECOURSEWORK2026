# Gantt Chart (text rendering)

```
Sprint 1 (Feb 2 - Feb 15)              Sprint 2 (Feb 16 - Mar 1)         Sprint 3 (Mar 2 - Mar 15)         Sprint 4 (Mar 16 - Mar 29)
|---------------------------------|   |---------------------------|     |---------------------------|     |---------------------------|

T1  Engine API contract        [##]
T2  Models                       [##]
T3  Deck                          [#]
T4  Engine core                   [###]
T5  Pygame skeleton                  [##]
T6  Unit tests F1-F3                  [##]
T7  Move/suggest/refute                  [###]                 |
T8  Accusation + win/lose                                 [##] |
T9  Screens                                              [####]
T10 Wire UI -> engine                                      [##]
T11 System tests F1-F8                                       [##]

T12 Validation guards                                                 [##]
T13 Last standing + draw                                                [#]
T14 turn_summary + history                                              [#]
T15 UI polish                                                           [##]
T16 validate_game_state                                                  [#]

T17 Regression + bug fix                                                              [##]
T18 Video demo                                                                          [#]
T19 Group report + peer review                                                          [##]
T20 Submission pack                                                                       [#]
```

`[#]` = ~1 day of effort. The brackets show the sprint window in which
the task lives, not the exact calendar day.

## Critical path

`T1 -> T2 -> T4 -> T7 -> T8 -> T12 -> T13 -> T16 -> T17 -> T20`

If any of those slips, the next sprint starts late. T7 (suggestion +
refutation) and T9 (screens) ran in parallel during Sprint 2 but only
T7 is on the critical path because the GUI is meaningless without it.
