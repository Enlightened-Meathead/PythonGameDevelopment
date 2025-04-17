import pygame
import game_settings
from spritegroups import enemies, projectiles

class Tower(pygame.sprite.Sprite):
    def __init__(self, cell):
        pygame.sprite.Sprite.__init__(self)
       # Image and rect
        ## Can make a tower image here and load that instead
        self.image = pygame.Surface((game_settings.COL_SIZE, game_settings.ROW_SIZE))
        self.image.fill("#AAAAAA")
        self.rect = self.image.get_rect()

        # Position the tower in the correct cell
        self.rect.topleft = (cell[0] * game_settings.COL_SIZE, cell[1] * game_settings.ROW_SIZE)

        # Position vector for projectiles
        self.position = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.range = 150
        self.fire_rate = 500
        self.tick_of_last_shot = 0
        self.cost = 50

    def update(self):
        if pygame.time.get_ticks() - self.tick_of_last_shot >= self.fire_rate:
            self.fire_at_closest_target()
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

