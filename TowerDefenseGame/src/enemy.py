import json

import pygame
import copy
import game_settings

# The enemy class will represent our lane runners
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        ## Enemy Animation setup
        self.frames = self.load_frames("images/sprites/TNT_Red.png", "images/sprites/TNT_Red.json")
        self.frames = self.frames[:-6]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        ## Animation Control
        self.counter = 0
        self.animation_speed = 0.2  # Lower = faster
        self.facing_right = True

        # Waypoints
        self.waypoints = copy.deepcopy(level.enemy_waypoints)
        self.current_waypoint = 0

        # Position and speed
        self.position = self.waypoints[self.current_waypoint]
        self.speed = 120 # This is pixels per second

        self.max_hp = 3
        self.hp = 3
#        self.update_color()

        # Money given for defeating the enemy
        self.bounty = 3
        game_settings.tick_of_last_enemy_spawn = pygame.time.get_ticks()


    def update(self):
        self.update_position()

        ## Animate
        self.counter += self.animation_speed
        if self.counter >= 1:
            self.counter = 0
            self.index = (self.index + 1) % len(self.frames)

        frame = self.frames[self.index]

        ## Determine direction toward the next waypoint
        if self.current_waypoint + 1 < len(self.waypoints):
            next_wp = self.waypoints[self.current_waypoint + 1]
            dx = next_wp.x - self.position.x

            if dx < -1:
                self.facing_right = False
            elif dx > 1:
                self.facing_right = True

        ## Flip the image if needed
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame
        self.rect.center = (self.position.x, self.position.y)

    ## Grab the frames from the data sheets
    def load_frames(self, sprite_sheet_path, json_path):
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        with open(json_path) as f:
            data = json.load(f)

        frames = []
        for frame_name in data["frames"]:
            frame = data["frames"][frame_name]["frame"]
            rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
            image = sheet.subsurface(rect)
            frames.append(image)
        return frames

    def update_position(self):
        if len(self.waypoints) - 1 > self.current_waypoint:
            self.position.move_towards_ip(self.waypoints[self.current_waypoint + 1], self.speed * game_settings.dt)
            if self.position == self.waypoints[self.current_waypoint + 1]:
                self.current_waypoint += 1
        else:
            ## If the enemy makes it to the end of the level, decrement the player life
            game_settings.player_lives -= 1
            self.kill()