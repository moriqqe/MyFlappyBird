import pygame
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

def main_menu():
    menu = True
    while menu:
        screen.fill((0,0,0))
        draw_text("MAIN MENU", pygame.font.Font(my_font, 65), (255, 255, 255), screen, 130, 100)
        #buttons
        play_button = pygame.Rect(300,200,200,50)
        leader_board_button = pygame.Rect(300,300,200,50)
        exit_button = pygame.Rect(300, 400, 200, 50)

        #visualise buttons
        pygame.draw.rect(screen, (255, 0, 0), play_button)
        pygame.draw.rect(screen, (0, 255, 0 ), leader_board_button)
        pygame.draw.rect(screen,(0, 0, 255), exit_button)

        #Draw button text
        draw_text("PLAY", font, (255,255,255), screen, play_button.x -40, play_button.y + 10)
        draw_text("LEADER BOARD", font, (255, 255, 255), screen, leader_board_button.x + -110, leader_board_button.y + 10)
        draw_text("EXIT", font, (255, 255, 255), screen, exit_button.x + -35, exit_button.y + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu = False
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                if leader_board_button.collidepoint(event.pos):
                    print("LEADER BOARD")
        pygame.display.update()
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

    print(score)
    draw_text(str(score), (pygame.font.Font(my_font, 70)), (255, 255, 255), screen, int(285), 60)

    #collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        scroll_speed = 0
        game_over = True
    #cheking for game_over
    if flappy.rect.bottom >= 750:
        game_over = True
        flying = False
    if abs(base_scroll) > 300:
        base_scroll = 0

    #draw nickname
    draw_text(nickname, (font), (255, 255, 255), screen, 10, 10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()



