import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
SPEED = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
GRAY = (169, 169, 169)

pygame.mixer.music.load('assets/sounds/music_music.mp3')
eat_sound = pygame.mixer.Sound('assets/sounds/music_food.mp3')  
crash_sound = pygame.mixer.Sound('assets/sounds/hit.wav')

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creative Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 20)

# generate obstacles
obstacles = [[random.randint(0, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
              random.randint(0, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE] for _ in range(5)]

def display_score(score):
    """displays the current score on the screen."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def draw_obstacles():
    """draws obstacles on the screen."""
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])

def game_over():
    """displays the game over message and stops the game."""
    screen.fill(BLACK)
    message = font.render("Game Over! Press Q to Quit or R to Restart", True, RED)
    screen.blit(message, [WIDTH // 6, HEIGHT // 3])
    pygame.display.update()
    crash_sound.play()
    time.sleep(2)

def game_loop():
    """main game loop."""
    # snake position at start
    x, y = WIDTH // 2, HEIGHT // 2
    x_change = y_change = 0
    snake_body = []
    snake_length = 1

    # food initial position
    food_x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
    food_y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE

    game_close = False
    game_running = True

    while game_running:
        while game_close:
            game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_running = False
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # update snake position
        x = (x + x_change) % WIDTH
        y = (y + y_change) % HEIGHT

        screen.fill(BLACK)
        draw_obstacles()

        # draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # collision detection
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True
        for obs in obstacles:
            if snake_head == obs:
                game_close = True

        # draw the snake
        for i, segment in enumerate(snake_body):
            if i == len(snake_body) - 1:
                # draw the head with eyes
                pygame.draw.rect(screen, GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])
                pygame.draw.circle(screen, WHITE, (segment[0] + 5, segment[1] + 5), 3)  # left eye
                pygame.draw.circle(screen, WHITE, (segment[0] + 15, segment[1] + 5), 3)  # right eye
                pygame.draw.circle(screen, BLACK, (segment[0] + 5, segment[1] + 5), 1)  # left eye pupil
                pygame.draw.circle(screen, BLACK, (segment[0] + 15, segment[1] + 5), 1)  # right eye pupil
            else:
                pygame.draw.rect(screen, BLUE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        # check if snake eats food
        if x == food_x and y == food_y:
            food_x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            food_y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            snake_length += 1
            eat_sound.play()  # play the food eat sound

        display_score(snake_length - 1)

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

# start the game
game_loop()
