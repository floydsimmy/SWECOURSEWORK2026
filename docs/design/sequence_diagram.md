# Sequence Diagrams

## 1. Game setup (`new_game`)

```
User             SetupScreen        engine.new_game        deck       random
 |  Click Start      |                    |                  |          |
 +------------------>|                    |                  |          |
 |                   |  validate names    |                  |          |
 |                   +-------+            |                  |          |
 |                   |       |            |                  |          |
 |                   |<------+            |                  |          |
 |                   |  collect Human/AI  |                  |          |
 |                   |  toggles per slot  |                  |          |
 |                   +-------+            |                  |          |
 |                   |<------+            |                  |          |
 |                   |  new_game(names,   |                  |          |
 |                   |    player_types)   |                  |          |
 |                   +------------------> |                  |          |
 |                   |                    |  create_deck()   |          |
 |                   |                    +----------------->|          |
 |                   |                    |<-----------------+          |
 |                   |                    |     21 Card                 |
 |                   |                    |  draw solution              |
 |                   |                    +---------------------------->|
 |                   |                    |<----------------------------+
 |                   |                    |  shuffle + deal             |
 |                   |                    +---------------------------->|
 |                   |                    |<----------------------------+
 |                   |                    |  seed AI ai_notes from own  |
 |                   |                    |  hand for any AI slot       |
 |                   |  GameState         |                  |          |
 |                   |<------------------ +                  |          |
 |  Show GameScreen  |                    |                  |          |
 |<------------------+                    |                  |          |
```

## 2. Human dice movement (`roll_die` → `legal_moves_for_roll` → `move_by_dice`)

```
Human            GameScreen           engine
 |  click Roll Dice  |                    |
 +------------------>|                    |
 |                   |  roll_die()        |
 |                   +------------------> |
 |                   |<------------------ +
 |                   |  legal_moves_for_roll(state, p, roll)
 |                   +------------------> |
 |                   |<------------------ +
 |                   |  {tiles, rooms}    |
 |                   |  highlight on board|
 |   highlighted     |                    |
 |<------------------+                    |
 |  click a tile or  |                    |
 |  highlighted room |                    |
 +------------------>|                    |
 |                   |  move_by_dice(state, p, roll, destination)
 |                   +------------------> |
 |                   |<------------------ +
 |    log line:      |                    |
 |    "Alice moved   |                    |
 |     to Kitchen"   |                    |
 |<------------------+                    |
```

The same engine functions (`roll_die`, `legal_moves_for_roll`, `move_by_dice`) are used by the AI; only the click step is replaced with `RandomAIPlayerStrategy.choose_room`.

## 3. Suggestion + refutation (`make_suggestion`, F12)

```
Suggester        GameScreen     engine        GameState     Other Players
 |  click Suggest    |              |              |              |
 +----------------- >|              |              |              |
 |  pick suspect/wpn |              |              |              |
 +------------------>|              |              |              |
 |  click Confirm    |              |              |              |
 +------------------>|              |              |              |
 |                   | make_suggestion(state,...) |              |
 |                   +------------> |              |              |
 |                   |              | check current/eliminated/  |
 |                   |              | room/valid suspect+weapon  |
 |                   |              +-----+        |              |
 |                   |              |     |        |              |
 |                   |              |<----+        |              |
 |                   |              | F12: write   |              |
 |                   |              | suspect_locations[s]=room   |
 |                   |              | weapon_locations[w]=room    |
 |                   |              +------------> |              |
 |                   |              | append turn_history         |
 |                   |              +------------> |              |
 |                   |              | for each player to the left,|
 |                   |              | including eliminated:        |
 |                   |              |   if hand has match -> stop |
 |                   |              +---------------------------->|
 |                   |              |<----------------------------+
 |                   |              | (first match's owner+card)  |
 |                   | RefuteResult |              |              |
 |                   |<------------ +              |              |
 |   "Alice suggests:..."           |              |              |
 |   "  -> Miss Scarlet token       |              |              |
 |       moved to Kitchen;          |              |              |
 |       Knife token moved to       |              |              |
 |       Kitchen"   (TC-25)         |              |              |
 |   "Bob refutes! (showed Rope)"   |              |              |
 |<------------------+              |              |              |
```

