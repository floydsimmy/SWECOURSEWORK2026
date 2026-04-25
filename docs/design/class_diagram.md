# Class Diagram

## Engine (`src/game/`)

```
+----------------------------+
|           Card             |
+----------------------------+
| - card_type: str           |
| - name: str                |
+----------------------------+
| + __str__() -> str         |
+----------------------------+
              ^
              |  (held by)
+----------------------------+      +---------------------------+
|          Player            |      |        GameState          |
+----------------------------+      +---------------------------+
| - name: str                |  *   | - players: list[Player]   |
| - hand: list[Card]         |<-----| - solution: dict[str,Card]|
| - current_room: str | None |      | - current_turn_index: int |
| - is_eliminated: bool      |      | - started: bool           |
+----------------------------+      | - game_over: bool         |
| + __str__() -> str         |      | - winner: str | None      |
+----------------------------+      | - turn_history: list[dict]|
                                    +---------------------------+

+----------------------------+      +-----------------------------+
|        RefuteResult        |      |       AccusationResult      |
+----------------------------+      +-----------------------------+
| - refuted: bool            |      | - correct: bool             |
| - refuting_player: str|None|      | - player_name: str          |
| - card_shown: Card | None  |      | - suspect: str              |
+----------------------------+      | - weapon: str               |
                                    | - room: str                 |
                                    +-----------------------------+
```

`engine.py` holds the rules as free functions over `GameState`. There
is no `Game` class — the spec says no premature abstractions, and a
class with one instance per game adds noise without adding behaviour.

Public engine functions (informal API):

```
new_game(player_names)               -> GameState
reset_game(player_names)             -> GameState
get_current_player(state)            -> Player
next_turn(state)                     -> None
get_game_status(state)               -> dict
get_turn_summary(state)              -> dict
move_to_room(state, player, room)    -> None
make_suggestion(state, p, sus, wpn)  -> RefuteResult
make_accusation(state, p, sus, wpn, rm) -> AccusationResult
check_for_winner(state)              -> Player | None
validate_game_state(state)           -> bool
```

## UI (`src/ui/`)

```
+------------------+
|  ScreenManager   |
+------------------+
| screens: dict    |
| current_screen   |
| game_state*      |
+------------------+
| handle_event()   |
| update()         |
| draw()           |
+--------+---------+
         | manages
         v
+------------------+      +-------------------+
|     Screen       |<-----+ MainMenuScreen    |
| (abstract)       |      +-------------------+
+------------------+      | SetupScreen       |
| screen, w, h     |      +-------------------+
| handle_event()   |      | GameScreen        |
| update()         |      +-------------------+
| draw()           |      | EndScreen         |
+------------------+      +-------------------+

  Components used by all screens:
    Button, TextInput, DropdownMenu, MessageBox, CardDisplay
```

`ScreenManager.game_state` is a class attribute used as a shared slot;
SetupScreen writes it and GameScreen / EndScreen read it. Pragmatic for
a single-game prototype.

## Mapping diagram <-> codebase

| Diagram element  | File / line              |
| ---------------- | ------------------------- |
| Card             | `src/game/models.py:14`   |
| Player           | `src/game/models.py:25`   |
| GameState        | `src/game/models.py:43`   |
| RefuteResult     | `src/game/models.py:55`   |
| AccusationResult | `src/game/models.py:64`   |
| ScreenManager    | `src/ui/screens.py:797`   |
| MainMenuScreen   | `src/ui/screens.py:55`    |
| SetupScreen      | `src/ui/screens.py:129`   |
| GameScreen       | `src/ui/screens.py:256`   |
| EndScreen        | `src/ui/screens.py:694`   |
| Button           | `src/ui/components.py:22` |
