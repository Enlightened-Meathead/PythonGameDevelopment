import json

import pygame
import game_settings
from spritegroups import enemies, projectiles

class Tower(pygame.sprite.Sprite):
    def __init__(self, cell):
        pygame.sprite.Sprite.__init__(self)
       # Image and rect
        ## Tower Animation setup
        self.frames = self.load_frames("images/sprites/Archer_Blue.png", "images/sprites/Archer_Blue.json")
        ## get rid of the last two frames because they are just arrows
        self.frames = self.frames[:-2]
        self.index = 0
        self.image = self.frames[self.index]
        # Get the position of the tile center
        tile_x = cell[0] * game_settings.COL_SIZE + game_settings.COL_SIZE // 2
        tile_y = cell[1] * game_settings.ROW_SIZE + game_settings.ROW_SIZE // 2
        ## Animation timing
        self.counter = 0
        self.animation_speed = 0.2

        # Center the sprite on the tile
        self.rect = self.image.get_rect(center=(tile_x, tile_y))

        # Position vector for projectiles
        self.position = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.range = 150
        self.fire_rate = 500
        self.tick_of_last_shot = 0
        self.cost = 50
        self.is_firing = False


    ## Load the frames for the tower animation
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

    def update(self):
        # Firing logic
        if pygame.time.get_ticks() - self.tick_of_last_shot >= self.fire_rate:
            self.fire_at_closest_target()
            self.is_firing = True
        else:
            self.is_firing = False

        ## Animate tower if its firing
        if not self.is_firing:
            self.counter += self.animation_speed
            if self.counter >= 1:
                self.index = (self.index + 1) % len(self.frames)
                self.image = self.frames[self.index]
                self.counter = 0

    def fire_at_closest_target(self):
        if len(enemies) > 0:
            enemy_sprites = enemies.sprites()
            closest_enemy = enemy_sprites[0]
            closest_enemy_distance = self.position.distance_to(closest_enemy.position)

            for enemy in enemy_sprites:
                enemy_distance = self.position.distance_to(enemy.position)
                if enemy_distance < closest_enemy_distance:
                    closest_enemy = enemy
                    closest_enemy_distance = enemy_distance

            if closest_enemy_distance <= self.range:
                self.tick_of_last_shot = pygame.time.get_ticks()
                projectiles.add(Projectile(self, closest_enemy))




class Projectile(pygame.sprite.Sprite):
    def __init__(self, tower, target):
        pygame.sprite.Sprite.__init__(self)

        # Image and rect
        self.image = pygame.Surface((10,10))
        self.image.fill("#DDDDDD")
        self.rect = self.image.get_rect()

        self.tower = tower
        self.target = target

        self.base_speed = 400
        self.speed = 400

        # Keep track of moving parts
        self.position = pygame.Vector2(tower.rect.center)
        self.velocity = target.position - self.position
        self.velocity = self.velocity.normalize()
        self.velocity.scale_to_length(self.speed)

        # Keep track of projectile lifespan
        self.time_to_live = 500
        self.tick_of_fired = pygame.time.get_ticks()
        self.damage = 1

    def update(self):
        self.update_position()
        self.rect.center = (self.position.x, self.position.y)

    def update_position(self):
        if pygame.time.get_ticks() - self.tick_of_fired < self.time_to_live:
            self.position += self.velocity * game_settings.dt
        else:
            self.kill()

