# Sprint 4 — Start

Format follows `Guidance_for_a_Sprint_cycle.pdf` Appendix A.

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | `[TEAM TO FILL IN]`            |
| Sprint technical lead| `[CONTRIBUTOR A]`              |
| Sprint start date    | `[TEAM TO FILL IN]`            |
| Sprint end date      | `[TEAM TO FILL IN]`            |

## 2) Sprint goal

Submission-ready build. Per `CLAUDE.md` §13 Sprint 4 this is a
**code-freeze** sprint. The only `src/` change permitted is a single
critical bugfix in `src/ui/screens.py` (see backlog item TC-25
below). Everything else is documentation, evidence assembly, and
submission packaging.

## 3) Scope

**In scope**

- Critical bugfix: surface F12 token movement in the in-game log
  (single edit, ~3 lines, in `src/ui/screens.py`).
- Top-level `README.md` polish: install, run, controls, screenshots.
- `docs/testing/system_test_report.md` final fill-in: every requirement
  has a Pass/Fail entry with linked evidence.
- `docs/report/group_report.md` draft (with `[TEAM TO FILL IN]` markers
  per `CLAUDE.md` §13.5).
- `docs/decisions.md`: ADR-005 recording the §13 path override for the
  group report.
- `docs/sprints/sprint_4_start.md` (this file) and
  `docs/sprints/sprint_4_end.md` stub.

**Out of scope** (explicitly forbidden by `CLAUDE.md` §2 and §13)

- New features of any kind.
- Refactors. No "while I was here" cleanups.
- Anything from §2: AI, grid board, networking, save/load,
  animations, sound, mobile, web, alternative languages.
- Touching `pytest.ini`, the engine API, or import statements.

## 4) Backlog (this sprint only)

| ID     | Card                                                          | Priority | Owner            |
| ------ | ------------------------------------------------------------- | -------- | ---------------- |
| TC-25  | Bugfix: log token movement on suggestion (`src/ui/screens.py`) | H        | `[CONTRIBUTOR A]` (Technical Lead) |
| TC-26  | Polish top-level `README.md`                                   | H        | `[CONTRIBUTOR E]` (Scrum / Docs)   |
| TC-27  | Final fill-in `docs/testing/system_test_report.md`             | H        | `[CONTRIBUTOR D]` (QA)             |
| TC-28  | Draft `docs/report/group_report.md` skeleton                   | H        | `[CONTRIBUTOR E]`                  |
| TC-29  | ADR-005 in `docs/decisions.md`                                 | M        | `[CONTRIBUTOR E]`                  |
| TC-30  | Record demo video (human-only, §13.5)                          | H        | `[CONTRIBUTOR E]` (recording) + all members on camera |
| TC-31  | Agree peer-assessment marks (§13.5)                            | H        | All members                         |
| TC-32  | Fill in screenshot placeholders in `README.md` and `system_test_report.md` (§13.5) | H | `[CONTRIBUTOR E]` |
| TC-33  | Final regression run; freeze `main`                            | H        | `[CONTRIBUTOR A]`                  |

## 5) Acceptance criteria

Sprint 4 is closed when **all** of the following hold:

- [ ] TC-25 merged; `python -m pytest -q` reports 100 passed; the
  in-game log shows the F12 token-movement line for any suggestion.
- [ ] `README.md` covers install, run (both commands), controls, 3–6
  player setup, screenshot placeholders, and a link to `docs/README.md`.
- [ ] `docs/testing/system_test_report.md` has a Pass/Fail entry with
  evidence for every requirement in `CLAUDE.md` §6 (F1–F8, NF1–NF2).
- [ ] `docs/report/group_report.md` exists at the path agreed in
  ADR-005, with `[TEAM TO FILL IN]` and `[CONTRIBUTOR A–E]` placeholders.
- [ ] `docs/decisions.md` ends with ADR-005.
- [ ] Demo video recorded and filed (per `CLAUDE.md` §13.5, this is a
  human-only artefact — Claude Code cannot produce it).
- [ ] Peer-assessment marks agreed (per §13.5, human-only).
- [ ] Submission ZIP assembled and unpacks cleanly on a fresh machine.

## 6) Closure checklist (`CLAUDE.md` §10 Definition of Done — Sprint 4 mapping)

| § | Criterion                                                       | TC-25 (bugfix) | TC-26..32 (docs) |
| --- | ------------------------------------------------------------- | -------------- | ---------------- |
| 10.1 | Matches a specific requirement ID                             | F12-DOMAIN     | n/a (process artefacts) |
| 10.2 | Engine unit tests for the change                              | n/a — bugfix is presentation-layer; F12 unit tests already cover the rule | n/a |
| 10.3 | System test row for user-visible change                       | already present (`docs/testing/system_test_report.md` ST-12d-GUI) | n/a |
| 10.4 | `python -m src.main` still runs                               | verified after bugfix | unchanged       |
| 10.5 | Sprint doc updated with what was delivered                    | this file → `sprint_4_end.md` at close | this file → `sprint_4_end.md` at close |

## 7) Risks

| ID  | Risk                                                                                  | Mitigation                                                                                  |
| --- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| R-S4-01 | Scope creep into anything from `CLAUDE.md` §2                                  | Hard stop. PO + Scrum reject any non-bugfix `src/` change.                                  |
| R-S4-02 | Bugfix introduces a regression                                                  | Run `python -m pytest -q` before and after; reject the change if the suite is not 100 green. |
| R-S4-03 | Screenshot placeholders left unfilled at submission                              | TC-32 owner runs the game once and replaces every `[SCREENSHOT: …]` placeholder.            |
| R-S4-04 | Demo video not recorded in time                                                  | TC-30 booked into the sprint window with a 48-hour buffer before submission.                |
| R-S4-05 | Peer-assessment disagreement                                                     | Discuss at sprint-end review; resolve before submission. Per the playbook, equal-share is the default if no other agreement is reached. |

## 8) Owners' summary

Per Q5 placeholder convention (`CLAUDE.md` §13.5). The team
substitutes real names at submission time.

- `[CONTRIBUTOR A]` — Technical Lead & Integrator
- `[CONTRIBUTOR B]` — Game Logic Engineer
- `[CONTRIBUTOR C]` — Product Owner
- `[CONTRIBUTOR D]` — QA Lead
- `[CONTRIBUTOR E]` — Scrum Master & Documentation Owner
