import pygame
from pygame.locals import *
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Block, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((0, 200, 255))
        self.position = [x, y]

pygame.init()
# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

block = Block(40, 40)

# Initial position and size of the snake
snake_head = [200, 150]
snake_segments = [[200, 150], [190, 150], [180, 150]]

movement_direction = 'R'
next_direction = movement_direction

fruit_spawned = True
fruit_image = pygame.image.load('magenta.png')
fruit_image = pygame.transform.scale(fruit_image, (20, 20))
fruit_position = [random.randrange(15, (screen_width // 10)) * 10 - 21, random.randrange(15, (screen_height // 10)) * 10 - 21]

score = 0

# Refresh the display
pygame.display.flip()

running = True
# Main game loop
while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # Clear the old snake position
    block.surf.fill((0, 0, 0))
    for pos in snake_segments:
        block.position = pos
        screen.blit(block.surf, tuple(block.position))
    block.surf.fill((0, 200, 255))

    # Change direction based on key presses
    if keys[K_w] or keys[K_UP]:
        next_direction = 'U'
    if keys[K_a] or keys[K_LEFT]:
        next_direction = 'L'
    if keys[K_s] or keys[K_DOWN]:
        next_direction = 'D'
    if keys[K_d] or keys[K_RIGHT]:
        next_direction = 'R'

    # Ensure the snake doesn't move in the opposite direction instantly
    if next_direction == 'U' and movement_direction != 'D':
        movement_direction = 'U'
    if next_direction == 'D' and movement_direction != 'U':
        movement_direction = 'D'
    if next_direction == 'L' and movement_direction != 'R':
        movement_direction = 'L'
    if next_direction == 'R' and movement_direction != 'L':
        movement_direction = 'R'

    # Move the snake
    if movement_direction == 'U':
        snake_head[1] -= 5
    if movement_direction == 'D':
        snake_head[1] += 5
    if movement_direction == 'L':
        snake_head[0] -= 5
    if movement_direction == 'R':
        snake_head[0] += 5

    # Check if the snake has eaten the fruit
    if (abs(snake_head[0] - fruit_position[0]) < 10 and abs(snake_head[1] - fruit_position[1]) < 10):
        score += 1
        fruit_spawned = False
    else:
        snake_segments.pop()

    # Spawn fruit if not already spawned
    if not fruit_spawned:
        fruit_position = [random.randrange(1, (screen_width // 10)) * 10 - 21, random.randrange(1, (screen_height // 10)) * 10 - 21]
        fruit_spawned = True

    snake_segments.insert(0, list(snake_head))

    # Draw the snake on the screen
    screen.fill((0, 0, 0))
    for pos in snake_segments:
        block.position = pos
        screen.blit(block.surf, tuple(block.position))

    # Draw the fruit on the screen
    block.position = fruit_position
    screen.blit(fruit_image, tuple(block.position))

    # Check if the snake is out of bounds
    if snake_head[0] < 0 or snake_head[0] > screen_width - 20:
        running = False
    if snake_head[1] < 0 or snake_head[1] > screen_height - 20:
        running = False

    # Check if the snake has collided with itself
    for segment in snake_segments[1:]:
        if snake_head[0] == segment[0] and snake_head[1] == segment[1]:
            running = False

    # Refresh the display
    pygame.display.flip()

print("Your score is:", score)
pygame.quit()
