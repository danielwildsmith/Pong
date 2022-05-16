import pygame
from sys import exit
pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pong')

player_one_rect = pygame.Rect((100, 175), (10, 50))
player_two_rect = pygame.Rect((700, 175), (10, 50))
game_font = pygame.font.Font('retganon.ttf', 50)
title_surface = game_font.render('Pong', False, 'White')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.draw.rect(screen, 'white', player_one_rect)
    pygame.draw.rect(screen, 'white', player_two_rect)
    screen.blit(title_surface, title_surface.get_rect(center=(400, 50)))

    pygame.display.update()
