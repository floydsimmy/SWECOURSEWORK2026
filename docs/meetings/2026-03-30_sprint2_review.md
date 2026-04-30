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

- Grid + dice movement and the AI player both kept in scope at the midpoint (ADR-006 in `docs/decisions.md`); AI deferred to Sprint 3.
- Sprint 2 extended by one week; ending today.

## 2) Issues discussed at this meeting

- Live demo: a full 3-player game played end-to-end during the meeting. Roll Dice → click destination → Suggest → Accuse flows working. EndScreen showing the winner.
- Bugs surfaced during the demo and the QA pass:
  - Wrong-turn protection was missing on `move_to_room` — non-current players could move on someone else's turn. Fixed in-meeting (Maysarah).
  - Eliminated player could still attempt to suggest because the room check ran before the eliminated check. Fixed.
  - End screen showed "None" as winner when the game ended by all players being eliminated. Fixed by adding an explicit "draw" path.
  - Floyd flagged a suspected off-by-one in the dice-roll BFS — need to write a tighter system test in Sprint 3 to confirm.
- Abdurrahman reported the system test report now has rows for F4–F8 with linked unit tests; the F4 row is currently a "happy path" only and will be tightened in Sprint 3.
- Adam flagged that the team is short on edge-case validation tests — needs to push hard in Sprint 3 to cover invalid inputs, wrong-turn errors, action-after-game-over, etc. — and that the AI module deferred from Sprint 2 should land in Sprint 3 alongside the hardening work.

## 3) Decisions agreed at this meeting

- Sprint 2 goal met (with the one-week extension). Move to Sprint 3.
- **Sprint 3 goal: hardening (input validation, edge cases, end-game polish) + the AI player module deferred from Sprint 2.** (Action: Maysarah, Abdurrahman.)
- Sprint 3 technical lead: Maysarah (engine + AI work).
- Floyd and Nasser to polish EndScreen, fix the dice-roll BFS off-by-one, and add a message-history panel to GameScreen.
- Abdurrahman to expand the unit test suite to cover validation, edge cases, and the new AI behaviour as Maysarah lands it.
- Adam to draft the group-report skeleton and the AI requirements F20–F23 for the Sprint 3 acceptance criteria.

## 4) Date of next meeting

2026-04-08, Sprint 3 midpoint, Google Meet.

END
