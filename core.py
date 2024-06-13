# Import necessary modules and classes
import pygame  # Main pygame library
import csv  # CSV handling library
from csv import *  # Import everything from csv module
import os  # OS library for file handling
import sys  # System-specific parameters and functions
import random  # Random number generation
import Worker  # Custom module for worker
import Groups  # Custom module for groups
from Groups import *  # Import everything from Groups module
from Worker import *  # Import everything from Worker module
from pygame import *  # Import everything from pygame
from pygame.sprite import Group  # Group class from pygame.sprite for managing groups of sprites
from pygame.locals import *  # Import pygame constants
from classes import Bird  # Import Bird class from classes module

# Initialize pygame
pygame.init()

# Set the title and icon for the game window
pygame.display.set_caption(gameTitle)
pygame.display.set_icon(icon)

# Load background and ground images
bg = pygame.image.load(background)
base = pygame.image.load(ground)
base_width = base.get_width()
base_positions = [0, base_width]  # Base positions for scrolling effect

# Game variables
score = 0
pipe_gap = 150  # Gap between pipes
pipe_frequency = 1500  # Frequency of pipe generation in milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency  # Track the last pipe creation time

# Load fonts
font = pygame.font.Font(my_font, 30)
large_font = pygame.font.Font(my_font, 40)
small_font = pygame.font.Font(my_font, 15)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)  # Render text
    textrect = textobj.get_rect()  # Get the text rectangle
    textrect.topleft = (x, y)  # Set the position of the text
    surface.blit(textobj, textrect)  # Draw the text on the surface

# Bird update method to handle physics
def update(self):  # physics

    # Gravity
    if flying == True:
        self.vel += 0.5  # Increase velocity for gravity effect
        if self.vel > 8:
            self.vel = 8  # Cap the maximum velocity
        if self.rect.bottom < 750:
            self.rect.y += int(self.vel)  # Update the bird's vertical position
        if self.rect.top < 0:
            self.rect.top = 0  # Prevent the bird from moving off the top of the screen
            self.vel = 0

    # Jump physics
    if game_over == False:
        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys

        # Handle mouse click for jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10  # Make the bird jump

        # Handle space key for jump
        if keys[pygame.K_SPACE] and not self.clicked:
            self.clicked = True
            self.vel = -10  # Make the bird jump

        # Reset clicked status if mouse or space key is not pressed
        if not any(pygame.mouse.get_pressed()) and not keys[pygame.K_SPACE]:
            self.clicked = False

        if self.rect.bottom <= 0:
            self.rect.y += int(self.vel)  # Update the bird's vertical position

        # Animation handling
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]  # Update bird's image

        # Rotate the bird based on velocity
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
    else:
        self.image = pygame.transform.rotate(self.images[self.index], -60)  # Rotate the bird when game over

# Pipe update method to handle scrolling
def update(self):
    self.rect.x -= scroll_speed  # Move the pipe leftward by the scroll speed
    if self.rect.right < 0:
        self.kill()  # Remove the pipe if it moves off the screen

# Function to measure text width
def measure_text_width(text, font):
    textobj = font.render(text, True, (0, 0, 0))  # Render text
    return textobj.get_width()  # Return the width of the text

# Function to handle player input for nickname and difficulty
def player_input():
    input_active = True
    nickname = ""
    difficulty = ""
    valid_difficulties = ['easy', 'medium', 'hard']
    stage = "nickname"

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if stage == "nickname" and nickname:
                        stage = "difficulty"
                    elif stage == "difficulty" and difficulty in valid_difficulties:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if stage == "difficulty":
                        difficulty = difficulty[:-1]
                    elif stage == "nickname":
                        nickname = nickname[:-1]
                else:
                    if stage == "nickname" and len(nickname) < 10:
                        nickname += event.unicode
                    elif stage == "difficulty" and len(difficulty) < 6:
                        difficulty += event.unicode
        screen.fill((0, 0, 0))  # Clear screen
        draw_text('Enter your nickname:', font, (255, 255, 255), screen, 150, 350)
        nickname_width = measure_text_width(nickname, large_font)
        draw_text(nickname, large_font, (255, 255, 255), screen, 300 - nickname_width / 2, 400)
        if nickname:
            draw_text('Enter difficulty (easy, medium, hard):', small_font, (255, 255, 255), screen, 150, 450)
            difficulty_width = measure_text_width(difficulty, small_font)
            draw_text(difficulty, small_font, (255, 255, 255), screen, 300 - difficulty_width / 2, 500)

        pygame.display.update()  # Update display

    return nickname, difficulty

