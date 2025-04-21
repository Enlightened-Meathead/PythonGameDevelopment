import random

import pygame
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
        self.actions["attack_1"] = CharacterAction("attack_1", self.animations["attack_1"], 200, False)
        self.actions["attack_3"] = CharacterAction("attack_3", self.animations["attack_3"], 100, False)
        self.image = self.animations["idle"].get_frame(0)
        self.rect = self.image.get_rect()

        # set the position
        self.position = pygame.Vector2(x,y + self.rect.height / 2)

        # set up the initial position
        self.rect.midbottom = (self.position.x, self.position.y)

        self.base_speed = 250
        self.speed = self.base_speed

    def update(self):
        self.update_user_velocity()

        if not self.is_in_action:
            if self.velocity.magnitude() != 0:
                self.image = self.animations["run"].run_animation(100, True)
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
                self.run_action(self.actions["attack_3"])
            ## Additional heavy attack
            if keys[pygame.K_h]:
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
                                                runners[rand_runner][2],
                                                128,
                                                128,
                                                )
        self.animations["run"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Run.png",
                                                runners[rand_runner][3],
                                                128,
                                                128,
                                                )
        self.animations["faint"] = SpriteSurface(f"images/sprites/{runners[rand_runner][0]}/Dead.png",
                                               runners[rand_runner][4],
                                               128,
                                               128,
                                               )
        self.actions["faint"] = CharacterAction("faint", self.animations["faint"], 350, True)

        # Image and rect
        self.image = self.animations["idle"].get_frame(0)
        self.rect = self.image.get_rect()

        self.position = pygame.Vector2(x,y + self.rect.height/2)
        self.rect.midbottom = self.position

        self.base_speed = 80
        self.speed = 80

        # Have a cooldown for running away from user and teleports
        self.run_cd = 1000
        self.tick_of_last_run = -1 * self.run_cd
        self.is_running = False
        self.teleport_cd = 0
        self.tick_of_last_teleport = 0

        self.threat_distance = 100
        self.is_idling = False

        ## For the duration of an action, use this flag so the score doesnt update every frame
        self.score_incremented = False

    def update(self, user_character):
        if not self.is_in_action:
            self.update_monster_velocity(user_character)
            self.update_position()

            self.monster_try_teleport()


            if self.is_running:
                self.image = self.animations["run"].run_animation(80, True)
                self.is_idling = False
            elif self.velocity.magnitude() !=0:
                self.image = self.animations["walk"].run_animation(80, True)
                self.is_idling = False
            else:
                self.image = self.animations["idle"].run_animation(80,True)
                if not self.is_idling:
                    game_settings.monsters_succeeded += 1
                self.is_idling = True

        else:
            for action in self.actions:
                if self.actions[action].is_active:
                    self.run_action(self.actions[action])
                    ## Increment score if the action results in a sprite being killed
                    if not self.score_incremented:
                        game_settings.score += 1
                    self.score_incremented = True


        if self.is_flipped:
            self.image = pygame.transform.flip(self.image, True, False)


        self.resize_rect()
        self.rect.midbottom = self.position

    # NPC logic here
    def update_monster_velocity(self, user_character):
        # NPC goal is to get to center and runs away from user. Teleport if they are at the edge of the map
        distance_to_user = pygame.Vector2(self.rect.center).distance_to(user_character.sprite.rect.center)
        vel_away_user = pygame.Vector2(self.rect.centerx - user_character.sprite.rect.centerx,
                                       user_character.sprite.rect.centery - self.rect.centery)

        distance_to_center = pygame.Vector2(self.rect.center).distance_to(self.surface.get_rect().center)
        vel_to_center = pygame.Vector2(self.surface.get_rect().centerx- self.rect.centerx,
                                       self.surface.get_rect().centery - self.rect.centery)

        is_player_too_close = distance_to_user <= distance_to_center or distance_to_user <= self.threat_distance
        off_run_cd = pygame.time.get_ticks() - self.tick_of_last_run >= self.run_cd

        if is_player_too_close and off_run_cd:
            self.velocity = vel_away_user
            self.speed = self.base_speed * 1.3
            self.tick_of_last_run = pygame.time.get_ticks()
            self.is_running = True
        elif self.is_running and not off_run_cd:
            self.velocity = vel_away_user
            self.speed = self.base_speed * 1.3
        else:
            if distance_to_center < 2:
                self.velocity = pygame.Vector2(0,0)
            else:
                self.velocity = vel_to_center
            self.speed = self.base_speed
            self.is_running = False

        if self.velocity.x < 0:
            self.is_flipped = True
        if self.velocity.x > 0:
            self.is_flipped = False

    # If runner is at the edge of the map teleport them to the other side:
    def monster_try_teleport(self):
        if self.velocity.magnitude() != 0:
            is_left = self.rect.left <= self.surface.get_rect().left
            is_right = self.rect.right >= self.surface.get_rect().right
            is_top = self.rect.top <= self.surface.get_rect().top
            is_bottom = self.rect.bottom >= self.surface.get_rect().bottom

            tp_off_cd = pygame.time.get_ticks() - self.tick_of_last_teleport > self.teleport_cd

            if is_left and tp_off_cd:
                if self.rect.right <= self.surface.get_rect().left:
                    self.position.x = self.surface.get_rect().right - int(self.rect.width/2)
                    self.tick_of_last_teleport = pygame.time.get_ticks()
                    self.is_running = False
                    self.tick_of_last_run -= self.run_cd
            elif is_left and not tp_off_cd:
                self.position.x = self.surface.get_rect().left + int(self.rect.width/2)
            if is_right and tp_off_cd:
                if self.rect.left >= self.surface.get_rect().right:
                    self.position.x = self.surface.get_rect().left + int(self.rect.width/2)
                    self.tick_of_last_teleport = pygame.time.get_ticks()
                    self.is_running = False
                    self.tick_of_last_run -= self.run_cd
            elif is_right and not tp_off_cd:
                self.position.x = self.surface.get_rect().right - int(self.rect.width/2)

            if is_top and tp_off_cd:
                if self.rect.bottom <= self.surface.get_rect().top:
                    self.position.y = self.surface.get_rect().bottom + int(self.rect.height)
                    self.tick_of_last_teleport = pygame.time.get_ticks()
                    self.is_running = False
                    self.tick_of_last_run -= self.run_cd
            elif is_top and not tp_off_cd:
                self.position.y = self.surface.get_rect().top - self.rect.height
            if is_bottom and tp_off_cd:
                if self.rect.top >= self.surface.get_rect().bottom:
                    self.position.y = self.surface.get_rect().top + int(self.rect.height)
                    self.tick_of_last_teleport = pygame.time.get_ticks()
                    self.is_running = False
                    self.tick_of_last_run -= self.run_cd
            elif is_top and not tp_off_cd:
                self.position.y = self.surface.get_rect().top
