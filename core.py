import pygame
import Worker
import Groups
from Groups import *
from Worker import *
from pygame import *
from pygame.sprite import Group

# pygame initialize
pygame.init()

pygame.display.set_caption(gameTitle)
pygame.display.set_icon(icon)

bg = pygame.image.load(background)
base = pygame.image.load(ground)

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
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 450:
            self.rect.y += int(self.vel)

        #jump physics
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN and not self.clicked:
                self.clicked = True
                self.vel = -10


        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if keys[pygame.K_SPACE] and self.clicked == False:
            self.clicked = True
            self.vel = -10

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

#pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/pipe-green.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)


run = True
while run:

    clock.tick(fps)

    #background & base
    screen.blit(bg, (0,0))

    screen.blit(base, (base_scroll, 450))
    base_scroll -= scroll_speed

    bird_group.draw(screen)
    bird_group.update()

    if abs(base_scroll) > 50:
        base_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()



