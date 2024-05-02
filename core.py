import pygame
from pygame import *

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 288
screen_height = 512

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Flappy Bird")

#using sprites

bg = pygame.image.load('sprites/background-day.png')
base = pygame.image.load('sprites/base.png')

#adding scroll script

base_scroll = 0
scroll_speed = 4

run = True
while run:

    clock.tick(fps)

    #background & base
    screen.blit(bg, (0,0))

    screen.blit(base, (base_scroll, 450))
    base_scroll -= scroll_speed
    if abs(base_scroll) > 50:
        base_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()



