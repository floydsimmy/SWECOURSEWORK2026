# Team Meeting — Sprint 1 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | (assigned)                                             |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | Hybrid (3 in person, 2 on Zoom)                        |
| Date and time        | 2026-02-10, 14:00-14:45                                |
| Meeting co-ordinator | Member E                                               |

## 1) Matters to note from last meeting

- Repo created and shared (action: Floyd, completed 2026-02-04).
- User stories F1-F8 drafted (action: Member C, completed 2026-02-05).
- System test plan v0.1 (action: Member D, completed 2026-02-08).

## 2) Issues discussed at this meeting

- Engine API contract walkthrough — agreed `RefuteResult` and
  `AccusationResult` should be dataclasses (not bare dicts).
- Should `make_accusation` auto-advance the turn? Decision: yes, even on
  a correct accusation, so the test for "Game is already over" can be
  exercised by the next player.
- Solution selection: random.choice from each card-type subset (simple,
  fair, easy to test).
- Naming: American Cluedo names (Miss Scarlet, Knife, Wrench, ...) so
  unit tests stay readable.

## 3) Decisions agreed at this meeting

- Engine API frozen (Maysarah documents in `docs/design/api.md` by 2026-02-12).
- All engine functions raise `ValueError` with descriptive messages — never bare `Exception`.
- Skip eliminated players in both `next_turn` and refutation order.
- Pygame skeleton should compile on `main` by end of Sprint 1 (Floyd).

## 4) Date of next meeting

2026-02-15, sprint review.

END
