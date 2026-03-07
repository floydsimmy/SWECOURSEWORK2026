# src/game/engine.py
# ===================
# The game engine — the brain of the game.
# It controls the flow of a match from start to finish:
#   - Setting up the game (players, cards, starting positions)
#   - Managing whose turn it is
#   - Processing player actions (moving, making suggestions, making accusations)
#   - Checking win/loss conditions
#
# The engine uses the models from models.py to represent game state,
# and checks rules.py to decide what is and isn't allowed.
import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
Caption = pygame.display.set_caption("Cluedo")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True
while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    win.fill((0,0,0))
    pygame.draw.rect(win, (255,0,0), (x,y,width,height))
    pygame.display.update()

    pygame.quit()