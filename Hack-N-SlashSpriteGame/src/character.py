import pygame
from pygame.sprite import Sprite
from surface_handler import SpriteSurface

import game_settings

# Parent character class for other characters

class Character(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface

        # Image and rect
        self.image = None
        self.rect = None

        self.position = pygame.Vector2(0,0)
        self.velocity = pygame.Vector2(0,0)
        self.base_speed = 0
        self.speed = 0

        # Attributes for sprite animations
        self.animations = {}
        self.is_flipped = False


    # Run every game loop
    def update(self):
        pass

    # Use velocity to update position and rect attributes
    def update_position(self):
        pass




class User(Character):
    def __init__(self, surface, x, y):
        Character.__init__(self, surface)
        self.animations["idle"] = SpriteSurface("images/sprites/samurai/Idle.png",
                                                5,
                                                128,
                                                128,
                                                scale=1.25,
                                                crop_top=50,
                                                crop_left=40,
                                                crop_right=40)
        self.image = self.animations["idle"].get_frame(0)
        self.rect = self.image.get_rect()

        # set the position
        self.position = pygame.Vector2(x,y)

        # set up the initial position
        self.rect.midbottom = (self.position.x, self.position.y)

        self.base_speed = 250
        self.speed = self.base_speed



class Monster(Character):
    def __init__(self, surface):
        Character.__init__(self, surface)

