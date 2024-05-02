import pygame
from pygame import *

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 288
screen_height = 512

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Flappy Bird")
icon = pygame.image.load('Icon.ico')
pygame.display.set_icon(icon)


#using sprites
bg = pygame.image.load('sprites/background-day.png')
base = pygame.image.load('sprites/base.png')

#adding scroll script
base_scroll = 0
scroll_speed = 8

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

    def update(self):  #making animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0

        self.image = self.images[self.index]




bird_group = pygame.sprite.Group()

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



