import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (adjust according to your preference)
screen_width = 640
screen_height = 480

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set the initial position of the snake
snake_x = screen_width // 2
snake_y = screen_height // 2

# Set the initial velocity of the snake
snake_dx = 0
snake_dy = 0

# Set the size of each segment of the snake and the space between segments
segment_size = 20
segment_margin = 2

# Create a list to hold the segments of the snake
snake_segments = []

# Set the initial length of the snake
snake_length = 1

# Set the initial position of the food
food_x = random.randint(0, screen_width - segment_size) // segment_size * segment_size
food_y = random.randint(0, screen_height - segment_size) // segment_size * segment_size

# Set the initial position of the food bomb
bomb_x = -segment_size
bomb_y = -segment_size

# Set the clock for controlling the frame rate
clock = pygame.time.Clock()

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set up the font for the score, game over message, and speed window
font = pygame.font.Font(None, 36)

# Function to display the snake, food, and bomb
def draw_snake(snake_color):
    for segment in snake_segments:
        pygame.draw.rect(screen, snake_color, (segment[0], segment[1], segment_size, segment_size))
    pygame.draw.rect(screen, red, (food_x, food_y, segment_size, segment_size))
    pygame.draw.rect(screen, orange, (bomb_x, bomb_y, segment_size, segment_size))

# Function to display the score
def draw_score(score):
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

# Function to display the game over message
def draw_game_over():
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

# Function to display the remaining time for the bomb
def draw_timer(seconds):
    text = font.render("Time: " + str(seconds), True, white)
    screen.blit(text, (10, 50))

# Function to display the speed window and get user input
def get_speed():
    speed = 10  # Default speed
    speed_selected = False
    while not speed_selected:
        screen.fill(black)
        text = font.render("Select Snake Speed:", True, white)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text, text_rect)

        slow_text = font.render("Slow", True, white)
        slow_rect = slow_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(slow_text, slow_rect)

        medium_text = font.render("Medium", True, white)
        medium_rect = medium_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(medium_text, medium_rect)

        fast_text = font.render("Fast", True, white)
        fast_rect = fast_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(fast_text, fast_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if slow_rect.collidepoint(mouse_pos):
                    speed = 5
                    speed_selected = True
                elif medium_rect.collidepoint(mouse_pos):
                    speed = 10
                    speed_selected = True
                elif fast_rect.collidepoint(mouse_pos):
                    speed = 15
                    speed_selected = True

        clock.tick(30)

    return speed

# Function to restart the game
def restart_game():
    global snake_x, snake_y, snake_dx, snake_dy, snake_segments, snake_length, score, game_over, food_x, food_y
    global bomb_x, bomb_y, bomb_active, bomb_start_time

    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_dx = 0
    snake_dy = 0
    snake_segments = []
    snake_length = 1
    score = 0
    game_over = False
    food_x = random.randint(0, screen_width - segment_size) // segment_size * segment_size
    food_y = random.randint(0, screen_height - segment_size) // segment_size * segment_size
    bomb_x = -segment_size
    bomb_y = -segment_size
    bomb_active = False
    bomb_start_time = 0

# Game loop
running = True
score = 0
game_over = False
food_counter = 0
bomb_active = False
bomb_start_time = 0
bomb_duration = 60

# Get the snake speed from the player
snake_speed = get_speed()

# Set up the snake color selector
snake_color_options = [green, blue]
snake_color_index = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_dx != segment_size:
                snake_dx = -segment_size
                snake_dy = 0
            elif event.key == pygame.K_RIGHT and snake_dx != -segment_size:
                snake_dx = segment_size
                snake_dy = 0
            elif event.key == pygame.K_UP and snake_dy != segment_size:
                snake_dx = 0
                snake_dy = -segment_size
            elif event.key == pygame.K_DOWN and snake_dy != -segment_size:
                snake_dx = 0
                snake_dy = segment_size
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                restart_game()
                snake_speed = get_speed()
                snake_color_index = 0

    if not game_over:
        # Update snake position
        snake_x += snake_dx
        snake_y += snake_dy

        # Check for collision with food
        if snake_x == food_x and snake_y == food_y:
            food_x = random.randint(0, screen_width - segment_size) // segment_size * segment_size
            food_y = random.randint(0, screen_height - segment_size) // segment_size * segment_size
            snake_length += 1
            score += 1
            food_counter += 1

            # Check if it's time to show the food bomb
            if food_counter % 7 == 0:
                bomb_x = random.randint(0, screen_width - segment_size) // segment_size * segment_size
                bomb_y = random.randint(0, screen_height - segment_size) // segment_size * segment_size
                bomb_active = True
                bomb_start_time = time.time()

        # Check for collision with bomb
        if snake_x == bomb_x and snake_y == bomb_y:
            game_over = True

        # Check if the bomb has exploded
        if bomb_active and time.time() - bomb_start_time >= bomb_duration:
            bomb_active = False
            bomb_x = -segment_size
            bomb_y = -segment_size

        # Update snake segments
        snake_segments.append((snake_x, snake_y))

        if len(snake_segments) > snake_length:
            del snake_segments[0]

        # Check for collision with snake body
        if (snake_x, snake_y) in snake_segments[:-1]:
            game_over = True

        # Check for collision with screen edges
        if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
            game_over = True

        # Clear the screen with the selected background color
        screen.fill(black)

        # Draw the snake, food, and bomb with the selected snake color
        draw_snake(snake_color_options[snake_color_index])

        # Draw the score
        draw_score(score)

        # Draw the remaining time for the bomb
        if bomb_active:
            draw_timer(int(bomb_duration - (time.time() - bomb_start_time)))

    else:
        # Draw the game over message
        draw_game_over()

    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(snake_speed)

# Quit the game
pygame.quit()
