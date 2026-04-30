# Team Meeting — Final Review and Submission Sign-off

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah, Nasser, Abdurrahman             |
| Members absent       | None                                                   |
| Meeting format       | Hybrid — Adam and Floyd in person at Floyd's house; Maysarah, Nasser, and Abdurrahman joined via Google Meet |
| Date and time        | 2026-04-28, 14:00–15:30                                |
| Meeting co-ordinator | Adam                                                   |

## 1) Matters to note from last meeting

- Demo video recorded on 26 April (one take after a notification interrupted the first attempt).
- Final pytest run by Abdurrahman on 27 April: 116 of 116 tests passed (engine + AI + models).
- Screenshots delivered by Nasser on 25 April; placed in `docs/screenshots/`.

## 2) Issues discussed at this meeting

- Final read-through of the group report. Adam walked the team through every section. Team approved with two small wording changes in the "What we would do differently" section.
- Final read-through of the system test report. Every requirement F1–F16, F20–F23 and NF1–NF4 has a Pass row with linked evidence (unit test reference plus screenshot where relevant). Approved.
- Peer review marks discussed openly. Each member spoke briefly about their contribution and what they thought was a fair distribution. Agreement reached without dispute.
- Submission ZIP assembly. Adam and Floyd built the ZIP locally on Floyd's machine, then Maysarah unzipped it on her laptop to verify integrity. `python -m pytest -q` ran cleanly on the unzipped copy.
- Final regression run on the unzipped submission ZIP: 116 / 116 tests passed.

## 3) Decisions agreed at this meeting

- Peer review marks agreed and recorded in `docs/report/peer_review.md`. (Sum = 100 across 5 members.)
- Submission ZIP to be uploaded by Adam to the Canvas submission point by 18:00 on 28 April (a full 22 hours before the 4PM deadline on 30 April), using the team-53 submission slot.
- Repository tagged `submission-2026-04-28` after upload.
- No further code or documentation changes after the upload.

## 4) Date of next meeting

None scheduled — project closed. Demo to module convenor on request.

END
