# Sprint 4 — Polish, Demo & Submission

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | 53                             |
| Sprint technical lead| Floyd                          |
| Sprint start date    | 2026-04-13                     |
| Sprint end date      | 2026-04-29                     |

## 2) Individual key contributions

| Team member  | Key contribution(s)                                                                                                                                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Adam         | Final group report drafting and team sign-off coordination; `docs/report/peer_review.md`; demo video script and recording (one re-take after a notification interrupted the first attempt); top-level `README.md` polish; submission ZIP assembly and integrity check on Floyd's machine; Sprint 4 midpoint minutes (2026-04-22) and Final review minutes (2026-04-28); Canvas submission upload. |
| Floyd        | TC-25 bugfix in `src/ui/screens.py` — surfaces F12 token movement in the suggestion log; final UI polish (button colour scheme, end-screen typography); code-freeze enforcement; integration smoke testing across both `python -m src.main` and `python src/main.py` invocations; submission ZIP build on his machine; in-person final review meeting hosting. |
| Maysarah     | Final test suite verification (100 of 100 passing throughout the sprint); minor `__str__` polish on `Card` and `Player` for readable log lines; final code documentation sweep — every public engine function has a docstring.                                                                                                                                                                                                                                              |
| Nasser       | Title-screen, gameplay, and end-screen screenshots captured from the polished build (delivered to `#docs-evidence` on Discord on 2026-04-25 for inclusion in `README.md` and the system test report); ad-hoc UI polish in response to screenshot review.                                                                                                                                                                                                                                |
| Abdurrahman  | Final regression run on 2026-04-27 (100 of 100 passing); system test report finalised with every F1–F8 and NF1–NF2 row marked Pass with linked evidence; bug log closed; final regression on the *unpacked submission ZIP* (still 100 of 100, confirming clean export).                                                                                                                                                                                                                                |

## 3) User stories / task cards

Sprint 4 is a code-freeze sprint, not a feature sprint. The "user story" is the marker's own perspective:

> **As a marker, I want to receive a complete, runnable, well-documented submission package so that I can grade Team 53's work efficiently.**

Task cards prioritised at the Sprint 3 review on 2026-04-13:

| ID     | Card                                                                  | Priority | Owner                          |
| ------ | --------------------------------------------------------------------- | -------- | ------------------------------ |
| TC-25  | Bugfix: log token movement on suggestion (`src/ui/screens.py`)         | H        | Floyd                          |
| TC-26  | Polish top-level `README.md`                                           | H        | Adam                           |
| TC-27  | Final fill-in `docs/testing/system_test_report.md`                     | H        | Abdurrahman                    |
| TC-28  | Finalise `docs/report/group_report.md`                                 | H        | Adam                           |
| TC-29  | Agree peer-assessment marks; record in `docs/report/peer_review.md`    | H        | All members                    |
| TC-30  | Record demo video                                                      | H        | Adam (record), all on camera   |
| TC-31  | Capture screenshots for `README.md` and system test report             | H        | Nasser                         |
| TC-32  | Final regression run; freeze `main`                                    | H        | Floyd, Abdurrahman             |
| TC-33  | Submission ZIP assembly and integrity check                            | H        | Adam, Floyd                    |

## 4) Requirements analysis

No new functional or non-functional requirements in Sprint 4. The sprint validates that all requirements from Sprints 1–3 (F1–F16, NF1–NF2) remain satisfied at submission. The only material change is the F12 visibility bugfix (TC-25), which is a presentation-layer fix on top of the engine-layer F12 work delivered in Sprint 3.

## 5) Design

No new design artefacts. The existing design documentation (`docs/design/architecture.md`, `class_diagram.md`, `sequence_diagram.md`, `api.md`) was reviewed by the team during the Sprint 4 midpoint meeting (2026-04-22) and confirmed to match the final codebase.

The TC-25 bugfix is a 3-line addition to `GameScreen._execute_suggestion` in `src/ui/screens.py`. It calls `self._add_message` with a human-readable line indicating where the suggested suspect and weapon tokens were placed (e.g. "→ Miss Scarlet token moved to Kitchen; Knife token moved to Kitchen"). This change does not affect the engine API.

## 6) Test plan and evidence of testing

**Final regression run** (Abdurrahman, 2026-04-27, Python 3.13.13, Windows 11):
$ python -m pytest -q
.................................... ........................................
....................                                                       [100%]
100 passed in 0.06s

**Re-run on the unpacked submission ZIP** (Maysarah, 2026-04-28, different laptop): also 100 of 100. This confirms the ZIP exports cleanly.

**Manual smoke tests on the final build** (whole team during the Final Review, 2026-04-28):

- 3-player game, correct accusation on first turn → EndScreen shows winner.
- 4-player game, all wrong accusations → EndScreen shows draw.
- 6-player game, deliberate wrong-turn click → error banner shown, no crash.
- Quit and re-enter from EndScreen → Main Menu reachable.
- F12 visibility check: every suggestion in the log shows the token-movement line.

All passed. No outstanding deficiencies.

## 7) Summary of sprint

**Did we achieve our objectives?** Yes. The build is stable, the demo video is recorded, the submission pack is assembled, and the ZIP unpacks cleanly with the test suite still 100 of 100.

**Is there a working prototype?** Yes — the final build, ready to submit.

**What went well?** The decision to make Sprint 4 a strict code-freeze sprint (with one critical bugfix permitted) gave the team budget for a clean demo video, a thorough group report, and submission ZIP integrity checking. Adam and Floyd meeting in person at Floyd's house for the final review meant the ZIP was assembled and verified together with the rest of the team on Google Meet — no async-confirmation delay. The contribution tables in each sprint doc made the peer review conversation at the final meeting straightforward; the team agreed an equal 20/20/20/20/20 split without dispute.

**What did not go well?** Demo video took two attempts because the first take had an audible system notification at around 0:42. Trivial to avoid (Do Not Disturb mode); we just didn't think of it ahead of time. Not a meaningful problem.

**Customer feedback?** None this sprint — Sprint 4 is internal polish and submission prep.
