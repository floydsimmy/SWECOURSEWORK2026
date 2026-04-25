# Team Meeting — Sprint 2 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | In person                                              |
| Date and time        | 2026-03-01, 14:00-15:00                                |
| Meeting co-ordinator | Floyd                                                  |

## 1) Matters to note from last meeting

- All Sprint 2 actions completed.
- Grid movement and AI both descoped (in `decisions.md`).

## 2) Issues discussed at this meeting

- Live demo: full game played by three of us, end to end. Suggestion
  and accusation flows worked.
- Bugs surfaced during QA pass:
  - Wrong-turn protection missing on `move_to_room` (fixed).
  - Eliminated player could still try to suggest because the room check
    came before the eliminated check (fixed; eliminated check first).
  - End screen showed `None` when game ended by all-eliminated (fixed
    by adding the "draw" path).
- Member E flagged that we are short on system tests — only ~20 cases
  written so far. Plan to push to 35+ in Sprint 3.

## 3) Decisions agreed at this meeting

- Sprint 3 goal: robustness, validation, edge cases, end-game polish.
- Maysarah owns `validate_game_state` and `verify_deck` for Sprint 3.
- Floyd owns the EndScreen + game-over handling.
- QA expands the test report with the Sprint 3 requirements.
- Scrum drafts the group report skeleton.

## 4) Date of next meeting

2026-03-08, Sprint 3 midpoint.

END
