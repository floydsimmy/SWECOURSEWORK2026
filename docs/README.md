# Documentation Index

This directory contains all process, design, testing, and reporting documentation for the Cluedo project. Documents are grouped by topic rather than by playbook section name. This index maps each marking criteria element and each playbook deliverable to its actual location, so any reader — marker, team member, or future maintainer — can find what they need without exploring directories.

The topic-subfolder structure is a deliberate deviation from the flat layout in `CLAUDE.md` §3 and is recorded in `decisions.md` as **ADR-002**.

---

## For markers — quick map of marking criteria to evidence

The marking criteria in `Refined_Marking_Criteria.pdf` assesses nine elements. Each element's evidence lives at the path below.

| Marking element | Out of | Location |
|---|---|---|
| Planning — project plan, PERT/Gantt, risk analysis, resourcing | 5 | [`planning/`](./planning/) |
| Planning — meeting notes | 5 | [`meetings/`](./meetings/) |
| Process documentation — sprint cycle docs | 10 | [`sprints/`](./sprints/) |
| Design — high-level (use cases, activity diagrams, component overview) | 5 | [`design/`](./design/) — see `architecture.md` and `use_cases.md` |
| Design — low-level (class diagrams, API specs, sequence diagrams) | 5 | [`design/`](./design/) — see `class_diagram.md` and `architecture.md` |
| Software documentation — code-level (docstrings, in-code comments) | 5 | In source: `src/game/` and `src/ui/` modules |
| Testing — unit and system tests, requirement linkage | 10 | [`testing/`](./testing/) — system test report; unit tests in repo `tests/` |
| Code | 50 | Repo `src/` directory; entry point `python -m src.main` |
| Group report | 5 | [`report/`](./report/) |

Engineering decisions, deviations, and trade-offs are recorded in [`decisions.md`](./decisions.md). Markers reviewing design or process choices should read this alongside the design documents.

---

## Directory structure

```
docs/
  README.md           ← this index
  decisions.md        ← engineering decision log (ADRs)
  planning/           ← project plan, Gantt/PERT, risk register, resourcing
  design/             ← architecture, class diagrams, sequence diagrams, use cases
  testing/            ← system test report, test plan, regression evidence
  report/             ← group report, peer assessment template
  meetings/           ← meeting minutes (one file per meeting)
  sprints/            ← sprint start and end documents (one pair per sprint)
```

Unit tests themselves live at `tests/` in the repo root, not under `docs/` — they are executable artefacts, not documentation.

---

## Subfolder contents

### `planning/`

Project planning artefacts referenced by the marking criteria's first planning element.

- `project_plan.md` — task breakdown, ownership, schedule
- `gantt.md` — visual schedule (text-rendered Gantt + critical path)
- `risk_register.md` — identified risks, likelihood, impact, mitigation

### `design/`

High-level and low-level design documentation. The marking criteria splits these into two five-mark elements; both live here for cohesion.

- `architecture.md` — system overview, module boundaries, engine ↔ UI separation per `CLAUDE.md` §4
- `class_diagram.md` — class relationships in `src/game/`
- `sequence_diagram.md` — key flows: game setup, turn cycle, suggestion+refutation, accusation
- `api.md` — the engine API contract per `CLAUDE.md` §5

### `testing/`

Testing evidence linking back to requirement IDs (F1–F8, NF1–NF2 per `CLAUDE.md` §6).

- `system_test_report.md` — primary deliverable. Each row: requirement ID, description, inputs, expected output, actual output, pass/fail, action. Format follows the example in `Example_System_Testing.pdf`.

Unit test source files are in the repo `tests/` directory, not here.

### `report/`

Submission-final documents.

- `group_report.md` — narrative of the project, team performance, what went well, what didn't, what would change next time
- `peer_review.md` — agreed mark distribution per the playbook's 20-points-per-member rule
- `requirements.md` — the formal requirements list (F1–F16, NF1–NF4, domain rules) referenced by the system test report

### `meetings/`

One file per meeting, named `YYYY-MM-DD_meeting.md`. Each file follows the template from `TeamMeetingNoteTemplate.pdf`: attendees, matters from last meeting, issues discussed, decisions agreed (with owner), date of next meeting.

### `sprints/`

Two files per sprint:

- `sprint_N_start.md` — sprint dates, goal, backlog with owners, acceptance criteria, risks
- `sprint_N_end.md` — what was delivered, evidence links, test results, retrospective, plan for next sprint

The format follows the sprint template in `Guidance_for_a_Sprint_cycle.pdf` Appendix A.

---

## Cross-reference: playbook deliverables to locations

The team playbook (`4_sprints.pdf`) §11 specifies several documents under flat names. Their actual locations in this layout are:

| Playbook reference | Actual location |
|---|---|
| `docs/requirements.md` | `report/requirements.md` (F1–F16 + NF1–NF4 + domain rules) |
| `docs/architecture.md` | `design/architecture.md` |
| `docs/decisions.md` | `decisions.md` (kept at `docs/` root for visibility) |
| `docs/system_test_report.md` | `testing/system_test_report.md` |
| `docs/meetings/` | `meetings/` |
| `docs/sprints/` | `sprints/` |

---

## Cross-reference: `CLAUDE.md` section to document

For Claude Code sessions, the most-cited `CLAUDE.md` sections map to documents as follows:

| `CLAUDE.md` section | Document |
|---|---|
| §3 (repo structure) | `decisions.md` ADR-001, ADR-002, ADR-004 — explains all structural deviations |
| §5 (engine API) | `design/api.md` |
| §6 (functional requirements) | `report/requirements.md` and `testing/system_test_report.md` |
| §7 (domain rules) | `design/architecture.md` (rule encoding) and `decisions.md` ADR-003 (hand privacy) |
| §10 (Definition of Done) | `decisions.md` ADR-004 (run command) |
| §13 (sprint scope) | `sprints/sprint_N_*.md` for each sprint |

---

*This index is updated whenever a new document type is added or relocated. If you add a document and a marker can't find it from this README, the index is broken — fix the index before merging.*
