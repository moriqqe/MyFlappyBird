import pygame
pygame.init()
#Title
gameTitle = "My Flappy Bird"

#ingame variables
fps = 60
screen_width = 288
screen_height = 512
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))

#scroll script
base_scroll = 0
scroll_speed = 4

flying = False
game_over = False

#Font
my_font = 'flappy-font.ttf'

#ingame sprites
ground = 'sprites/base.png'
background = 'sprites/background-day.png'


#icon
icon = pygame.image.load('icon.ico')