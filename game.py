import pygame
from random import choice
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

ball_speed_x *= choice([1, -1])
ball_speed_y *= choice([1, -1])

countdown_timer = pygame.USEREVENT + 1
pygame.time.set_timer(countdown_timer, 1000)
ball_active = False
count = 3
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_over:
            if event.type == countdown_timer and not ball_active:
                count -= 1
                if count < 1:
                    ball_active = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    opponent_score = 0
                    player_score = 0

    screen.fill(background_color)
    if not game_over:
        player_rect.y = player_input(player_rect.y, player_speed)
        if player_rect.top <= 0:
            player_rect.top = 0
        elif player_rect.bottom >= SCREEN_HEIGHT:
            player_rect.bottom = SCREEN_HEIGHT
        if ball_active:
            ball_rect.x += ball_speed_x
            ball_rect.y += ball_speed_y
            if ball_rect.bottom >= SCREEN_HEIGHT or ball_rect.top <= 0:
                ball_speed_y *= -1
            elif ball_rect.left <= 0:
                opponent_score += 1
                ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                ball_active = False
                count = 3
            elif ball_rect.right >= SCREEN_WIDTH:
                player_score += 1
                ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                ball_active = False
                count = 3

            if ball_rect.colliderect(player_rect) or ball_rect.colliderect(opponent_rect):
                ball_speed_x *= -1

            if ball_rect.x >= SCREEN_WIDTH / 2:
                if opponent_rect.top <= ball_rect.centery:
                    opponent_rect.y += opponent_speed
                elif opponent_rect.bottom >= ball_rect.centery:
                    opponent_rect.y -= opponent_speed

        if opponent_score >= 3 or player_score >= 3:
            game_over = True

        pygame.draw.rect(screen, rect_color, player_rect)
        pygame.draw.rect(screen, rect_color, opponent_rect)
        pygame.draw.aaline(screen, rect_color, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        pygame.draw.ellipse(screen, rect_color, ball_rect)

        player_score_text = game_font.render(f'{player_score}', False, rect_color)
        screen.blit(player_score_text, (SCREEN_WIDTH * .25, 15))

        opponent_score_text = game_font.render(f'{opponent_score}', False, rect_color)
        screen.blit(opponent_score_text, (SCREEN_WIDTH * .75, 15))

        if not ball_active:
            countdown_text = game_font.render(f'{count}', False, rect_color)
            screen.blit(countdown_text, (SCREEN_WIDTH / 2 - 7, SCREEN_HEIGHT / 2 - 40))
    else:
        if opponent_score == 3:
            winner = 'Opponent wins!'
            distance = 140
        else:
            winner = 'You win!'
            distance = 85
        game_over_text = game_font.render('Game Over', False, rect_color)
        winner_text = game_font.render(f'{winner}', False, rect_color)
        play_again_text = game_font.render('Press space to play again', False, rect_color)
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - 100, 50))
        screen.blit(winner_text, (SCREEN_WIDTH / 2 - distance, 100))
        screen.blit(play_again_text, (SCREEN_WIDTH / 2 - 230, 300))

    pygame.display.update()
    clock.tick(60)