# Get player input for nickname and difficulty
nickname, difficulty = player_input()
print(f"Nickname: {nickname}", f"Difficulty: {difficulty}")

# Function to set game parameters based on difficulty
def set_difficulty_params(difficulty):
    global scroll_speed, pipe_frequency, pipe_gap

    if difficulty == "easy":
        scroll_speed = 3
        pipe_frequency = 2000
        pipe_gap = 200
    elif difficulty == "medium":
        scroll_speed = 4
        pipe_frequency = 1500
        pipe_gap = 150
    elif difficulty == "hard":
        scroll_speed = 5
        pipe_frequency = 1000
        pipe_gap = 100
    else:
        "medium"  # Default to medium if invalid difficulty

# Set the game parameters based on chosen difficulty
set_difficulty_params(difficulty)

# Create sprite groups for birds and pipes
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Create a Bird object and add it to the bird group
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Function to update the leaderboard with player's score
def update_leaderboard(nickname, score):
    try:
        file_path = os.path.join(os.getcwd(), 'leaderboard.csv')
        file_exist = os.path.isfile(file_path)
        leaderboard = []
        found = False

        if file_exist:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row[0] == nickname:
                        best_score = int(row[2])
                        if score > best_score:
                            best_score = score
                        leaderboard.append([nickname, score, best_score])
                        found = True
                    else:
                        leaderboard.append(row)
        else:
            print("Leaderboard file does not exist. It will be created.")

        if not found:
            leaderboard.append([nickname, score, score])

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nickname', 'Last Score', 'Best Score'])
            writer.writerows(leaderboard)
            print("Leaderboard updated.")
    except Exception as e:
        print(f"Error updating leaderboard: {e}")

# Function to display the leaderboard
def display_leaderboard():
    try:
        file_path = os.path.join(os.getcwd(), 'leaderboard.csv')
        if not os.path.isfile(file_path):
            print("No leaderboard data found")
            return

        screen.fill((0, 0, 0))  # Clear screen
        draw_text('LEADER BOARD', large_font, (255, 255, 255), screen, 150, 50)

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            print(f"Header: {header}")
            y_offset = 150
            for row in reader:
                print(f"Row: {row}")
                draw_text(f"{row[0]}: Last Score: {row[1]}, Best Score: {row[2]}", small_font, (255, 255, 255), screen, 50, y_offset)
                y_offset += 30
        pygame.display.update()
    except Exception as e:
        print(f"Error displaying leaderboard: {e}")

# Display the leaderboard
display_leaderboard()

# Main game loop
run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Scroll the base for visual effect
    for i in range(len(base_positions)):
        base_positions[i] -= scroll_speed
        if base_positions[i] <= -base_width:
            base_positions[i] = base_width

    screen.blit(bg, (0, 0))  # Draw background
    for i in range(len(base_positions)):
        screen.blit(base, (base_positions[i], 700))  # Draw base

    bird_group.update()  # Update bird group
    pipe_group.update()  # Update pipe group

    bird_group.draw(screen)  # Draw bird group
    pipe_group.draw(screen)  # Draw pipe group

    score_text = large_font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (300, 100))  # Draw score

    pygame.display.update()  # Update display

pygame.quit()  # Quit pygame
sys.exit()  # Exit the script



