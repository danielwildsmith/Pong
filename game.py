import pygame
from random import randint
from sys import exit


def player_input(y_pos, speed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y_pos -= speed
    elif keys[pygame.K_DOWN]:
        y_pos += speed
    return y_pos


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 6
PADDLE_HEIGHT = 65
BALL_SIZE = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
game_font = pygame.font.Font('Kiona-Regular.ttf', 30)

player_rect = pygame.Rect((5, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
player_speed = 5
player_score = 0

opponent_rect = pygame.Rect((SCREEN_WIDTH - 5 - PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2),
                            (PADDLE_WIDTH, PADDLE_HEIGHT))
opponent_speed = 3
opponent_score = 0

ball_rect = pygame.Rect((SCREEN_WIDTH / 2 - BALL_SIZE / 2, SCREEN_HEIGHT / 2 - BALL_SIZE / 2), (BALL_SIZE, BALL_SIZE))
ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
ball_speed_x = 5
ball_speed_y = 5

background_color = pygame.Color('grey15')
rect_color = pygame.Color('lightgrey')

if randint(0, 2):
    ball_speed_x *= -1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player_rect.y = player_input(player_rect.y, player_speed)
    if player_rect.top <= 0:
        player_rect.top = 0
    elif player_rect.bottom >= SCREEN_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y
    if ball_rect.bottom >= SCREEN_HEIGHT or ball_rect.top <= 0:
        ball_speed_y *= -1
    elif ball_rect.left <= 0:
        opponent_score += 1
        ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    elif ball_rect.right >= SCREEN_WIDTH:
        player_score += 1
        ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    if ball_rect.colliderect(player_rect) or ball_rect.colliderect(opponent_rect):
        ball_speed_x *= -1

    if ball_rect.x >= SCREEN_WIDTH / 2:
        if opponent_rect.top <= ball_rect.centery:
            opponent_rect.y += opponent_speed
        elif opponent_rect.bottom >= ball_rect.centery:
            opponent_rect.y -= opponent_speed

    screen.fill(background_color)
    pygame.draw.rect(screen, rect_color, player_rect)
    pygame.draw.rect(screen, rect_color, opponent_rect)
    pygame.draw.aaline(screen, rect_color, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
    pygame.draw.ellipse(screen, rect_color, ball_rect)

    player_score_text = game_font.render(f'{player_score}', False, rect_color)
    screen.blit(player_score_text, (SCREEN_WIDTH * .25, 15))

    opponent_score_text = game_font.render(f'{opponent_score}', False, rect_color)
    screen.blit(opponent_score_text, (SCREEN_WIDTH * .75, 15))

    pygame.display.update()
    clock.tick(60)
