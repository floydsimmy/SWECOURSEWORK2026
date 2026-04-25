# Team Meeting — Sprint 3 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | In person                                              |
| Date and time        | 2026-03-15, 14:00-14:50                                |
| Meeting co-ordinator | Maysarah (technical lead this sprint)                  |

## 1) Matters to note from last meeting

- `check_for_winner` is GUI-driven (only fires when called).
- Game log panel shows the last 8 turn-history entries.

## 2) Issues discussed at this meeting

- Demo: Floyd played a full 4-player game with deliberate wrong moves.
  All edge cases handled: wrong-turn errors are shown in the message
  box, eliminated player's turn is auto-skipped, draw path works.
- Test count up to 91. Coverage of all F1-F16 plus three NF rules.
- Member E pointed out that the engine module's docstrings now cover
  every public function — software documentation element should grade
  cleanly.
- Member D reported zero open critical bugs.

## 3) Decisions agreed at this meeting

- Move into Sprint 4 (polish, video, group report). No new features.
- Floyd polishes button colour scheme and the end-screen typography.
- Maysarah keeps the test suite green; investigates any flake.
- Member E records the demo video on 2026-03-25 once final polish lands.
- Member C drafts the group-report Highlights / Lowlights section.

## 4) Date of next meeting

2026-03-22, Sprint 4 midpoint.

END
