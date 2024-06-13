# Import the pygame library for game development
import pygame

# Import the random module for generating random numbers
import random

# Import the Sprite class from pygame.sprite module
from pygame.sprite import Sprite

# Bird class for player's character, inheriting from Sprite
class Bird(Sprite):
    # Constructor method for initializing the Bird object
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Load bird images for animation and store them in a list
        self.images = [pygame.image.load(f'sprites/bluebird{num}.png') for num in range(3)]
        # Initialize the image index and animation counter
        self.index = 0
        self.counter = 0
        # Set the initial image and get its rectangle
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        # Initialize the velocity and clicked status
        self.vel = 0
        self.clicked = False

    # Method to update the bird's state
    def update(self, flying, game_over):
        # If the game is in flying mode
        if flying:
            # Increase the velocity to simulate gravity
            self.vel += 0.5
            # Cap the maximum velocity
            if self.vel > 8:
                self.vel = 8
            # Update the bird's position if it's within screen bounds
            if self.rect.bottom < 750:
                self.rect.y += int(self.vel)
            # Prevent the bird from moving off the top of the screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0

        # If the game is not over
        if not game_over:
            # Get the state of all keyboard keys
            keys = pygame.key.get_pressed()
            # Get the state of the left mouse button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            # If the left mouse button is pressed and the bird was not previously clicked
            if mouse_pressed and not self.clicked:
                self.clicked = True
                self.vel = -10  # Make the bird jump
            # If the space key is pressed and the bird was not previously clicked
            if keys[pygame.K_SPACE] and not self.clicked:
                self.clicked = True
                self.vel = -10  # Make the bird jump
            # If neither the mouse button nor the space key are pressed, reset clicked status
            if not any(pygame.mouse.get_pressed()) and not keys[pygame.K_SPACE]:
                self.clicked = False

            # Set the cooldown period for the flap animation
            flap_cooldown = 5
            # Increment the animation counter
            self.counter += 1
            # Update the bird's image based on the animation counter
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            # Rotate the bird's image based on its velocity
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)

        # If the game is over, set the bird's image to a fixed angle
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -60)

# Pipe class for obstacles, inheriting from Sprite
class Pipe(Sprite):
    # Constructor method for initializing the Pipe object
    def __init__(self, x, y, position, pipe_gap, pipes_sprite, scroll_speed):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Load the pipe image
        self.image = pygame.image.load(pipes_sprite)
        # Get the rectangle of the pipe image
        self.rect = self.image.get_rect()
        # If the pipe is an upper pipe, flip it vertically and set its position
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        # If the pipe is a lower pipe, set its position
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    # Method to update the pipe's position
    def update(self, scroll_speed):
        # Move the pipe leftward by the scroll speed
        self.rect.x -= scroll_speed
        # If the pipe moves off the screen, remove it
        if self.rect.right < 0:
            self.kill()
