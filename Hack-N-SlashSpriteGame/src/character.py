from random import random

import pygame
from pygame.sprite import Sprite
from surface_handler import SpriteSurface

import game_settings

# Class for character actions
class CharacterAction():
    def __init__(self, name, animation, frame_duration, kill = False):
        self.action_name = name
        self.animation = animation
        self.frame_duration = frame_duration
        self.tick_of_action_start = 0
        self.is_active = False
        self.kill = kill

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
        self.actions = {}
        self.is_flipped = False
        self.is_in_action = False


    # Run every game loop
    def update(self):
        pass

    # Use velocity to update position and rect attributes
    def update_position(self):
        if self.velocity.magnitude() != 0:
            # Normalize the velocity
            self.velocity = self.velocity.normalize()
            # Multiply our length by our characters speed and delta time
            self.velocity.scale_to_length(self.speed * game_settings.dt)
            # Add velocity to position
            self.position += self.velocity
    def run_action(self, action):
        if not self.is_in_action:
            self.is_in_action = True
            action.is_active = True
            action.tick_of_action_start = pygame.time.get_ticks()

        self.image = action.animation.run_animation(action.frame_duration, False)

        if pygame.time.get_ticks() - action.tick_of_action_start >= action.animation.num_of_frames * action.frame_duration:
            action.is_active = False
            self.is_in_action = False
            action.animation.current_frame = 0
            if action.kill:
                self.kill()

    def resize_rect(self):
        if self.rect.width != self.image.get_rect().width:
            self.rect.width = self.image.get_rect().width





class User(Character):
    def __init__(self, surface, x, y):
        Character.__init__(self, surface)
        self.animations["idle"] = SpriteSurface("images/sprites/samurai/Idle.png",
                                                6,
                                                128,
                                                128,
                                                )
        self.animations["walk"] = SpriteSurface("images/sprites/samurai/Walk.png",
                                                9,
                                                128,
                                                128)
        self.animations["run"] = SpriteSurface("images/sprites/samurai/Run.png",
                                                8,
                                                128,
                                                128)
        self.animations["attack_1"] = SpriteSurface("images/sprites/samurai/Attack_1.png",
                                                    4,
                                                    128,
                                                    128)
        self.animations["attack_2"] = SpriteSurface("images/sprites/samurai/Attack_2.png",
                                                    5,
                                                    128,
                                                    128)
        self.animations["attack_3"] = SpriteSurface("images/sprites/samurai/Attack_3.png",
                                                 4,
                                                 128,
                                                 128)
        # Set up character actions
        self.actions["attack_1"] = CharacterAction("attack_1", self.animations["attack_1"], 100, False)
        self.image = self.animations["idle"].get_frame(0)
        self.rect = self.image.get_rect()

        # set the position
        self.position = pygame.Vector2(x,y + self.rect.height / 2)

        # set up the initial position
        self.rect.midbottom = (self.position.x, self.position.y)

        self.base_speed = 200
        self.speed = self.base_speed

    def update(self):
        #self.image = self.animations["run"].run_animation(100, True)
        self.update_user_velocity()

        if not self.is_in_action:
            if self.velocity.magnitude() != 0:
                self.image = self.animations["walk"].run_animation(100, True)
            else:
                self.image = self.animations["idle"].run_animation(100, True)
        else:
            for action in self.actions:
                if self.actions[action].is_active:
                    self.run_action(self.actions[action])


        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        self.resize_rect()
        self.update_position()
        self.bind_position_to_surface()
        self.rect.midbottom = self.position

        #self.image.fill("#ffffff")

    def update_user_velocity(self):
        # Zero out the velocity, stops movement if keys arent pressed
        ## Can add acceleration friction here
        self.velocity = pygame.Vector2(0,0)

        if not (self.is_in_action):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.velocity.y -= 1
            if keys[pygame.K_d]:
                self.velocity.x += 1
                self.is_flipped = False
            if keys[pygame.K_s]:
                self.velocity.y += 1
            if keys[pygame.K_a]:
                self.velocity.x -= 1
                self.is_flipped = True
            if keys[pygame.K_SPACE]:
                self.run_action(self.actions["attack_1"])
    def bind_position_to_surface(self):
        if self.position.x - self.rect.width/2 < self.surface.get_rect().left:
            self.position.x = self.surface.get_rect().left + self.rect.width/2
        elif self.position.x + self.rect.width/2 > self.surface.get_rect().right:
            self.position.x = self.surface.get_rect().right - self.rect.width/2

        if self.position.y - self.rect.height < self.surface.get_rect().top:
            self.position.y = self.surface.get_rect().top + self.rect.height
        elif self.position.y > self.surface.get_rect().bottom:
            self.position.y = self.surface.get_rect().bottom

runners = {}
runners[1] = (
    "werewolf",
    8, # Frames in idle animation
    11, # Frames in walk animation
    9, # Frames in run animation
    2 # Frames for death animation
)
runners[2] = ("gorgon", 7, 13, 7, 3)

class Monster(Character):
    def __init__(self, surface, x, y):
        Character.__init__(self, surface)
        rand_runner = random.randint(1,2)
        self.animations["idle"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Idle.png",
                                                runners[rand_runner][1],
                                                128,
                                                128,
                                                )
        self.animations["walk"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Walk.png",
                                                runners[rand_runner][1],
                                                128,
                                                128,
                                                )
        self.animations["run"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Run.png",
                                                runners[rand_runner][1],
                                                128,
                                                128,
                                                )
        self.animations["faint"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Dead.png",
                                               runners[rand_runner][1],
                                               128,
                                               128,
                                               )
        self.actions["faint"] = CharacterAction("faint", self.animations["faint"], 100, True)

        # Image and rect
        self.image = self.animations["idle"].get_frame(0)
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(x,y + self.rect.height/2)
        self.rect.midbottom = self.position

        self.base_speed = 100
        self.speed = 100

        self.threat_distance = 150

    def update(self):
        pass

    # NPC logic here
    def update_monster_velocity(self):
        pass



