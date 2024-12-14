import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BG_COLOR = (0, 125, 255)
FG_COLOR = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle properties
paddle_width = 100
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 40
paddle_speed = 10

# Ball properties
ball_size = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = -4

# Brick properties
brick_rows = 5
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

# Create bricks
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * brick_width
        brick_y = row * brick_height
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= WIDTH - ball_size:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # Ball collision with paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    if paddle_rect.colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size)):
        ball_dy *= -1

    # Ball collision with bricks
    for brick in bricks[:]:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size)):
            bricks.remove(brick)
            ball_dy *= -1
            break

    # Check for game over
    if ball_y > HEIGHT:
        print("Game Over!")
        running = False

    # Draw paddle
    pygame.draw.rect(
        screen, FG_COLOR, (paddle_x, paddle_y, paddle_width, paddle_height)
    )

    # Draw ball
    pygame.draw.rect(screen, FG_COLOR, (ball_x, ball_y, ball_size, ball_size))

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, FG_COLOR, brick)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
