# Team Meeting — Sprint 2 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah, Nasser, Abdurrahman             |
| Members absent       | None                                                   |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-03-30, 18:00–19:15                                |
| Meeting co-ordinator | Floyd                                                  |

## 1) Matters to note from last meeting

- Grid movement and AI both descoped (decisions logged in `docs/decisions.md`).
- Sprint 2 extended by one week; ending today.

## 2) Issues discussed at this meeting

- Live demo: a full 3-player game played end-to-end during the meeting. Suggestion and accusation flows working. EndScreen showing the winner.
- Bugs surfaced during the demo and the QA pass:
  - Wrong-turn protection was missing on `move_to_room` — non-current players could move on someone else's turn. Fixed in-meeting (Maysarah).
  - Eliminated player could still attempt to suggest because the room check ran before the eliminated check. Fixed.
  - End screen showed "None" as winner when the game ended by all players being eliminated. Fixed by adding an explicit "draw" path.
- Abdurrahman reported the system test report now has rows for F4–F8 with linked unit tests.
- Adam flagged that the team is short on edge-case validation tests — needs to push hard in Sprint 3 to cover invalid inputs, wrong-turn errors, action-after-game-over, etc.

## 3) Decisions agreed at this meeting

- Sprint 2 goal met (with the one-week extension). Move to Sprint 3.
- **Sprint 3 goal: hardening — input validation, edge cases, end-game polish. No new gameplay features.** (Action: Maysarah, Abdurrahman.)
- Sprint 3 technical lead: Maysarah (engine-focused work).
- Floyd and Nasser to polish EndScreen and add a message-history panel to GameScreen.
- Abdurrahman to expand the unit test suite to cover validation and edge cases as Maysarah lands them.
- Adam to draft the group-report skeleton.

## 4) Date of next meeting

2026-04-08, Sprint 3 midpoint, Google Meet.

END
