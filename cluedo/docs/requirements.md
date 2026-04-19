# Sprint 1

## Team Roles

| Role                               | Name        | Member Responsibility                 |
| ---------------------------------- | ----------- | ------------------------------------- |
| Technical Lead & Integrator        | Floyd       | System structure and integration      |
| Game Logic Engineer                | Maysarah    | Core rules and mechanics              |
| Product Owner                      | Abdulrahman | Requirements, scope, backlog          |
| QA Lead                            | Nasser      | Testing, validation, bug reporting    |
| Scrum Master & Documentation Owner | Adam        | Sprint coordination and documentation |

## Sprint 1 Goal

Creating a playable Cluedo game that can run from start to finish with correct basic mechanics.
This sprint prioritises functional correctness, simplicity, and testability.
No advanced features will be implemented yet.

## Sprint 1 Scope

* The dealing logic works for different player counts
* Turn rotation is properly validated
* QA can test realistic gameplay scenarios
* The system meets the original functional requirements early

## Features

### Game Setup

The system randomly selects 1 suspect, 1 weapon, and 1 room.
The remaining cards are shuffled and dealt evenly to players.

### Turn System

Players take turns in a fixed repeating order. Each turn allows the player to:

* View their hand
* Move to a room
* Make a suggestion
* Make an accusation

### Accusation Mechanic

* If correct, the player wins and the game ends.
* If incorrect, that player cannot accuse again but continues playing.

## Functional Requirements

| ID | Requirement                                                      |
| -- | ---------------------------------------------------------------- |
| F1 | Game generates a random hidden solution                          |
| F2 | Remaining cards must be shuffled and dealt evenly to players     |
| F3 | Turn order rotates correctly                                     |
| F4 | Player must be able to select a room                             |
| F5 | Player must be able to make a suggestion using the current room  |
| F6 | Other players must refute if they hold a matching card           |
| F7 | Player should be able to make an accusation                      |
| F8 | Incorrect accusations prevent further accusations by that player |

## Non-Functional Requirements

| ID  | Requirement                                  |
| --- | -------------------------------------------- |
| NF1 | CLI provides clear instructions and feedback |
| NF2 | Game runs without crashing                   |
| NF3 | Separate game logic from user interface      |
| NF4 | System is simple for QA to test              |

## User Stories

US1: As a player, I want a randomly generated mystery so each game feels different.
US2: As a player, I want cards dealt fairly so the game is unbiased.
US3: As a player, I want turns to rotate automatically so gameplay flows smoothly.
US4: As a player, I want to move into a room so I can investigate.
US5: As a player, I want to make suggestions to gather clues.
US6: As a player, I want other players to refute my suggestion if they can.
US7: As a player, I want to make an accusation when I believe I solved the mystery.
US8: As a player, I should be penalised for an incorrect accusation to maintain fairness.

## Sprint 1 Backlog

| Task                                  | Owner       |
| ------------------------------------- | ----------- |
| Implement game setup and solutions    | Maysarah    |
| Implement card shuffle                | Maysarah    |
| Create turn loop and flow             | Floyd       |
| Implement suggestion/refutation logic | Maysarah    |
| Implement accusation logic            | Maysarah    |
| Build CLI prompts and menus           | Floyd       |
| Input validation                      | Floyd       |
| Define MVP scope and requirements     | Abdulrahman |
| Maintain backlog and acceptance       | Abdulrahman |
| System testing and debugging          | Nasser      |
| Sprint documentation and tracking     | Adam        |

---

# Sprint 2

## Sprint 2 Goal

Creating a complete Cluedo game that can be played from start to finish through the engine and interface.
This sprint prioritises gameplay completion, user interaction, and rule accuracy.
Core game mechanics must now fully work.

## Sprint 2 Scope

* Suggestion and refutation logic fully works
* Accusation and win/lose conditions fully work
* Player elimination works correctly
* Players can interact through the system smoothly

## Features

### Suggestion Mechanic

Players can suggest a suspect and weapon in the current room.

### Refutation Mechanic

Other players must refute if possible by showing one matching card.

### Accusation Mechanic

* Correct accusation wins the game
* Incorrect accusation removes player from future accusations

### Player Flow

Players continue turns correctly after accusations.

## Functional Requirements

