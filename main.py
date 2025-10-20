'''
┌──────────────────────────────┐
│          Game Loop           │
│                              │
│  ┌────────────────────────┐  │
│  │ 1. Handle Input        │  │ ← Move paddles
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ 2. Update Ball         │  │ ← Update position by velocitys
│  │     - Move             │  │ ← pos += dir * speed * dt
│  │     - Check Collisions │  │ ← Walls / Paddles
│  │     - Reset if Missed  │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ 3. Draw Everything     │  │
│  └────────────────────────┘  │
└──────────────────────────────┘

'''

import pygame
import random
import math

# Initialize Pygame
pygame.init()

pygame.display.set_caption("pong -- by nibbleton")

# Screen setup
screen = pygame.display.set_mode((1920, 1000))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
pad_width, pad_height = 20, 150

# circle properties
ball_radius = 10

# Use geometric center for positions
red_pos = pygame.Vector2(pad_width/2, screen.get_height()/2)  # LEFT paddle center
blue_pos = pygame.Vector2(screen.get_width() - pad_width/2, screen.get_height()/2)  # RIGHT paddle center

# Movement speed (pixels per second)
speed = 1000

running = True
dt = 0  # Delta time

ball_speed = 3
ball_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

x_direction_normalised_global, y_direction_normalised_global = 0, 0

def clamp_paddle(position_y):
    position_y = max(pad_height/2, position_y)  # top boundary
    position_y = min(screen.get_height() - pad_height/2, position_y)  # bottom boundary
    return position_y

def handle_input():
    global ball_running

    keys = pygame.key.get_pressed()
    
    # LEFT paddle movement
    if keys[pygame.K_w]:
        red_pos.y -= speed * dt
    if keys[pygame.K_s]:
        red_pos.y += speed * dt

    # RIGHT paddle movement
    if keys[pygame.K_UP]:
        blue_pos.y -= speed * dt
    if keys[pygame.K_DOWN]:
        blue_pos.y += speed * dt
    
    if keys[pygame.K_SPACE]:
        ball_running = True

def get_ball_direction():
    global x_direction_normalised_global, y_direction_normalised_global

    x_direction_non_normalised = 2*screen.get_width()*random.random() - screen.get_width()
    y_direction_non_normalised = 2*screen.get_height()*random.random() - screen.get_height()

    norm = math.sqrt(x_direction_non_normalised**2 + y_direction_non_normalised**2)

    x_direction_normalised, y_direction_normalised = x_direction_non_normalised/norm, y_direction_non_normalised/norm

    x_direction_normalised_global, y_direction_normalised_global = x_direction_normalised, y_direction_normalised
    return x_direction_normalised, y_direction_normalised

x_direction_normalised_global, y_direction_normalised_global = get_ball_direction()
ball_running = False

blue_score, red_score = 0, 0

font_size = 200
font = pygame.font.Font("boldpixels/BoldPixels.ttf", font_size)

final_text_size = 100

while running:

    # HANDLE EVENTS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if red_score == 1:
        screen.fill((0, 0, 0))
        final_text_content = "RIGHT WON!"
        final_text = font.render(final_text_content, True, (255, 255, 255))
        screen.blit(blue_score_text, (screen.get_width()/2 - screen.get_width()/4 - final_text_size/2, 50))  # top-left corner
        screen.blit(red_score_text, (screen.get_width()/2 + screen.get_width()/4 - final_text_size/2, 50))  # top-left corner
        screen.blit(final_text, (screen.get_width()/2 - len(final_text_content)*final_text_size/2, screen.get_height()/2 - final_text_size/2))
        pygame.display.flip()
        continue
    if blue_score == 1:
        screen.fill((0, 0, 0))
        final_text_content = "LEFT WON!"
        final_text = font.render(final_text_content, True, (255, 255, 255))
        screen.blit(blue_score_text, (screen.get_width()/2 - screen.get_width()/4 - font_size/2, 50))  # top-left corner
        screen.blit(red_score_text, (screen.get_width()/2 + screen.get_width()/4 - font_size/2, 50))  # top-left corner
        screen.blit(final_text, (screen.get_width()/2 - len(final_text_content)*final_text_size/2, screen.get_height()/2 - final_text_size/2))
        pygame.display.flip()
        continue

    blue_score_text = font.render(str(blue_score), True, (255, 255, 255))
    red_score_text = font.render(str(red_score), True, (255, 255, 255))
    screen.blit(blue_score_text, (240, 50))  # top-left corner
    screen.blit(red_score_text, (780, 50))  # top-left corner

    # --- INPUT ---
    handle_input()

    # --- UPDATE BALL ---
    if ball_running:
        ball_pos.x += x_direction_normalised_global*ball_speed
        ball_pos.y += y_direction_normalised_global*ball_speed

        if ball_pos.y >= screen.get_height() or ball_pos.y <= 0:
            y_direction_normalised_global *= -1

        ball_rect = pygame.Rect(
            ball_pos.x - ball_radius,
            ball_pos.y - ball_radius,
            ball_radius * 2,
            ball_radius * 2
        )

        red_rect = pygame.Rect(
            red_pos.x - pad_width / 2,
            red_pos.y - pad_height / 2,
            pad_width,
            pad_height
        )

        blue_rect = pygame.Rect(
            blue_pos.x - pad_width / 2,
            blue_pos.y - pad_height / 2,
            pad_width,
            pad_height
        )

        if ball_rect.colliderect(red_rect):
            x_direction_normalised_global *= -1
            ball_pos.x = red_rect.right + ball_radius  # push it out a bit

            ball_speed += 1

        elif ball_rect.colliderect(blue_rect):
            x_direction_normalised_global *= -1
            ball_pos.x = blue_rect.left - ball_radius  # push it out a bit

            ball_speed += 1

        if ball_pos.x < 0:
            ball_pos.x, ball_pos.y = screen.get_width()/2, screen.get_height()/2
            ball_running = False
            x_direction_normalised_global, y_direction_normalised_global = get_ball_direction()
            red_score += 1

        elif ball_pos.x > screen.get_width():
            ball_pos.x, ball_pos.y = screen.get_width()/2, screen.get_height()/2
            ball_running = False
            x_direction_normalised_global, y_direction_normalised_global = get_ball_direction()
            blue_score += 1


    # --- Keep paddles on screen ---
    red_pos.y = clamp_paddle(red_pos.y)
    blue_pos.y = clamp_paddle(blue_pos.y)

    # --- DRAW EVERYTHING ---
    screen.fill(BLACK)
    # Draw paddles using center-based coordinates
    pygame.draw.rect(screen, WHITE, (red_pos.x - pad_width/2, red_pos.y - pad_height/2, pad_width, pad_height))
    pygame.draw.rect(screen, WHITE, (blue_pos.x - pad_width/2, blue_pos.y - pad_height/2, pad_width, pad_height))

    pygame.draw.circle(screen, "white", ball_pos, ball_radius)

    screen.blit(blue_score_text, (screen.get_width()/2 - screen.get_width()/4 - font_size/2, 50))  # top-left corner
    screen.blit(red_score_text, (screen.get_width()/2 + screen.get_width()/4 - font_size/2, 50))  # top-left corner
    pygame.display.flip()

    # --- Frame timing ---
    dt = clock.tick(100) / 1000  # Seconds since last frame

pygame.quit()