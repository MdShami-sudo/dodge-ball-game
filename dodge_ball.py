import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SKYBLUE = (255, 255, 255)
GREEN = (0, 0, 0)
RED = (255, 0, 0)

player_size = 50
player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT-2*player_size]
player_speed = 30

ball_size = 30
ball_pos = [random.randint(0, SCREEN_WIDTH-ball_size), 0]
ball_speed = 10

game_over = False
clock = pygame.time.Clock()
score = 0

font = pygame.font.SysFont("monospace", 35)

def drop_balls(ball_list):
    delay = random.random()
    if len(ball_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH-ball_size)
        y_pos = 0
        ball_list.append([x_pos, y_pos])

def draw_balls(ball_list):
    for ball_pos in ball_list:
        pygame.draw.circle(screen, RED, (ball_pos[0] + ball_size//2, ball_pos[1] + ball_size//2), ball_size//2)

def update_ball_positions(ball_list, score):
    for idx, ball_pos in enumerate(ball_list):
        if ball_pos[1] >= 0 and ball_pos[1] < SCREEN_HEIGHT:
            ball_pos[1] += ball_speed
        else:
            ball_list.pop(idx)
            score += 1
    return score

def detect_collision(player_pos, ball_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    
    b_x = ball_pos[0]
    b_y = ball_pos[1]
    
    if (b_x >= p_x and b_x < (p_x + player_size)) or (p_x >= b_x and p_x < (b_x + ball_size)):
        if (b_y >= p_y and b_y < (p_y + player_size)) or (p_y >= b_y and p_y < (b_y + ball_size)):
            return True
    return False

def check_collisions(ball_list, player_pos):
    for ball_pos in ball_list:
        if detect_collision(player_pos, ball_pos):
            return True
    return False

ball_list = [ball_pos]

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_speed
            elif event.key == pygame.K_RIGHT:
                x += player_speed
            player_pos = [x, y]
    
    screen.fill(GREEN)
    
    drop_balls(ball_list)
    score = update_ball_positions(ball_list, score)
    
    if check_collisions(ball_list, player_pos):
        game_over = True
        break
    
    draw_balls(ball_list)
    
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    
    text = font.render("Score: {}".format(score), True, SKYBLUE)
    screen.blit(text, (10, 10))
    
    clock.tick(30)
    pygame.display.update()

pygame.quit()

