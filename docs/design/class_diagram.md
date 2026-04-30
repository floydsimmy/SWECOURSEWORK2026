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
+--------------------------------+      +---------------------------------+
|             Player             |      |            GameState            |
+--------------------------------+  *   +---------------------------------+
| - name: str                    |<-----| - players: list[Player]         |
| - hand: list[Card]             |      | - solution: dict[str, Card]     |
| - current_room: str | None     |      | - current_turn_index: int       |
| - is_eliminated: bool          |      | - started: bool                 |
| - player_type: str (= "human"  |      | - game_over: bool               |
|                       or "ai") |      | - winner: str | None            |
| - character: str | None        |      | - turn_history: list[dict]      |
| - board_position: tuple|None   |      | - suspect_locations: dict[str,  |
| - ai_notes: DetectiveNotes|None|      |     str | None]                 |
+--------------------------------+      | - weapon_locations: dict[str,   |
| + __str__() -> str             |      |     str | None]                 |
+--------------------------------+      +---------------------------------+

+--------------------------------+
|       DetectiveNotes           |
+--------------------------------+
| - owned_cards: set             |
| - seen_cards: set              |
| - known_not_in_envelope: set   |
| - possible_suspects: set       |
| - possible_weapons: set        |
| - possible_rooms: set          |
| - suggestion_history: list     |
| - failed_disprovals: list      |
+--------------------------------+

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

`engine.py` holds the rules as free functions over `GameState`. There is no `Game` class — the spec says no premature abstractions, and a class with one instance per game adds noise without adding behaviour.

Public engine functions (informal API):

```
new_game(player_names, seed=None, player_types=None) -> GameState
reset_game(player_names, seed=None, player_types=None) -> GameState
get_current_player(state)              -> Player
next_turn(state)                       -> None
get_game_status(state)                 -> dict
get_turn_summary(state)                -> dict
roll_die(rng=None)                     -> int
legal_moves_for_roll(state, p, roll)   -> dict
move_by_dice(state, p, roll, dest)     -> None
move_to_room(state, player, room)      -> None
make_suggestion(state, p, sus, wpn,
                refute_card_chooser=None) -> RefuteResult
make_accusation(state, p, sus, wpn, rm)  -> AccusationResult
check_for_winner(state)                -> Player | None
validate_game_state(state)             -> bool
```

## AI player module (`src/game/ai.py`)

```
+--------------------------------+
|           AITurnResult         |   (dataclass, returned by take_ai_turn)
+--------------------------------+
| - player_name: str             |
| - dice_roll: int | None        |
| - moved_to: str | None         |
| - suggestion: dict | None      |
| - refute_result: RefuteResult|None |
| - accusation: AccusationResult|None|
| - skipped: bool                |
| - game_over: bool              |
+--------------------------------+

+--------------------------------+
|     RandomAIPlayerStrategy     |
+--------------------------------+
| - rng: random.Random           |
+--------------------------------+
| + roll_die() -> int            |
| + choose_room(p, roll) -> str  |
| + choose_suggestion(p) ->      |
|         tuple[str, str]        |
| + choose_refutation_card(p,    |
|         cards) -> Card         |
| + choose_accusation(p) ->      |
|         tuple|None             |
+--------------------------------+

Helpers (free functions):
  is_ai_player(player) -> bool
  take_ai_turn(state, strategy=None) -> AITurnResult
  run_ai_simulation(state, max_turns=100, strategy=None) -> list[AITurnResult]
  ensure_ai_notes(player) -> DetectiveNotes
  record_known_card(notes, card, *, owned=False) -> None
  record_suggestion_result(player, suggestion, result) -> None
  choose_refutation_card(player, suspect, weapon, room, rng=None) -> Card | None
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
| screen, w, h     |      |   (Human/AI       |
| handle_event()   |      |    toggle per     |
| update()         |      |    player slot)   |
| draw()           |      +-------------------+
+------------------+      | GameScreen        |
                          |   (Roll Dice,     |
                          |    Suggest,       |
                          |    Accuse,        |
                          |    End Turn,      |
                          |    AI auto-turn   |
                          |    in update())   |
                          +-------------------+
                          | EndScreen         |
                          +-------------------+

  Components used by all screens:
    Button, TextInput, PopupSelect, MessageBox, CardDisplay
  Board renderer:
    src/ui/gui.py::Board   (24x24 grid + door highlight)
```

`ScreenManager.game_state` is a class attribute used as a shared slot; SetupScreen writes it and GameScreen / EndScreen read it. Pragmatic for a single-game prototype.

## Mapping diagram → codebase

| Diagram element            | File / line                              |
| -------------------------- | ---------------------------------------- |
| Card                       | `src/game/models.py:17`                  |
| DetectiveNotes             | `src/game/models.py:32`                  |
| Player                     | `src/game/models.py:51`                  |
| GameState                  | `src/game/models.py:74`                  |
| RefuteResult               | `src/game/models.py:97`                  |
| AccusationResult           | `src/game/models.py:106`                 |
| AITurnResult               | `src/game/ai.py:33`                      |
| RandomAIPlayerStrategy     | `src/game/ai.py:47`                      |
| `take_ai_turn`             | `src/game/ai.py:99`                      |
| `roll_die` / dice mechanics | `src/game/engine.py:286`                |
| `legal_moves_for_roll`     | `src/game/engine.py:292`                 |
| `move_by_dice`             | `src/game/engine.py:323`                 |
| `make_suggestion` (F12)    | `src/game/engine.py:379`                 |
| ScreenManager              | `src/ui/screens.py:1370`                 |
| MainMenuScreen             | `src/ui/screens.py:63`                   |
| SetupScreen                | `src/ui/screens.py:137`                  |
| GameScreen                 | `src/ui/screens.py:306`                  |
| EndScreen                  | `src/ui/screens.py:1267`                 |
| Button / TextInput / etc.  | `src/ui/components.py`                   |
| Board renderer             | `src/ui/gui.py`                          |
