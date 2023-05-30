import pygame
from pac import *
pygame.init()


WINDOW_WIDTH = 606
WINDOW_HEIGHT = 606
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background_image = pygame.image.load('background2.jpg').convert()
background_image = pygame.transform.scale(background_image, (1072,606))
pygame.display.set_caption("Pacman")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.Font(cfg.FONTPATH, 16)   
text = font.render("The goal of the game: collect all coins.\n Arrow control. Q - teleport forward for a short distance (you can teleport between walls), the player can teleport 3 times in a game. There are 2 teleports on the right and left side of the map that can be used without restrictions. Also, a random number of cherries appear on the field, picking which pacman gets invulnerability to ghosts for a short period of time.", True, BLACK)
def draw_rect():
    rect = pygame.Rect(15, 15, 576, 200)
    pygame.draw.rect(window, cfg.SKYBLUE, rect)
def infostart():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    window.blit(background_image, (0, 0))
    draw_rect()
    window.blit(text, (20,20))
    pygame.display.update()

pygame.quit()