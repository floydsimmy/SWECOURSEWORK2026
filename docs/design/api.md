# Engine API Reference

The full public surface of `src/game/engine.py` and `src/game/ai.py`. All engine functions raise `ValueError` (with a descriptive message) on illegal input. They never catch and swallow exceptions.

## Setup

```
new_game(player_names: list[str],
         seed: int | None = None,
         player_types: list[str] | None = None) -> GameState
```
Validate player count (3–6), uniqueness, non-empty names. Build the 21-card deck, draw the solution (one of each type), deal the remaining 18 round-robin. Place each player's character token on its canonical start tile (Miss Scarlet at (7,23), Colonel Mustard at (7,17), and so on). Initialise empty `suspect_locations` / `weapon_locations` and, for any AI slot, an empty `DetectiveNotes` seeded from the player's own hand. Return a `GameState` with `started=True`.

`seed` makes setup deterministic for reproducible tests; the same seed yields the same solution, deal, and turn order. `player_types` is a list of `"human"` or `"ai"` strings, one per name; if omitted, every slot defaults to human.

```
reset_game(player_names: list[str],
           seed: int | None = None,
           player_types: list[str] | None = None) -> GameState
```
Convenience wrapper; produces a fresh game with the same names.

## Turn queries

```
get_current_player(state: GameState) -> Player
```
The player at `state.current_turn_index`.

```
next_turn(state: GameState) -> None
```
Advance the index by one, wrapping. Skip eliminated players. If every player is eliminated, leave the index unchanged (game is over).

```
get_game_status(state: GameState) -> dict
```
Returns `{current_player, players_remaining, game_over, winner}`.

```
get_turn_summary(state: GameState) -> dict
```
Returns `{player_name, available_actions, room, is_eliminated, cards_in_hand}`. `available_actions` always contains `move` and `accuse`; it contains `suggest` only if the current player is in a room.

## Movement (dice + grid)

```
roll_die(rng: random.Random | None = None) -> int
```
Roll one fair six-sided die. Returns 1–6. Accepts an optional injected RNG so tests can pin the result.

```
legal_moves_for_roll(state: GameState,
                     player: Player,
                     dice_roll: int) -> dict
```
Returns `{"tiles": [(col, row), ...], "rooms": ["Kitchen", ...]}` — the corridor tiles exactly `dice_roll` steps away on the grid, plus every room whose door is reachable in at most `dice_roll` steps. Walks a BFS over the static `ROOM_LAYOUT`, `ROOM_DOORS`, and `CHARACTER_START_TILES` tables, blocking other players' tiles. Errors: not current, eliminated, dice out of 1–6.

```
move_by_dice(state: GameState,
             player: Player,
             dice_roll: int,
             destination: str | tuple[int, int]) -> None
```
Move `player` to a destination chosen from a `legal_moves_for_roll` result. A string destination is a room name; a tuple is a corridor tile. Errors: destination not in the legal set, unknown room, malformed tile.

```
move_to_room(state: GameState, player: Player, room: str) -> None
```
Direct room placement — used by tests and by the AI's simplified room-targeting strategy. Sets `player.current_room = room`, clears `player.board_position`, records a `move` entry in `turn_history`. Errors: not current player, unknown room, game over.

## Suggestion and accusation

```
make_suggestion(state: GameState,
                player: Player,
                suspect: Card | str,
                weapon: Card | str,
                refute_card_chooser: Callable | None = None) -> RefuteResult
```
The suggesting player must be in a room. The room from `player.current_room` is the implicit third element of the suggestion. Walk active **and eliminated** players in turn order from the suggester's left; the first player whose hand contains a card matching the suggested suspect, weapon, or current room shows that card. Eliminated players still refute (D5).

**F12 (domain):** the named suspect and weapon tokens are written into `state.suspect_locations[suspect_name]` and `state.weapon_locations[weapon_name]` as the suggester's current room **before** the refutation walk. They remain there afterwards; refutation does not move them back.

