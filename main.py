import pygame

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((1920, 1000))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
pad_width, pad_height = 20, 150

# circle properties
ball_size = 10

# Use geometric center for positions
red_pos = pygame.Vector2(pad_width/2, screen.get_height()/2)  # LEFT paddle center
blue_pos = pygame.Vector2(screen.get_width() - pad_width/2, screen.get_height()/2)  # RIGHT paddle center

ball_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)


# Movement speed (pixels per second)
speed = 1000

running = True
dt = 0  # Delta time

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
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

    # --- Keep paddles on screen ---
    # Use center-based boundaries
    red_pos.y = max(pad_height/2, red_pos.y)  # top boundary
    red_pos.y = min(screen.get_height() - pad_height/2, red_pos.y)  # bottom boundary

    blue_pos.y = max(pad_height/2, blue_pos.y) # top boundary
    blue_pos.y = min(screen.get_height() - pad_height/2, blue_pos.y)  # bottom boundary

    # --- Drawing ---
    screen.fill(BLACK)
    # Draw paddles using center-based coordinates
    pygame.draw.rect(screen, WHITE, (red_pos.x - pad_width/2, red_pos.y - pad_height/2, pad_width, pad_height))
    pygame.draw.rect(screen, WHITE, (blue_pos.x - pad_width/2, blue_pos.y - pad_height/2, pad_width, pad_height))

    pygame.draw.circle(screen, "white", ball_pos, ball_size)

    pygame.display.flip()

    # --- Frame timing ---
    dt = clock.tick(100) / 1000  # Seconds since last frame

pygame.quit()