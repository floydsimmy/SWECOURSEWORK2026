# Engine API Reference

The full public surface of `src/game/engine.py`. All functions raise
`ValueError` (with a descriptive message) on illegal input. They never
catch and swallow exceptions.

## Setup

```
new_game(player_names: list[str]) -> GameState
```
Validate player count (3-6), uniqueness, non-empty names. Build the
21-card deck, draw the solution (one of each type), deal the remaining
18 round-robin. Return a `GameState` with `started=True`.

```
reset_game(player_names: list[str]) -> GameState
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
Advance the index by one, wrapping. Skip eliminated players. If every
player is eliminated, leave the index unchanged (game is over).

```
get_game_status(state: GameState) -> dict
```
Returns `{current_player, players_remaining, game_over, winner}`.

```
get_turn_summary(state: GameState) -> dict
```
Returns `{player_name, available_actions, room, is_eliminated, cards_in_hand}`.
`available_actions` always contains `move` and `accuse`; it contains
`suggest` only if the current player is in a room.

## Actions

```
move_to_room(state, player, room) -> None
```
Set `player.current_room = room`. Records a `move` entry in
`turn_history`. Errors: not current player, unknown room, game over.

```
make_suggestion(state, player, suspect, weapon) -> RefuteResult
```
Walk active players in turn order from the suggester's left. The first
player whose hand contains a card matching the suggested suspect,
weapon, or *current* room shows that card. Records a `suggestion`
entry in `turn_history`. Errors: not current, eliminated, no room,
unknown suspect/weapon, game over.

```
make_accusation(state, player, suspect, weapon, room) -> AccusationResult
```
Compare to the hidden solution. On a correct match, set `state.game_over`
and `state.winner`. On a wrong match, set `player.is_eliminated`; if
that empties the active pool, set `game_over=True` with `winner=None`.
ALWAYS calls `next_turn` before returning. Errors: not current,
eliminated, unknown suspect/weapon/room, game over.

```
check_for_winner(state) -> Player | None
```
If the game is in progress and exactly one player is still active,
declare them the winner and end the game. Returns the winning Player or
None. Designed to be called by the GUI layer on every tick.

## Validation

```
validate_game_state(state) -> bool
```
Asserts: solution has exactly the 3 keys, total cards across all hands
+ solution = 21, no duplicate cards, deck content is the canonical set,
`current_turn_index` is in `[0, len(players))`. Returns True or raises
`ValueError`.

```
verify_deck(deck: list[Card]) -> bool
```
Asserts the input list is exactly the 21 canonical cards (right count,
no duplicates, correct types).
