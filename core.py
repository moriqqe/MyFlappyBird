import pygame
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

#Load front
font = pygame.font.Font(my_font, 17)


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
        # gravity

        if flying == True:

            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 450:
                self.rect.y += int(self.vel)
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0

            # jump physics
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
            # animations
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -60)


#pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/pipe-green.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

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
        draw_text('Enter your nickname:', font, (255, 255, 255), screen, 50, 200)
        draw_text(nickname, font, (255, 255, 255),screen, 50, 250)
        pygame.display.update()

    return nickname
nickname = nickname_input()
print(f"Nickname: {nickname}")


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()



flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

top_border = 0
run = True
while run:

    clock.tick(fps)

    #background & base
    screen.blit(bg, (0,0))
    screen.blit(base, (base_scroll, 450))

    if game_over == False:
        base_scroll -= scroll_speed

    bird_group.draw(screen)
    bird_group.update()

    #cheking for game_over
    if flappy.rect.bottom > 450:
        game_over = True
        flying = False
    if abs(base_scroll) > 50:
        base_scroll = 0

    #draw nickname
    draw_text(nickname, font, (255, 255, 255), screen, 10, 10)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()



