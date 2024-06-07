import pygame
import random
from pygame.sprite import Sprite

# Bird class for player's character
class Bird(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'sprites/bluebird{num}.png') for num in range(3)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False

    def update(self, flying, game_over):
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 750:
                self.rect.y += int(self.vel)
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0

        if not game_over:
            keys = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed and not self.clicked:
                self.clicked = True
                self.vel = -10
            if keys[pygame.K_SPACE] and not self.clicked:
                self.clicked = True
                self.vel = -10
            if not any(pygame.mouse.get_pressed()) and not keys[pygame.K_SPACE]:
                self.clicked = False

            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -60)

# Pipe class for obstacles
class Pipe(Sprite):
    def __init__(self, x, y, position, pipe_gap, pipes_sprite, scroll_speed):
        super().__init__()
        self.image = pygame.image.load(pipes_sprite)
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        else:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