| ID | Requirement                             |
| -- | --------------------------------------- |
| F5 | Suggestion system fully works           |
| F6 | Refutation logic fully works            |
| F7 | Accusation system fully works           |
| F8 | Incorrect accusations handled correctly |

## Non-Functional Requirements

| ID  | Requirement                                 |
| --- | ------------------------------------------- |
| NF1 | Interface remains clear and usable          |
| NF2 | No crashes during complete gameplay         |
| NF3 | System responds correctly to player actions |

## User Stories

US1: As a player, I want to make suggestions so I can gather clues.
US2: As a player, I want other players to refute suggestions fairly.
US3: As a player, I want accusations to correctly determine winners.
US4: As a player, I want the game to continue smoothly after wrong accusations.

## Sprint 2 Backlog

| Task                                 | Owner       |
| ------------------------------------ | ----------- |
| Complete suggestion logic            | Maysarah    |
| Complete refutation logic            | Maysarah    |
| Complete accusation system           | Maysarah    |
| Build gameplay screens and menus     | Floyd       |
| Connect interface to engine          | Floyd       |
| Review scope and acceptance criteria | Abdulrahman |
| Update backlog priorities            | Abdulrahman |
| System testing and regression tests  | Nasser      |
| Sprint documentation                 | Adam        |

---

# Sprint 3

## Sprint 3 Goal

Improving Cluedo game quality, usability, and reliability.
This sprint prioritises bug fixing, polish, clearer feedback, and stronger validation.

## Sprint 3 Scope

* Input validation improved
* Better turn summaries and feedback added
* End game screen added
* System handles edge cases correctly

## Features

### Validation

Invalid actions are rejected correctly.

### Feedback

Suggestions, accusations, and turns are clearly shown.

### End Game

Winner displayed clearly.

### Edge Cases

Last remaining player wins if applicable.

## Functional Requirements

| ID  | Requirement                           |
| --- | ------------------------------------- |
| F9  | Invalid player actions rejected       |
| F10 | Winner announcement displayed clearly |
| F11 | Edge cases handled correctly          |

## Non-Functional Requirements

| ID  | Requirement                         |
| --- | ----------------------------------- |
| NF1 | Interface easy to understand        |
| NF2 | No crashes during valid gameplay    |
| NF3 | Faster and smoother user experience |

## Sprint 3 Backlog

| Task                                 | Owner       |
| ------------------------------------ | ----------- |
| Improve input validation             | Floyd       |
| Improve visual feedback              | Floyd       |
| Fix gameplay bugs                    | Maysarah    |
| Improve edge case handling           | Maysarah    |
| Validate non-functional requirements | Abdulrahman |
| Review user experience               | Abdulrahman |
| Full regression testing              | Nasser      |
| Update testing report                | Nasser      |
| Sprint documentation                 | Adam        |
| Begin group report                   | Adam        |

---

# Sprint 4

## Sprint 4 Goal

Preparing final Cluedo project for submission.
This sprint prioritises stability, final testing, evidence, report completion, and demo readiness.

## Sprint 4 Scope

* No new features added
* Only bug fixes and final improvements
* All evidence completed
* Final version ready for demo

## Features

### Final Bug Fixes

Remaining issues resolved.

### Testing

All system tests completed.

### Demo

Full working gameplay recorded.

### Submission

Report and files finalised.

## Functional Requirements

| ID  | Requirement                          |
| --- | ------------------------------------ |
| F12 | Final version fully playable         |
| F13 | All core mechanics working correctly |

## Non-Functional Requirements

| ID  | Requirement                  |
| --- | ---------------------------- |
| NF1 | Stable release build         |
| NF2 | No major bugs remain         |
| NF3 | Project ready for submission |

## Sprint 4 Backlog

| Task                         | Owner       |
| ---------------------------- | ----------- |
| Final integration fixes      | Floyd       |
| Final engine fixes           | Maysarah    |
| Final acceptance sign-off    | Abdulrahman |
| Confirm all requirements met | Abdulrahman |
| Final system testing         | Nasser      |
| Confirm all bugs resolved    | Nasser      |
| Final sprint documents       | Adam        |
| Assemble submission pack     | Adam        |
| Documentation and tracking   | Adam        |
| Complete report              | All Members |






