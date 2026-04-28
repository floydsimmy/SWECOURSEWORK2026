# Team Meeting — Sprint 2 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah                                  |
| Members absent       | Nasser, Abdurrahman (both flagged on Discord that they had clashes; would catch up async) |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-03-18, 17:00–18:00                                |
| Meeting co-ordinator | Adam                                                   |

## 1) Matters to note from last meeting

- Sprint 2 backlog assigned and underway.
- System test report skeleton created by Abdurrahman.

## 2) Issues discussed at this meeting

- Suggestion and refutation rules implementation status. Maysarah confirmed the refutation walk works (player order from the suggester's left, skipping eliminated). Tests passing.
- **Scope question raised by Floyd: should we attempt grid-based board movement?** Floyd had explored a tile-based prototype during the week. Adam (PO) read the user requirements again on the call and ruled it out of MVP scope — the requirements allow simplification, and the time risk was too high mid-sprint. Decision recorded.
- **AI player.** Same conversation: stretch goal in the marking criteria, descoped indefinitely. Effort to be redirected into validation and the system test report.
- ScreenManager state-sharing. Floyd proposed a class attribute on ScreenManager to hold the current `GameState`. Pragmatic for a single-game prototype; agreed.
- Sprint 2 is running long. Likely to extend by a week into the following Monday.

## 3) Decisions agreed at this meeting

- **Grid-based movement DROPPED from MVP scope.** Replaced with dropdown room selection. (PO sign-off: Adam.)
- **AI player DROPPED from scope.** (PO sign-off: Adam.)
- Sprint 2 to extend by one week (now ending 29 March instead of 22 March) to absorb the additional integration work. (Action: Adam to update sprint planning docs.)
- Floyd to ship SetupScreen and GameScreen by 26 March. (Action: Floyd, Nasser.)
- Maysarah to finish accusation auto-advance and `check_for_winner` by 25 March. (Action: Maysarah.)

## 4) Date of next meeting

2026-03-30, Sprint 2 review, Google Meet.

END
