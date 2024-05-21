import pygame
pygame.init()
#Title
gameTitle = "My Flappy Bird"

#ingame variables
fps = 60
screen_width = 600
screen_height = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0


#scroll script
base_scroll = 0
scroll_speed = 4

flying = False
game_over = False
pass_pipe = False
#Font
my_font = 'flappy-font.ttf'

#ingame sprites
ground = 'Flappy Bird Assets/Tiles/Style 1/newground.png'
background = 'Flappy Bird Assets/Background/Background1.png'
pipes_sprite = 'Flappy Bird Assets/Tiles/Style 1/red_pipe.png'
main_menu_img = 'meme.png'

#icon
icon = pygame.image.load('icon.ico')