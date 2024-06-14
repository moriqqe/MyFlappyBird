# Import the pygame module, which is used for creating games and multimedia applications
import pygame

import time

# Import the csv module, which provides functionality to read from and write to CSV files
import csv

# Import everything from the csv module to make its functions directly accessible
from csv import *

# Import the os module, which provides functions for interacting with the operating system
import os

# Import the random module, which provides functions for generating random numbers
import random

# Import the Worker module, which is likely a custom module for handling worker-related functionalities
import Worker

# Import the Groups module, which is likely a custom module for handling group-related functionalities
import Groups

# Import everything from the Groups module to make its functions and classes directly accessible
from Groups import *

# Import everything from the Worker module to make its functions and classes directly accessible
from Worker import *

# Import everything from the pygame module to make its functions and classes directly accessible
from pygame import *

# Import the Group class from pygame.sprite module, used for handling groups of sprites
from pygame.sprite import Group

# Import everything from the pygame.locals module, which contains constants used by pygame
from pygame.locals import *

from game_objects import Bird, Pipe

# Initialize all imported pygame modules
pygame.init()

# Set the window title to the value of the variable gameTitle
pygame.display.set_caption(gameTitle)

# Set the window icon to the image referenced by the variable icon
pygame.display.set_icon(icon)

# Load the background image from the file path stored in the variable background
bg = pygame.image.load(background)

# Load the ground image from the file path stored in the variable ground
base = pygame.image.load(ground)

# Get the width of the base image and store it in the variable base_width
base_width = base.get_width()

# Initialize a list with two elements: 0 and the width of the base image. This is likely for scrolling the ground.
base_positions = [0, base_width]

# Initialize the game score to 0
score = 0
game_scores = []
report_interval = 60
start_time = pygame.time.get_ticks()  # Store the start time
end_time = pygame.time.get_ticks()
playtime = (end_time - start_time) / 1000  # Convert milliseconds to seconds



# Get the current time in milliseconds since pygame.init() was called and subtract the pipe_frequency value. 
# This initializes last_pipe to ensure a pipe is created immediately when the game starts.
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Load the font from the file path stored in the variable my_font, set the size to 30 pixels, and store it in the variable font
font = pygame.font.Font(my_font, 30)

# Load the font from the same file path but with a size of 40 pixels, and store it in the variable large_font
large_font = pygame.font.Font(my_font, 40)

# Load the font from the same file path but with a size of 15 pixels, and store it in the variable small_font
small_font = pygame.font.Font(my_font, 15)

# Define a function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    # Render the text into an image (Surface) with the given font and color
    textobj = font.render(text, True, color)
    
    # Get the rectangular area of the text image
    textrect = textobj.get_rect()
    
    # Set the top-left corner of this rectangle to the (x, y) position
    textrect.topleft = (x, y)
    
    # Draw the text image onto the provided surface at the specified position
    surface.blit(textobj, textrect)

# Define a Bird class that inherits from pygame's Sprite class


# Function to measure the width of the rendered text
def measure_text_width(text, font):
    # Render the text with the specified font
    textobj = font.render(text, True, (0, 0, 0))
    # Return the width of the rendered text
    return textobj.get_width()

# Function to handle player input for nickname and difficulty
def player_input():
    # Set the input active flag to True
    input_active = True
    # Initialize the nickname and difficulty as empty strings
    nickname = ""
    difficulty = ""
    # Define the valid difficulty options
    valid_difficulties = ['easy', 'medium', 'hard']
    # Set the initial input stage to "nickname"
    stage = "nickname"

    # Continue taking input while input is active
    while input_active:
        # Handle events in the event queue
        for event in pygame.event.get():
            # If the quit event is triggered, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If a key is pressed down
            if event.type == pygame.KEYDOWN:
                # If the Enter key is pressed
                if event.key == pygame.K_RETURN:
                    # If in the nickname stage and nickname is entered, move to difficulty stage
                    if stage == "nickname" and nickname:
                        stage = "difficulty"
                    # If in the difficulty stage and a valid difficulty is entered, end input
                    elif stage == "difficulty" and difficulty in valid_difficulties:
                        input_active = False
                # If the Backspace key is pressed, remove the last character from the input
                elif event.key == pygame.K_BACKSPACE:
                    if stage == "difficulty":
                        difficulty = difficulty[:-1]
                    elif stage == "nickname":
                        nickname = nickname[:-1]
                # Add the unicode character of the key to the appropriate input string
                else:
                    if stage == "nickname" and len(nickname) < 10:
                        nickname += event.unicode
                    elif stage == "difficulty" and len(difficulty) < 6:
                        difficulty += event.unicode
        # Fill the screen with black color
        screen.fill((0, 0, 0))
        # Draw the prompt for entering nickname
        draw_text('Enter your nickname:', font, (255, 255, 255), screen, 150, 350)
        # Measure the width of the entered nickname
        nickname_width = measure_text_width(nickname, large_font)
        # Draw the entered nickname centered on the screen
        draw_text(nickname, large_font, (255, 255, 255), screen, 300 - nickname_width / 2, 400)
        # If a nickname is entered, prompt for difficulty
        if nickname:
            draw_text('Enter difficulty (easy, medium, hard):', small_font, (255, 255, 255), screen, 150, 450)
            # Measure the width of the entered difficulty
            difficulty_width = measure_text_width(difficulty, small_font)
            # Draw the entered difficulty centered on the screen
            draw_text(difficulty, small_font, (255, 255, 255), screen, 300 - difficulty_width / 2, 500)

        # Update the display with the new drawings
        pygame.display.update()