`suspect` and `weapon` accept either a `Card` instance (per §5 contract) or a bare name string (back-compat). A `Card` with the wrong `card_type` raises `ValueError`.

`refute_card_chooser` is an optional callback `(player, matching_cards) -> Card` used by the AI to pick which card to show when more than one matches. Defaults to "show the first match" (deterministic, suitable for tests).

Records a `suggestion` entry in `turn_history`. Errors: not current, eliminated, no room, unknown suspect / weapon, game over, callback returns a non-matching card.

```
make_accusation(state: GameState,
                player: Player,
                suspect: Card | str,
                weapon: Card | str,
                room: Card | str) -> AccusationResult
```
Compare to the hidden solution. On a correct match, set `state.game_over=True` and `state.winner=player.name`. On a wrong match, set `player.is_eliminated=True`; if that empties the active pool, set `game_over=True` with `winner=None`. **ALWAYS calls `next_turn`** before returning. Errors: not current, eliminated, unknown suspect / weapon / room, game over.

```
check_for_winner(state: GameState) -> Player | None
```
If the game is in progress and exactly one player is still active, declare them the winner and end the game. Returns the winning Player, or None. Designed to be called by the GUI layer on every tick.

## Validation

```
validate_game_state(state: GameState) -> bool
```
Asserts: solution has exactly the 3 keys; total cards across all hands + solution = 21; no duplicate cards; deck content is the canonical set; every `Player.player_type` is one of `{"human", "ai"}`; `current_turn_index` is in `[0, len(players))`. Returns True or raises `ValueError`.

```
verify_deck(deck: list[Card]) -> bool
```
Asserts the input list is exactly the 21 canonical cards (right count, no duplicates, correct types).

---

## AI player API (`src/game/ai.py`)

```
is_ai_player(player: Player) -> bool
```
True if `player.player_type == AI_PLAYER` (`"ai"`).

```
class RandomAIPlayerStrategy:
    rng: random.Random

    roll_die() -> int
    choose_room(player, dice_roll) -> str
    choose_suggestion(player) -> tuple[str, str]
    choose_refutation_card(player, matching_cards) -> Card
    choose_accusation(player) -> tuple[str, str, str] | None
```
The default strategy. All choices are random over what the player **is allowed to know** — the strategy reads `player.ai_notes` (a `DetectiveNotes` instance) and the canonical card lists, never `state.solution`. `choose_accusation` returns `None` until the strategy's notes have narrowed each card type to exactly one possibility, at which point it accuses confidently.

```
take_ai_turn(state: GameState,
             strategy: RandomAIPlayerStrategy | None = None) -> AITurnResult
```
Execute one complete turn for the current AI player: roll, move, suggest, optionally accuse, advance. Updates only the **acting** AI's `DetectiveNotes` from the public outcome of the suggestion. Returns an `AITurnResult` summarising what happened. Errors: current player is not AI.

```
run_ai_simulation(state: GameState,
                  max_turns: int = 100,
                  strategy: RandomAIPlayerStrategy | None = None
                  ) -> list[AITurnResult]
```
Run AI turns one after another until the game ends, control reaches a human player, or `max_turns` is hit. Used in `tests/test_ai.py` for end-to-end AI behaviour.

```
ensure_ai_notes(player: Player) -> DetectiveNotes
record_known_card(notes, card, *, owned=False) -> None
record_suggestion_result(player, suggestion, result) -> None
```
Helpers for maintaining `DetectiveNotes` outside the strategy. `ensure_ai_notes` is idempotent and is what `tests/` and legacy state paths use to lazily seed notes if they are absent.

### Privacy invariants for the AI

These are tested in `tests/test_ai.py` and held by the implementation:

- The AI never reads `state.solution` directly (`test_ai_turn_does_not_read_solution_when_not_accusing`).
- A card shown to AI A during refutation does not appear in AI B's notes (`test_private_shown_card_updates_only_suggesting_ai_notes`).
- The AI shows exactly one matching card when refuting and never one that does not match (`test_ai_refutation_shows_one_matching_card`, `test_ai_refutation_does_not_show_non_matching_cards`).
