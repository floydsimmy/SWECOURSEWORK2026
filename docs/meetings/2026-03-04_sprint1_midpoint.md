# Team Meeting — Sprint 1 Midpoint

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah, Abdurrahman                     |
| Members absent       | Nasser (sent update via Discord)                       |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-03-04, 17:00–17:50                                |
| Meeting co-ordinator | Adam                                                   |

## 1) Matters to note from last meeting

- Discord server is live and channels are populated.
- User stories F1–F8 drafted by Adam and posted in `#decisions` for review.

## 2) Issues discussed at this meeting

- Python and Git setup issues. Two members had trouble getting Python on their PATH (Microsoft Store stub problem on Windows) and another was new to Git branching. Floyd ran a short walkthrough and shared a setup checklist in `#dev`.
- Engine API design. Maysarah proposed using dataclasses (`Card`, `Player`, `GameState`) rather than dicts so the IDE would help with autocomplete. Agreed.
- Question raised about how `make_accusation` should handle the auto-advance to the next player. Decision deferred to the Sprint 1 review meeting once a working implementation existed to discuss against.
- Nasser sent screenshots via Discord of the title-screen layout he was prototyping. Team gave feedback to merge into the main branch once it ran.

## 3) Decisions agreed at this meeting

- Engine API to be frozen by end of Sprint 1 so screens can be built against a stable contract. (Action: Maysarah, Floyd.)
- Setup checklist for Python + Git pinned in `#dev`. (Action: Floyd, completed during the meeting.)
- All engine functions to raise `ValueError` (not bare `Exception`) for illegal input, with descriptive messages. (Action: Maysarah.)

## 4) Date of next meeting

2026-03-09, Sprint 1 review, Google Meet.

END
