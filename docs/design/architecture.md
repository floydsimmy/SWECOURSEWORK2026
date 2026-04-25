# Architecture — Cluedo

## Component overview

```
+--------------------+        +---------------------+
|        UI          |        |      ENGINE         |
|  (src/ui/*.py)     |        |   (src/game/*.py)   |
|                    |        |                     |
|  ScreenManager     |        |   models.py         |
|   - MainMenuScreen |        |     Card            |
|   - SetupScreen    |  reads |     Player          |
|   - GameScreen     | ------>|     GameState       |
|   - EndScreen      |        |     RefuteResult    |
|                    |        |     AccusationResult|
|  components.py     |        |                     |
|   - Button         |        |   deck.py           |
|   - TextInput      |        |     SUSPECTS / ...  |
|   - DropdownMenu   |        |     create_deck     |
|   - MessageBox     |        |     verify_deck     |
|   - CardDisplay    |        |                     |
|                    |        |   engine.py         |
|  gui.py (board art)|        |     new_game        |
|                    |        |     next_turn       |
|                    |        |     get_current_*   |
|                    |        |     move_to_room    |
|                    |        |     make_suggestion |
|                    |        |     make_accusation |
|                    |        |     check_for_winner|
|                    |        |     validate_*      |
+---------+----------+        +----------+----------+
          |                              ^
          | calls public engine API       |
          +-------------------------------+

  main.py  — Pygame init + main loop, instantiates ScreenManager
  tests/   — pytest covers the engine; UI is validated manually + via video
```

## Boundaries (what NOT to do)

- **Engine** does not import Pygame. It is fully testable headless.
- **UI** does not implement any rule. If `screens.py` ever needs to
  decide who is "next" or whether a card refutes, that's a smell —
  the engine should expose a function for it instead.
- **Deck constants are single-source.** No other module hardcodes a
  suspect / weapon / room name; everything resolves through
  `game.deck.SUSPECTS / WEAPONS / ROOMS`.

## Why this split?

1. **Testability.** 91 unit tests run in 0.34 seconds because they
   never touch SDL. If we'd entangled rules with rendering, every test
   would need a window.
2. **Replaceability.** A future CLI front-end (or a web port) could
   reuse the entire `game/` package unchanged.
3. **Clarity.** "Bug in scoring" and "bug in screen layout" land in
   different folders. New contributors know where to look.

## Module dependencies

```
ui.screens   -> game.engine, game.models, game.deck, ui.components
ui.gui       -> game.models, game.deck
ui.components-> (pygame only)
game.engine  -> game.deck, game.models
game.deck    -> game.models
game.models  -> (stdlib only)
```

No cycles. Strict layering: `game.models` is the leaf.

## Data flow for a single turn

1. `main.py` event loop -> `ScreenManager.handle_event(event)`.
2. `GameScreen.handle_event` reads which button/dropdown was clicked.
3. On confirm: `GameScreen` calls the appropriate engine function
   (`move_to_room`, `make_suggestion`, `make_accusation`, `next_turn`).
4. Engine mutates `GameState` and returns a result dataclass (or None).
5. `GameScreen` appends a human-readable line to its message log and
   re-paints. It never touches `GameState` directly except to read.

## Deferred / out-of-scope

- Grid-based movement on a board (descoped Sprint 2).
- AI player (descoped Sprint 2).
- Save / load games.
- Network multiplayer.

These are explicitly *not* designed for; adding them would require
revisiting the engine API.
