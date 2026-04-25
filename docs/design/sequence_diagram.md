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
 |                   |  new_game(names)   |                  |          |
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
 |                   |  GameState         |                  |          |
 |                   |<------------------ +                  |          |
 |  Show GameScreen  |                    |                  |          |
 |<------------------+                    |                  |          |
```

## 2. Suggestion + refutation (`make_suggestion`)

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
 |                   |              | append turn_history         |
 |                   |              +------------> |              |
 |                   |              | for each player to the left,|
 |                   |              | skipping eliminated:        |
 |                   |              |   if hand has match -> stop |
 |                   |              +---------------------------->|
 |                   |              |<----------------------------+
 |                   |              | (first match's owner+card)  |
 |                   | RefuteResult |              |              |
 |                   |<------------ +              |              |
 |   "Bob refutes..."|              |              |              |
 |<------------------+              |              |              |
```

Key invariants:

- Refutation walks indices `(suggester+1) % n .. (suggester+n-1) % n`,
  i.e. every other player, in turn order.
- Eliminated players are skipped.
- The first matching card stops the walk; only that one card is shown,
  and only to the suggester.
- The suggester's turn does NOT advance; they may still accuse.

## 3. Accusation (`make_accusation`)

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