# Return the player's nickname and chosen difficulty
    return nickname, difficulty


# Call the player_input function to get the player's nickname and difficulty
nickname, difficulty = player_input()
# Print the player's nickname and difficulty to the console
print(f"Nickname: {nickname}", f"Difficulty: {difficulty}")

# Define a function to set game parameters based on the chosen difficulty
def set_difficulty_params(difficulty):
     # Declare the game parameters as global variables
    global scroll_speed, pipe_frequency, pipe_gap
# Set parameters for "easy" difficulty
    if difficulty == "easy":
        scroll_speed = 3 # Set the scroll speed to 3
        pipe_frequency = 2000 # Set the scroll speed to 3
        pipe_gap = 200 # Set the gap between pipes to 200 pixels
        # Set parameters for "medium" difficulty
    elif difficulty == "medium":
        scroll_speed = 4 # Set the scroll speed to 4
        pipe_frequency = 1500 # Set the pipe frequency to 1500 milliseconds
        pipe_gap = 150  # Set the gap between pipes to 150 pixels
    # Set parameters for "hard" difficulty
    elif difficulty == "hard":
        scroll_speed = 5 # Set the scroll speed to 5
        pipe_frequency = 1000 # Set the pipe frequency to 1000 milliseconds
        pipe_gap = 100  # Set the gap between pipes to 100 pixels
    # Default to "medium" difficulty if an invalid option is given
    else:
        "medium" # This line appears to be incomplete and should ideally set default parameters

# Set the game parameters based on the chosen difficulty level
set_difficulty_params(difficulty)

# Create a sprite group for the bird
bird_group = pygame.sprite.Group()
# Create a sprite group for the pipes
pipe_group = pygame.sprite.Group()

# Create a Bird object positioned at (100, screen_height / 2)
flappy = Bird(100, int(screen_height / 2))
# Add the bird object to the bird group
bird_group.add(flappy)


###super important leaderboard function
def update_leaderboard(nickname, score, playtime):
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
                        leaderboard.append([nickname, score, best_score, playtime])
                        found = True
                    else:
                        leaderboard.append(row)
        else:
            print("Leaderboard file does not exist. It will be created.")

        if not found:
            leaderboard.append([nickname, score, score, playtime])

        game_scores.append(score)

        if len(game_scores) % 10 == 0:
            generate_report(game_scores)

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nickname', 'Last Score', 'Best Score', 'Playtime'])
            writer.writerows(leaderboard)
            print("Leaderboard updated.")
    except Exception as e:
        print(f"Error updating leaderboard: {e}")



def display_leaderboard():
    try:
        file_path = os.path.join(os.getcwd(), 'leaderboard.csv')
        if not os.path.isfile(file_path):
            print("No leaderboard data found")
            return

        screen.fill((0, 0, 0))
        draw_text('LEADER BOARD', large_font, (255, 255, 255), screen, 150, 50)

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            print(f"Header: {header}")
            y_offset = 150
            for row in reader:
                print(f"Row: {row}")
                draw_text(f"{row[0]}: Last Score - {row[1]}, Best Score - {row[2]}, Playtime - {row[3]} seconds", small_font, (255, 255, 255), screen, 50,
                          y_offset)
                y_offset += 40

        pygame.display.update()
        pygame.time.wait(5000)
    except Exception as e:
        print(f"Error displaying leaderboard: {e}")

def generate_report(scores):
    total_games = len(scores)
    if total_games == 0:
        return
    
    average_score = sum(scores) / total_games
    max_score = max(scores)
    min_score = min(scores)

    print(f"Total games played: {total_games}")
    print(f"Average score: {average_score}")
    print(f"Maximum score: {max_score}")
    print(f"Minimum score: {min_score}")


