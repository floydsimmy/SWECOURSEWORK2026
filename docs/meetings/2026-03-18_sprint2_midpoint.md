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

- Suggestion and refutation rules implementation status. Maysarah confirmed the refutation walk works (player order from the suggester's left, including eliminated players per D5). Tests passing.
- **Scope question raised by Floyd: grid-based board movement and the AI player.** Floyd had a tile-based pathing prototype running and asked whether the team should commit fully or step back to a dropdown room selector. Adam (PO) read the user requirements and the marking criteria again on the call. Both items are in the user requirements; the marking criteria places the AI deliverable in the upper 41–50 code band; replacing tile movement with a dropdown would walk away from Cluedo's identity. The team weighed the time risk against the score upside and **agreed to keep both in scope**. Floyd to deliver the grid + dice pathfinder this sprint; the AI module deferred to Sprint 3 once the engine is hardened.
- ScreenManager state-sharing. Floyd proposed a class attribute on `ScreenManager` to hold the current `GameState`. Pragmatic for a single-game prototype; agreed.
- Sprint 2 is running long. Likely to extend by a week into the following Monday.

## 3) Decisions agreed at this meeting

- **Grid + dice movement KEPT in MVP scope.** Sprint 2 will deliver `roll_die`, `legal_moves_for_roll` (BFS over corridor tiles), `move_by_dice`, and the static board layout tables. (PO sign-off: Adam. Owner: Floyd.)
- **AI player KEPT in scope, deferred to Sprint 3.** The Sprint 3 lead will own it. (PO sign-off: Adam. Owner: Maysarah.)
- ADR-006 to be filed today by Adam, capturing the rationale (marking criteria leverage, identity of Cluedo, time risk acceptable). (Action: Adam, completed during the meeting.)
- Sprint 2 to extend by one week (now ending 29 March instead of 22 March) to absorb the additional integration work. (Action: Adam to update sprint planning docs.)
- Floyd to ship SetupScreen (with per-slot Human/AI toggle, ready for Sprint 3 wiring) and GameScreen by 26 March. (Action: Floyd, Nasser.)
- Maysarah to finish accusation auto-advance and `check_for_winner` by 25 March. (Action: Maysarah.)

## 4) Date of next meeting

2026-03-30, Sprint 2 review, Google Meet.

END
