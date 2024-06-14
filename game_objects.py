import pygame
from Worker import *


class Bird(pygame.sprite.Sprite):
    # Initialize the Bird instance with the initial x and y positions
    def __init__(self, x, y):
        # Call the initializer of the parent Sprite class
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize a list to store images of the bird
        self.images = []
        
        # Initialize the image index to 0
        self.index = 0
        
        # Initialize a counter for animation or other purposes
        self.counter = 0
        
        # Load three images for the bird and add them to the images list
        for num in range(0, 3):
            img = pygame.image.load(f'sprites/bluebird{num}.png')
            self.images.append(img)
        
        # Set the current image of the bird to the first image in the list
        self.image = self.images[self.index]
        
        # Get the rectangular area of the current image
        self.rect = self.image.get_rect()
        
        # Set the center of the rectangle to the initial x and y positions
        self.rect.center = [x, y]
        
        # Initialize the bird's vertical velocity to 0
        self.vel = 0
        
        # Initialize a flag to track if the bird has been clicked
        self.clicked = False

    # Define an update method to handle the bird's physics and movement
    def update(self):  # physics
        # Check if the bird is flying
        if flying == True:
            # Apply gravity by increasing the velocity
            self.vel += 0.5
            
            # Cap the velocity to a maximum value of 8
            if self.vel > 8:
                self.vel = 8
            
            # Move the bird down if it's not at the bottom of the screen
            if self.rect.bottom < 750:
                self.rect.y += int(self.vel)
            
            # Prevent the bird from moving above the top of the screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0


        # jump physics
        # Check if the game is still running
        if game_over == False:
            # Get the state of all keyboard keys
            keys = pygame.key.get_pressed()
            # Check if the left mouse button is pressed and the player has not clicked before

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                # Set the clicked state to True
                self.clicked = True
                # Set the upward velocity to -10 for a jump effect
                self.vel = -10

             # Check if the space key is pressed and the player has not clicked before

            if keys[pygame.K_SPACE] and not self.clicked:
                 # Set the clicked state to True
                self.clicked = True
                # Set the upward velocity to -10 for a jump effect
                self.vel = -10
            # Reset the clicked state if neither the mouse button nor space key is pressed
            if not any(pygame.mouse.get_pressed()) and not keys[pygame.K_SPACE]:
              # Set the clicked state to False
                self.clicked = False
 # Prevent the player from moving off the top of the screen
            if self.rect.bottom <= 0:
                # Adjust the player's position by adding the vertical velocity
                self.rect.y += int(self.vel)
            # animations
            # Increment the animation counter by 1
            self.counter += 1
            # Set the cooldown period for the flap animation
            flap_cooldown = 5
# Check if the counter exceeds the flap cooldown period
            if self.counter > flap_cooldown:
                # Reset the counter to 0
                self.counter = 0
                # Move to the next image in the animation sequence
                self.index += 1
                # Check if the index is beyond the last image
                if self.index >= len(self.images):
                    # Reset the index to 0 to loop the animation
                    self.index = 0
            
            # Update the current image to display based on the index

            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -60)


# pipes
# Define a class for the pipe sprites
class Pipe(pygame.sprite.Sprite):
    # Initialize the pipe with its position and orientation
    def __init__(self, x, y, position):
        # Initialize the parent Sprite class
        pygame.sprite.Sprite.__init__(self)
        # Load the pipe sprite image
        self.image = pygame.image.load(pipes_sprite)
        # Get the rectangle area of the image
        self.rect = self.image.get_rect()
        # If the pipe is positioned from the top
        if position == 1:
            # Flip the image vertically
            self.image = pygame.transform.flip(self.image, False, True)
            # Position the bottom left of the rectangle at the specified coordinates minus half the gap
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        # If the pipe is positioned from the bottom
        if position == -1:
            # Position the top left of the rectangle at the specified coordinates plus half the gap
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    # Update the pipe's position
    def update(self):
        # Move the pipe to the left by the scroll speed
        self.rect.x -= scroll_speed
        # If the pipe has moved off the screen
        if self.rect.right < 0:
            # Remove the pipe from the sprite group
            self.kill()