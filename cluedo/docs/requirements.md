#Sprint 1

Team Roles
Role                	             Name	             Member Responsibility
Technical Lead & Integrator        	Floyd	         System structure and integration
Game Logic Engineer	                Maysarah	     Core rules and mechanics
Product Owner	                    Abdulrahman  	 Requirements, scope, backlog 
QA Lead	                            Nasser	         Testing, validation, bug reporting
Scrum Master & Documentation       	Adam	         Sprint coordination and documentation

Sprint 1 Goal
Creating a playable Cluedo game that can run from start to finish with correct basic mechanics.
This sprint prioritises functional correctness, simplicity, testability.
No advanced features will be implemented yet.

Sprint 1 Scope 
The dealing logic works for different player counts
Turn rotation is properly validated
QA can test realistic gameplay scenarios
The system meets the original functional requirements early.

Features 
Game Setup: The system randomly selects 1 suspect, 1 weapon, 1 room. The remaining cards are shuffled and dealt evenly to the 3 players.
Turn System: Players take turns in a fixed repeating order, each turn allows the player to view their hand, move to a room, make a suggestion, make an accusation.
Accusation Mechanic: If correct, the player wins and the game ends. If incorrect, that player cannot accuse again but continues playing.

Functional Requirements
F1	 Game generates a random hidden solution
F2	 Remaining cards must be shuffled and dealt evenly to 3 players
F3	 Turn order rotates correctly
F4	 Player must be able to select a room 
F5   Player must be able to make a suggestion using the current room
F6 	 Other players must refute if they hold a matching card
F7	 Player should be able to make an accusation
F8   Incorrect accusations prevent further accusations by that player

Non-Functional Requirements
NF1   CLI provide clear instructions and feedback
NF2	  Game run without crashing 
NF3   Separate game logic from user interface
NF4   System be simple for QA to test 

User Stories
US1: As a player, I want a randomly generated mystery so each game feels different.
US2: As a player, I want cards dealt fairly so the game is unbiased.
US3: As a player, I want turns to rotate automatically so gameplay flows smoothly.
US4: As a player, I want to move into a room so I can investigate.
US5: As a player, I want to make suggestions to gather clues.
US6: As a player, I want other players to refute my suggestion if they can.
US7: As a player, I want to make an accusation when I believe I solved the mystery.
US8: As a player, I should be penalised for an incorrect accusation to maintain fairness.

Sprint 1 Backlog
Task	                                  Owner
Implement game setup and solutions	     Maysarah
Implement card shuffle 	                 Maysarah
Create turn loop and flow	             Floyd
Implement suggestion/refutation logic	 Maysarah
Implement accusation logic	             Maysarah
Build CLI prompts and menus	             Floyd
Input validation	                     Floyd
Define MVP scope and requirements	     Abdulrahman 
Maintain backlog and acceptance 	     Abdulrahman 
System testing and debugging  	         Nasser
Sprint documentation and tracking	     Adam






