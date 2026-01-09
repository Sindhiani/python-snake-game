import pygame
import random
import sys

# -------------------- INITIAL SETUP --------------------
pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

# -------------------- FUNCTIONS --------------------
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (*block, BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def game_over(score):
    screen.fill(BLACK)
    msg = font.render("Game Over!", True, RED)
    score_msg = font.render(f"Final Score: {score}", True, WHITE)
    restart_msg = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(msg, (WIDTH//2 - 80, HEIGHT//2 - 60))
    screen.blit(score_msg, (WIDTH//2 - 90, HEIGHT//2 - 20))
    screen.blit(restart_msg, (WIDTH//2 - 160, HEIGHT//2 + 20))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# -------------------- MAIN GAME LOOP --------------------
def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (BLOCK_SIZE, 0)

    food = (
        random.randrange(0, WIDTH, BLOCK_SIZE),
        random.randrange(0, HEIGHT, BLOCK_SIZE)
    )

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                    direction = (0, -BLOCK_SIZE)
                if event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                    direction = (0, BLOCK_SIZE)
                if event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                    direction = (-BLOCK_SIZE, 0)
                if event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                    direction = (BLOCK_SIZE, 0)

        # Move snake
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        snake.insert(0, new_head)

        # Eat food
        if new_head == food:
            score += 1
            food = (
                random.randrange(0, WIDTH, BLOCK_SIZE),
                random.randrange(0, HEIGHT, BLOCK_SIZE)
            )
        else:
            snake.pop()

        # Collision with wall
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            game_over(score)

        # Collision with itself
        if new_head in snake[1:]:
            game_over(score)

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        show_score(score)

        pygame.display.update()
        clock.tick(10)

# -------------------- START GAME --------------------
main()
