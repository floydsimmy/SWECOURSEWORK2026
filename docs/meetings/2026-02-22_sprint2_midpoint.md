# Team Meeting — Sprint 2 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | Zoom                                                   |
| Date and time        | 2026-02-22, 14:00-14:40                                |
| Meeting co-ordinator | Member E                                               |

## 1) Matters to note from last meeting

- Sprint 2 goal: full gameplay loop + Pygame integration.
- QA started `system_test_report.md`.

## 2) Issues discussed at this meeting

- Suggestion and refutation rules implemented; tests passing.
- Refutation order: from current player's left, skipping eliminated
  players. First match shown to the suggester only.
- Floyd raised the question of grid-based movement. PO ruled it out of
  scope for the MVP — drop-down room selection only. Documented as
  decision in `docs/sprints/sprint_2.md`.
- AI player: stretch only. Confirmed deferred indefinitely.
- ScreenManager class attribute `game_state` to share state between
  screens — agreed as pragmatic for the prototype, even if not the
  cleanest pattern.

## 3) Decisions agreed at this meeting

- Grid movement DROPPED from MVP. (Member C, recorded in decisions.md)
- AI player DROPPED from scope (Member C).
- Floyd ships SetupScreen and GameScreen by 2026-02-26.
- Maysarah finishes accusation auto-advance + `check_for_winner` by 2026-02-25.
- QA writes the F4-F8 system tests by 2026-02-28.

## 4) Date of next meeting

2026-03-01, Sprint 2 review.

END