def main_menu():
    menu = True
    button_down = None
    while menu:
        screen.blit(main_menu_img, (0, 0))
        draw_text("MAIN MENU", pygame.font.Font(my_font, 65), (255, 255, 255), screen, 130, 100)

        # buttons
        button_width = 250
        button_height = 50
        button_x = (screen_width - button_width) // 2

        play_button = pygame.Rect(button_x, 200, button_width, button_height)
        skin_button = pygame.Rect(button_x, 300, button_width, button_height)
        leader_board_button = pygame.Rect(button_x, 400, button_width, button_height)
        exit_button = pygame.Rect(button_x, 500, button_width, button_height)

        # buttons view
        if button_down == play_button:
            pygame.draw.rect(screen, (37, 176, 54), play_button)
        else:
            pygame.draw.rect(screen, (57, 196, 74), play_button)

        if button_down == skin_button:
            draw_gradient_rect(screen, skin_button, (0, 0, 200), (0, 200, 0))
        else:
            draw_gradient_rect(screen, skin_button, color_start, color_end)

        if button_down == leader_board_button:
            pygame.draw.rect(screen, (204, 133, 25), leader_board_button)
        else:
            pygame.draw.rect(screen, (224, 153, 45), leader_board_button)

        if button_down == exit_button:
            pygame.draw.rect(screen, (235, 5, 0), exit_button)
        else:
            pygame.draw.rect(screen, (255, 25, 0), exit_button)

        # draw font
        font = pygame.font.Font(my_font, 30)

        draw_text("PLAY", font, (255, 255, 255), screen, play_button.x + 95, play_button.y + 10)
        draw_text("SKINS", font, (255, 255, 255), screen, skin_button.x + 85, skin_button.y + 10)
        draw_text("LEADER BOARD", font, (255, 255, 255), screen, leader_board_button.x + 27, leader_board_button.y + 10)
        draw_text("EXIT", font, (255, 255, 255), screen, exit_button.x + 95, exit_button.y + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    button_down = play_button
                if exit_button.collidepoint(event.pos):
                    button_down = exit_button
                if leader_board_button.collidepoint(event.pos):
                    button_down = leader_board_button
                if skin_button.collidepoint(event.pos):
                    button_down = skin_button
            if event.type == pygame.MOUSEBUTTONUP:
                if button_down == play_button and play_button.collidepoint(event.pos):
                    menu = False
                if button_down == exit_button and exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if button_down == leader_board_button and leader_board_button.collidepoint(event.pos):
                    display_leaderboard()
                if button_down == skin_button and skin_button.collidepoint(event.pos):
                    print("SKINS ARE COMING SOON")
                button_down = None

        pygame.display.update()

def draw_gradient_rect(screen, rect, color_start, color_end):
    x, y, w, h = rect
    for i in range(h):
        r = color_start[0] + (color_end[0] - color_start[0]) * i // h
        g = color_start[1] + (color_end[1] - color_start[1]) * i // h
        b = color_start[2] + (color_end[2] - color_start[2]) * i // h
        pygame.draw.line(screen, (r, g, b), (x, y + i), (x + w, y + i))


# main menu startup
main_menu()

# Create a transparent overlay surface
overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 128))


def restart_game():
    restart = True
    button_down = None
    button_width = 200
    button_height = 70
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2
    restart_game_button = pygame.Rect(button_x, button_y, button_width, button_height)

    while restart:
        screen.blit(bg, (0, 0))
        draw_text("Game Over", large_font, (255, 255, 255), screen, button_x, 100)

        if button_down == restart_game_button:
            pygame.draw.rect(screen, (37, 176, 54), restart_game_button)
        else:
            pygame.draw.rect(screen, (57, 196, 74), restart_game_button)

        draw_text("RESTART", font, (255, 255, 255), screen, restart_game_button.x + 40, restart_game_button.y + 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_game_button.collidepoint(event.pos):
                    button_down = restart_game_button
            if event.type == pygame.MOUSEBUTTONUP:
                if button_down == restart_game_button and restart_game_button.collidepoint(event.pos):
                    restart = False
                    return True
                button_down = None

        pygame.display.update()
        pygame.time.wait(100)

    return False


def reset_game():
    global flappy, scroll_speed, score, game_over, flying, pass_pipe, last_pipe
    bird_group.empty()
    pipe_group.empty()
    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy)
    scroll_speed = 4
    score = 0
    game_over = False
    flying = False
    pass_pipe = False
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    set_difficulty_params(difficulty)
    main_menu()


top_border = 0
run = True
# Game loop
while run:
    clock.tick(fps)

    # Background & base
    screen.blit(bg, (0, 0))
    screen.blit(base, (base_scroll, 750))

    if not game_over and flying:
        # Generating new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        base_scroll -= scroll_speed

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    # Checking the score
    if len(pipe_group) > 0:
        bird = bird_group.sprites()[0]
        first_pipe = pipe_group.sprites()[0]
        if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird.rect.left > first_pipe.rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), pygame.font.Font(my_font, 70), (255, 255, 255), screen, int(285), 60)

    # Collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.bottom >= 750:
        scroll_speed = 0
        game_over = True
        end_time = pygame.time.get_ticks()
        playtime = (end_time - start_time) / 1000  # Calculate playtime in seconds
        update_leaderboard(nickname, score, playtime)
        if restart_game():
            reset_game()

    for i in range(len(base_positions)):
        base_positions[i] -= scroll_speed

    # Draw base images
    for pos in base_positions:
        screen.blit(base, (pos, 750))

    # Add new base image if the first one is out of screen
    if base_positions[0] <= -base_width:
        base_positions.append(base_positions[-1] + base_width)
        base_positions.pop(0)

    # Draw nickname
    draw_text(f"player: {nickname}", font, (255, 255, 255), screen, 10, 10)

    # Generate insights every report_interval games
    if len(game_scores) % report_interval == 0:
        generate_report(game_scores)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
        if event.type == KEYDOWN and event.key == pygame.K_SPACE and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()



