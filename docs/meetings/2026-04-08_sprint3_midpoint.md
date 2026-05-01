# Team Meeting — Sprint 3 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd                                            |
| Members absent       | Maysarah (illness; sent written update via Discord), Nasser, Abdurrahman (both clashing with another module's coursework deadline; updates via Discord) |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-04-08, 17:00–17:30                                |
| Meeting co-ordinator | Adam                                                   |

## 1) Matters to note from last meeting

- Sprint 3 is hardening-focused; no new features.
- Group report skeleton drafted.

## 2) Issues discussed at this meeting

Short meeting due to attendance. Adam and Floyd reviewed the written updates from the absent members and walked through current state.

- Maysarah's written update: validation work in progress — invalid suspect/weapon names rejected, wrong-turn guard added to all action functions, `validate_game_state` and `verify_deck` next. Once those land she will start the AI module that ADR-006 deferred from Sprint 2.
- Floyd reported the EndScreen and message-history panel are both finished, and the dice-roll BFS off-by-one identified at the Sprint 2 review is now fixed.
- **F12 token-position bug discussed.** The user requirements say the suggested suspect and weapon should be moved into the room when a suggestion is made, and remain there afterwards. The current engine doesn't track token positions at all — only player positions. Adam (PO) confirmed this is a real domain bug, not a documentation gap. Floyd to flag it to Maysarah for Sprint 3 closure ahead of the AI work.
- Abdurrahman's written update: 70+ unit tests passing, working through edge-case rows in the system test report. Plans an AI behaviour test pass once `tests/test_ai.py` lands.

## 3) Decisions agreed at this meeting

- F12 token-position fix to be added to Sprint 3 scope ahead of the AI module. (Action: Maysarah, when she's back from illness.)
- Floyd to start Sprint 4 planning in parallel — submission pack, video planning, screenshot list. (Action: Floyd.)
- Adam to follow up with Maysarah and Abdurrahman async on Discord with the F12 details and to write up the AI requirements F20–F23 for the Sprint 3 acceptance criteria.

## 4) Date of next meeting

2026-04-13, Sprint 3 review, Google Meet.

END
