import pygame
import sys
import platform

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# Nokia 3310 original
NOKIA_ORIGINAL_BG = hex_to_rgb("#c7f0d8")
NOKIA_ORIGINAL_FG = hex_to_rgb("#43523d")

# Nokia 3310 harsh
NOKIA_HARSH_BG = hex_to_rgb("#9bc700")
NOKIA_HARSH_FG = hex_to_rgb("#2b3f09")

# Nokia 3310 gray
NOKIA_GRAY_BG = hex_to_rgb("#879188")
NOKIA_GRAY_FG = hex_to_rgb("#1a1914")

# LCD
LCD_BG = hex_to_rgb("#C0C0C0")
LCD_FG = hex_to_rgb("#000000")

# AMBER
AMBER_BG = hex_to_rgb("#FF8000")
AMBER_FG = hex_to_rgb("#000000")


# Nokia 3310 color palettes
PALETTES = [
    (NOKIA_ORIGINAL_BG, NOKIA_ORIGINAL_FG),  # Default palette
    (NOKIA_HARSH_BG, NOKIA_HARSH_FG),
    (NOKIA_GRAY_BG, NOKIA_GRAY_FG),
    (LCD_BG, LCD_FG),
    (AMBER_BG, AMBER_FG),
]
current_palette_index = 0
BG_COLOR, FG_COLOR = PALETTES[current_palette_index]


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, FG_COLOR, self.rect)


class Ball:
    def __init__(self, x, y, size, dx, dy):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def bounce(self):
        self.dy *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, FG_COLOR, self.rect)


class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, FG_COLOR, self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset_game()

    def reset_game(self):
        self.paddle = Paddle((WIDTH - 100) // 2, HEIGHT - 40, 100, 20, 10)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 10, 4, -4)

        self.bricks = []
        brick_rows = 5
        brick_cols = 10
        brick_width = WIDTH // brick_cols
        brick_height = 30

        for row in range(brick_rows):
            for col in range(brick_cols):
                brick_x = col * brick_width
                brick_y = row * brick_height
                self.bricks.append(Brick(brick_x, brick_y, brick_width, brick_height))

    def check_collisions(self):
        # Ball collision with paddle
        if self.paddle.rect.colliderect(self.ball.rect):
            self.ball.bounce()

        # Ball collision with bricks
        for brick in self.bricks[:]:
            if brick.rect.colliderect(self.ball.rect):
                self.bricks.remove(brick)
                self.ball.bounce()
                break

        # Check for game over
        if self.ball.rect.top > HEIGHT:
            if sys.platform == "emscripten":
                platform.console.log("Game Over! Restarting...")
            else:
                print("Game Over! Restarting...")
            self.reset_game()

    def run(self):
        import asyncio  # Required for pygbag compatibility

        async def main_loop():
            global BG_COLOR, FG_COLOR, current_palette_index

            while self.running:
                self.screen.fill(BG_COLOR)

                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    # Cycle through color palettes
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            current_palette_index = (current_palette_index + 1) % len(
                                PALETTES
                            )
                            BG_COLOR, FG_COLOR = PALETTES[current_palette_index]

                # Move paddle and ball
                keys = pygame.key.get_pressed()
                self.paddle.move(keys)
                self.ball.move()

                # Check collisions
                self.check_collisions()

                # Draw everything
                self.paddle.draw(self.screen)
                self.ball.draw(self.screen)
                for brick in self.bricks:
                    brick.draw(self.screen)

                # Update display
                pygame.display.flip()

                # Cap the frame rate
                self.clock.tick(60)

                await asyncio.sleep(0)  # Allows event loop to yield

            pygame.quit()
            sys.exit()

        asyncio.run(main_loop())


if __name__ == "__main__":
    game = Game()
    game.run()
