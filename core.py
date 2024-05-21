import pygame
import csv
from csv import *
import os
import random
import Worker
import Groups
from Groups import *
from Worker import *
from pygame import *
from pygame.sprite import Group
from pygame.locals import *
#pygame initialize
pygame.init()

pygame.display.set_caption(gameTitle)
pygame.display.set_icon(icon)

bg = pygame.image.load(background)
base = pygame.image.load(ground)
base_width = base.get_width()
base_positions = [0, base_width]
#game variables

pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency

#Load front
font = pygame.font.Font(my_font, 30)
large_font = pygame.font.Font(my_font, 40)


#font function
def draw_text(text,font, color, surface, x,y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(0, 3):
            img = pygame.image.load(f'sprites/bluebird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    def update(self): #physics

        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 750:
                self.rect.y += int(self.vel)
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0

        #jump physics
        if game_over == False:
            keys = pygame.key.get_pressed()

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10

            if keys[pygame.K_SPACE] and not self.clicked:
                self.clicked = True
                self.vel = -10

            if not any(pygame.mouse.get_pressed()) and not keys[pygame.K_SPACE]:
                self.clicked = False

            if self.rect.bottom <= 0:
                self.rect.y += int(self.vel)
            #animations
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -60)


#pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(pipes_sprite)
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y +int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

def measure_text_width(text, font):
    textobj = font.render(text, True, (0, 0, 0))
    return textobj.get_width()

def nickname_input():
    input_active = True
    nickname = ""
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    nickname += event.unicode
        screen.fill((0, 0, 0))
        draw_text('Enter your nickname:', font, (255, 255, 255), screen, 150, 350)
        nickname_width = measure_text_width(nickname, large_font)
        draw_text(nickname, large_font,  (255, 255, 255),screen, 300 -nickname_width / 2, 400)
        pygame.display.update()

    return nickname
nickname = nickname_input()
print(f"Nickname: {nickname}")

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)


###super important leaderboard function
def update_leaderboard(nickname, score):
    file_exist = os.path.isfile('leaderboard.csv')
    leadeboard = []
    found = False

    if file_exist:
        with open('leaderboard.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nickname:
                    last_score = int(row[1])
                    best_score = int(row[2])
                    if score > best_score:
                        best_score = score
                    leadeboard.append([nickname, score, best_score])
                    found = True
                else:
                    leadeboard.append(row)
    if not found:
        leadeboard.append([nickname, score, score])
    with open('leaderboard.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(leadeboard)
def display_leaderboard():
    if not os.path.isfile('leaderboard.csv'):
        print("No leaderboard data found")
        return

    screen.fill((0, 0, 0))
    draw_text('LEADER BOARD', large_font, (255, 255, 255), screen, 150,50)

    with open('leaderboard.csv', mode='r') as file:
        reader = csv.reader(file)
        y_offset = 150
        for row in reader:
            draw_text(f"{row[0]}: Last Score - {row[1]}, Best Score - {row[2]}", font, (255, 255, 255), screen, 100, y_offset)
            y_offset += 40

    pygame.display.update()
    pygame.time.wait(5000)

#making gradient
def draw_gradient_rect(screen, rect, color_start, color_end):
    """Draw a vertical gradient rectangle."""
    x, y, w, h = rect
    for i in range(h):
        # Calculate the color for each row
        r = color_start[0] + (color_end[0] - color_start[0]) * i // h
        g = color_start[1] + (color_end[1] - color_start[1]) * i // h
        b = color_start[2] + (color_end[2] - color_start[2]) * i // h
        pygame.draw.line(screen, (r, g, b), (x, y + i), (x + w, y + i))
def main_menu():
    menu = True
    button_down = None
    while menu:
        screen.blit(main_menu_img, (0, 0))
        draw_text("MAIN MENU", pygame.font.Font(my_font, 65), (255, 255, 255), screen, 130, 100)

        # buttons
        button_width = 250
        button_height = 50
        screen_width = 600
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

#main menu startup
main_menu()

top_border = 0
run = True
while run:

    clock.tick(fps)

    #background & base
    screen.blit(bg, (0,0))
    screen.blit(base, (base_scroll, 750))

    if game_over == False and flying == True:

        #generating new pipes
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
    # checking the score
    if len(pipe_group) > 0:
        bird = bird_group.sprites()[0]
        first_pipe = pipe_group.sprites()[0]
        if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird.rect.left > first_pipe.rect.right:
                score += 1
                pass_pipe = False

    #print(score)
    #print(base_width)
    draw_text(str(score), (pygame.font.Font(my_font, 70)), (255, 255, 255), screen, int(285), 60)

    #collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        scroll_speed = 0
        game_over = True
    #cheking for game_over
    if flappy.rect.bottom >= 750:
        game_over = True
        flying = False
    for i in range(len(base_positions)):
        base_positions[i] -= scroll_speed

    # Draw base images
    for pos in base_positions:
        screen.blit(base, (pos, 750))

    # Add new base image if the first one is out of screen
    if base_positions[0] <= -base_width:
        base_positions.append(base_positions[-1] + base_width)
        base_positions.pop(0)

    #draw nickname
    draw_text(nickname, (font), (255, 255, 255), screen, 10, 10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()