Key invariants:

- Refutation walks indices `(suggester+1) % n .. (suggester+n-1) % n`, i.e. every other player, in turn order.
- **Eliminated players are *included* in the refutation walk** (D5 — eliminated players still refute with the cards in their hand).
- The first matching card stops the walk; only that one card is shown, and only to the suggester.
- The suggester's turn does NOT advance; they may still accuse.
- The suspect / weapon tokens written in F12 stay in the room across the rest of the game; they are only moved by another suggestion that names the same suspect / weapon again.

## 4. Accusation (`make_accusation`)

```
Player           GameScreen      engine        GameState     check_for_winner (later)
 |  click Accuse,    |               |              |
 |  pick parts,      |               |              |
 |  click Confirm    |               |              |
 +------------------>|               |              |
 |                   | make_accusation(state,...)   |
 |                   +-------------> |              |
 |                   |               | guard checks |
 |                   |               +-----+        |
 |                   |               |<----+        |
 |                   |               | compare to solution
 |                   |               +-----+        |
 |                   |               |<----+        |
 |                   |    correct?   |              |
 |                   |  +-- yes:     |              |
 |                   |  |   game_over=True, winner=name
 |                   |  +-- no:      |              |
 |                   |  |   player.is_eliminated=True
 |                   |  |   if active_count == 0:   |
 |                   |  |     game_over=True, winner=None
 |                   |               |              |
 |                   |               | next_turn()  |
 |                   |               +------------> |
 |                   | AccusationResult             |
 |                   |<------------- +              |
 |  EndScreen on win |               |              |
 |<------------------+               |              |
                              .   .   .
                  (separately, every tick)
GameScreen.update -> engine.check_for_winner(state)
                       -> if exactly one active: set winner+game_over
                       -> EndScreen
```

## 5. AI auto-turn (`take_ai_turn`)

```
GameScreen.update      ai.take_ai_turn         engine                 ai (notes)
 |  is_ai_player(p)?         |                    |                       |
 |  yes                      |                    |                       |
 +------------------------->|                     |                       |
 |                          | strategy.roll_die() |                       |
 |                          | -> dice             |                       |
 |                          | strategy.choose_room(p, dice)               |
 |                          | -> "Kitchen"        |                       |
 |                          | move_to_room(...)   |                       |
 |                          +-------------------> |                       |
 |                          |<------------------- +                       |
 |                          | strategy.choose_suggestion(p) reads ai_notes|
 |                          +-------------------------------------------> |
 |                          |<------------------------------------------- +
 |                          | make_suggestion(state, p, suspect, weapon, |
 |                          |   refute_card_chooser=strategy.choose_refutation_card)
 |                          +-------------------> |                       |
 |                          |<------------------- +                       |
 |                          | record_suggestion_result(p, suggestion, refute_result)
 |                          +-------------------------------------------> |
 |                          | strategy.choose_accusation(p)               |
 |                          | -> tuple or None                            |
 |                          | if tuple: make_accusation(...)              |
 |                          | else:     next_turn(...)                    |
 |                          +-------------------> |                       |
 |                          |<------------------- +                       |
 |   AITurnResult           |                     |                       |
 |<-------------------------+                     |                       |
 |  _add_ai_turn_messages   |                     |                       |
 |  (public log, no card    |                     |                       |
 |   identities leaked)     |                     |                       |
```

The AI never reads `state.solution` or another player's hand. Notes update only after a public outcome (suggestion refuted by X / not refuted) and after the AI itself sees a card during refutation. The strategy accuses only when the AI's notes have narrowed the solution to one of each card type.
