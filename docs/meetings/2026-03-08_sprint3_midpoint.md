# Team Meeting — Sprint 3 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | In person                                              |
| Date and time        | 2026-03-08, 14:00-14:35                                |
| Meeting co-ordinator | Member E                                               |

## 1) Matters to note from last meeting

- Wrong-turn guard added to all action functions.
- EndScreen now reveals the solution and offers Play Again / Main Menu.

## 2) Issues discussed at this meeting

- Validation: `make_suggestion` now rejects unknown suspect / weapon
  with messages that mention "suspect" and "weapon" — easier to test
  with `pytest.raises(match=...)`.
- `make_accusation` does the same plus a "room" check.
- `new_game` rejects empty names and duplicate names.
- `validate_game_state` checks: solution has 3 keys, total cards = 21,
  no duplicate cards, current_turn_index in bounds.
- Discussed `check_for_winner` semantics: should it auto-fire on each
  accusation or only when called? Decision: only when called. Engine
  sets game_over only on (a) correct accusation, (b) zero active
  players. The screen layer calls `check_for_winner` each tick to detect
  last-standing wins.
- QA reported 70+ tests passing. Looking on track for >85 by submission.

## 3) Decisions agreed at this meeting

- `check_for_winner` is called by the GUI, not the engine, after each
  accusation. (Member C confirmed this matches the rules text.)
- Maysarah adds `get_turn_summary` and `turn_history` (used by the GUI
  log panel and the system test report).
- Floyd adds the message-history panel on the GameScreen.
- Member E starts assembling the submission folder structure.

## 4) Date of next meeting

2026-03-15, Sprint 3 review.

END
