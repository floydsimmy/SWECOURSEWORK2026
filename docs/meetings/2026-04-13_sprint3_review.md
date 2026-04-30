# Team Meeting — Sprint 3 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah, Nasser                          |
| Members absent       | Abdurrahman (had a clashing exam; submitted his test-coverage report on Discord ahead of the meeting) |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-04-13, 18:00–19:00                                |
| Meeting co-ordinator | Maysarah (Technical Lead this sprint)                  |

## 1) Matters to note from last meeting

- F12 token-position bug added to Sprint 3 scope.
- Sprint 4 planning started in parallel.

## 2) Issues discussed at this meeting

- Demo: full 4-player mixed game (2 humans + 2 AI) with deliberate wrong moves at every step. All edge cases handled — wrong-turn errors shown in the message panel, eliminated player's turn auto-skipped, draw path working when all players accuse wrongly. AI turns auto-resolve in the GUI's update loop; the public game log shows AI moves and suggestions without leaking card identities.
- **F12 token-position fix landed.** Suspect and weapon tokens now move into the suggester's room and stay there. Verified with new unit tests by Abdurrahman.
- **AI player module landed.** `src/game/ai.py` with `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, `DetectiveNotes`. New `tests/test_ai.py` covers privacy invariants (AI never reads `state.solution`; private cards shown only update the suggesting AI's notes), correct dice/move/suggestion behaviour, and the "accuse only on single-candidate notes" rule.
- Test count now 113. Coverage of all functional requirements F1–F16 and F20–F23 plus the non-functional NF1, NF2.
- Adam noted that engine and AI module docstrings now cover every public function — the software documentation element should grade well.
- Abdurrahman's written report: zero open critical bugs.

## 3) Decisions agreed at this meeting

- Sprint 3 goal met. Move to Sprint 4 (polish, video, group report, submission). **No new features in Sprint 4** — code freeze with one critical bugfix permitted if anything user-visible regresses.
- Sprint 4 technical lead: Floyd.
- Floyd polishes button colour scheme and the end-screen typography.
- Maysarah keeps the test suite green; investigates any flakes.
- Nasser to capture screenshots once UI polish lands.
- Adam to record the demo video in the final week.
- Adam drafts the Highlights / Lowlights / Critical-analysis sections of the group report.

## 4) Date of next meeting

2026-04-22, Sprint 4 midpoint, Google Meet.

END
