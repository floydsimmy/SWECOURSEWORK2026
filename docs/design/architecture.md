# Architecture — Cluedo

## Component overview

```
+--------------------+        +-----------------------+
|        UI          |        |        ENGINE         |
|  (src/ui/*.py)     |        |    (src/game/*.py)    |
|                    |        |                       |
|  ScreenManager     |        |   models.py           |
|   - MainMenuScreen |        |     Card              |
|   - SetupScreen    |  reads |     Player (+ AI flag)|
|   - GameScreen     | ------>|     DetectiveNotes    |
|   - EndScreen      |        |     GameState         |
|                    |        |     RefuteResult      |
|  components.py     |        |     AccusationResult  |
|   - Button         |        |                       |
|   - TextInput      |        |   deck.py             |
|   - PopupSelect    |        |     SUSPECTS / ...    |
|   - MessageBox     |        |     create_deck       |
|   - CardDisplay    |        |     verify_deck       |
|                    |        |                       |
|  gui.py (Board     |        |   engine.py           |
|        renderer:   |        |     new_game          |
|        24x24 grid, |        |     next_turn         |
|        doors,      |        |     roll_die          |
|        tokens)     |        |     legal_moves_for_roll
|                    |        |     move_by_dice      |
|                    |        |     move_to_room      |
|                    |        |     make_suggestion   |
|                    |        |     make_accusation   |
|                    |        |     check_for_winner  |
|                    |        |     validate_*        |
|                    |        |                       |
|                    |        |   ai.py               |
|                    |        |     RandomAIPlayer-   |
|                    |        |       Strategy        |
|                    |        |     take_ai_turn      |
|                    |        |     run_ai_simulation |
+---------+----------+        +----------+------------+
          |                              ^
          | calls public engine API      |
          +------------------------------+

  main.py  — Pygame init + main loop, instantiates ScreenManager
  tests/   — pytest covers the engine and AI; UI is validated manually + via demo video
```

## Boundaries (what NOT to do)

- **Engine** does not import Pygame. It is fully testable headless. The AI module sits inside `game/` and is also Pygame-free; the same constraint applies.
- **UI** does not implement any rule. If `screens.py` ever needs to decide who is "next", whether a card refutes, or which tiles are reachable on a roll, that's a smell — the engine should expose a function for it instead. (`legal_moves_for_roll` is the canonical example: the GUI never walks the board itself.)
- **Deck constants are single-source.** No other module hardcodes a suspect / weapon / room name; everything resolves through `game.deck.SUSPECTS / WEAPONS / ROOMS`.

## Why this split?

1. **Testability.** The 116-test pytest suite runs in well under a second because no test opens a Pygame window. If we'd entangled rules with rendering, every test would need a window — and the AI's full-turn simulation tests would not be possible at all.
2. **Replaceability.** A future CLI front-end (or a web port) could reuse the entire `game/` package unchanged, including the AI player.
3. **Three consumers, one engine.** We call the engine from three places — the GUI, the AI, and the tests. Bugs that one place hides usually show up in another.
4. **Clarity.** "Bug in scoring" and "bug in screen layout" land in different folders. New contributors know where to look.

## Module dependencies

```
ui.screens     -> game.engine, game.ai, game.models, game.deck, ui.components, ui.gui
ui.gui         -> game.models, game.deck   (Board renderer)
ui.components  -> (pygame only)
game.ai        -> game.engine, game.models, game.deck
game.engine    -> game.deck, game.models
game.deck      -> game.models
game.models    -> (stdlib only)
```

No cycles. Strict layering: `game.models` is the leaf. `game.ai` depends on `game.engine` only — never the other way round, so removing the AI module would not break the engine.

## Data flow for a single human turn

1. `main.py` event loop → `ScreenManager.handle_event(event)`.
2. `GameScreen.handle_event` reads which button / dropdown was clicked.
3. On **Roll Dice**: GameScreen calls `engine.roll_die()` and `engine.legal_moves_for_roll(state, player, roll)`. Result is a `{tiles, rooms}` dict; both are highlighted on the board and the player clicks a destination, which triggers `engine.move_by_dice(state, player, roll, destination)`.
4. On **Make Suggestion**: GameScreen reads the suspect + weapon dropdowns and calls `engine.make_suggestion(state, player, suspect_card, weapon_card)`. The engine writes the suggester's room into `state.suspect_locations` / `state.weapon_locations` (F12) and walks the refutation order; the GUI surfaces the result and a token-movement log line in the in-game log (TC-25).
5. On **Make Accusation**: GameScreen calls `engine.make_accusation`; engine returns `AccusationResult` and always advances the turn.
6. Engine mutates `GameState` and returns a result dataclass (or None).
7. `GameScreen` appends a human-readable line to its message log and re-paints. It never touches `GameState` directly except to read.

## Data flow for an AI turn

1. `GameScreen.update()` checks `is_ai_player(get_current_player(state))`. If true, it calls `take_ai_turn(state)`.
2. `take_ai_turn` (in `game.ai`) drives the full turn through the engine API: `roll_die` → `move_to_room(...)` (the AI uses simplified room targeting; see `RandomAIPlayerStrategy.choose_room`) → `make_suggestion` → optional `make_accusation` → `next_turn`.
3. The AI updates only the **acting** player's `DetectiveNotes` from the public outcome of the suggestion. Other players' notes are untouched. The AI never inspects `state.solution`.
4. `take_ai_turn` returns an `AITurnResult` summarising what happened. `GameScreen._add_ai_turn_messages` writes the public-safe parts to the game log (no card identities are leaked).

## Deferred / out-of-scope

These are explicitly *not* designed for; adding them would require revisiting the engine API or the screen layer.

- Save / load games.
- Network multiplayer (the `ScreenManager.game_state` class attribute would need to become a per-session object).
- Animated tokens, sound effects, mobile or web build.
- Detective-notes sheet rendered for human players (the AI keeps its own private notes; surfacing them would change the privacy rules in ADR-003).
- Secret passages between corner rooms (the `ROOM_LAYOUT` and door tables would need a "passage" relation; not in the user requirements).
