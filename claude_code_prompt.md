# Claude Code Prompt — Fix Cluedo Project Structure

## Context
I am building a Cluedo (Clue) board game in Python using **Pygame** (GUI-based, not CLI).
I have an existing folder structure that was incorrectly set up for a CLI game. I need you to
fix it completely so it is 100% correct before I push to GitHub.

---

## What currently exists (wrong structure)
```
cluedo/
  src/
    game/
      models.py
      engine.py
      deck.py
      rules.py
    ui/
      cli.py        ← WRONG: this is CLI, needs to be removed and replaced
    main.py
  tests/
    test_engine.py
    test_models.py
  docs/
    requirements.md
    architecture.md
    decisions.md
    system_test_report.md
  meetings/
  sprints/
  README.md
  requirements.txt
  .gitignore
```

---

## What the correct final structure should be
```
cluedo/
  src/
    game/
      __init__.py
      models.py
      engine.py
      deck.py
      rules.py
    ui/
      __init__.py
      board.py       ← draws the game board and pieces
      screens.py     ← manages different screens (menu, game, end screen)
      components.py  ← reusable UI elements (buttons, card displays, etc.)
    __init__.py
    main.py          ← Pygame entry point
  assets/
    images/          ← board image, card images, character tokens
    fonts/           ← custom fonts
  tests/
    test_engine.py
    test_models.py
  docs/
    requirements.md
    architecture.md
    decisions.md
    system_test_report.md
  meetings/
  sprints/
  README.md
  requirements.txt
  .gitignore
```

---

## Tasks to complete

### 1. Fix the folder structure
- Delete `src/ui/cli.py`
- Create `src/ui/board.py`, `src/ui/screens.py`, `src/ui/components.py` as empty stubs
- Create `assets/images/` and `assets/fonts/` directories (add a `.gitkeep` file inside each so Git tracks them)
- Ensure all Python package folders have an `__init__.py` file: `src/`, `src/game/`, `src/ui/`

### 2. Fix `requirements.txt`
The file should contain only:
```
pygame
pytest
```

### 3. Fix `README.md`
Rewrite it to say:
```markdown
# Cluedo in Python

A GUI-based Cluedo board game built in Python using Pygame.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to run
```bash
python src/main.py
```

## How to run tests
```bash
pytest
```
```

### 4. Fix `.gitignore`
Rewrite it to contain:
```
# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/
.venv/

# Pygame / raw asset sources
*.psd
*.ai

# OS junk
.DS_Store
Thumbs.db
```

### 5. Write skeleton code for each new file

**`src/main.py`** — Pygame init and main window:
```python
import pygame
from ui.screens import ScreenManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Cluedo")
    clock = pygame.time.Clock()
    manager = ScreenManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update()
        manager.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
```

**`src/ui/screens.py`** — stub:
```python
class ScreenManager:
    def __init__(self, screen):
        self.screen = screen

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background placeholder
```

**`src/ui/board.py`** — stub:
```python
class Board:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pass  # Board drawing logic goes here
```

**`src/ui/components.py`** — stub:
```python
class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = (x, y, width, height)
        self.label = label

    def draw(self, screen):
        pass  # Button drawing logic goes here

    def is_clicked(self, event):
        pass  # Click detection logic goes here
```

### 6. Verify the final structure
After making all changes, run `find . -not -path './.git/*'` and confirm the output matches
the correct final structure shown above exactly.

### 7. Verify Pygame runs
Run `python src/main.py` and confirm a blank Pygame window opens without errors.

---

## Important rules
- Do NOT add any CLI input/output logic anywhere (no `input()`, no `print()` for game flow)
- All game rules stay in `src/game/` — nothing in `src/ui/` should contain game logic
- All files in `src/game/` (models, engine, deck, rules) should remain as empty stubs for now — do not touch them
- Do not modify anything inside `docs/`, `meetings/`, or `sprints/`
