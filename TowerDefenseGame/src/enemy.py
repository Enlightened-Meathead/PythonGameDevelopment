import pygame
import copy
import game_settings

# The enemy class will represent our lane runners
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)

        # Sprites need an image attribute
        self.image = pygame.Surface((16,16))

        # Sprites need a rect attribute
        self.rect = self.image.get_rect()

        # Waypoints
        self.waypoints = copy.deepcopy(level.enemy_waypoints)
        self.current_waypoint = 0

        # Position and speed
        self.position = self.waypoints[self.current_waypoint]
        self.speed = 100 # This is pixels per second

        self.max_hp = 3
        self.hp = 3
        self.update_color()

        # Money given for defeating the enemy
        self.bounty = 10
        game_settings.tick_of_last_enemy_spawn = pygame.time.get_ticks()

    # Runs every frame
    def update(self):
        self.update_position()
        self.rect.center = (self.position.x, self.position.y)
        pass

    def update_position(self):
        if len(self.waypoints) - 1 > self.current_waypoint:
            self.position.move_towards_ip(self.waypoints[self.current_waypoint + 1], self.speed * game_settings.dt)
            if self.position == self.waypoints[self.current_waypoint + 1]:
                self.current_waypoint += 1
        else:
            self.kill()

    def update_color(self):
        hp_percent = int(round((self.hp/self.max_hp),1) * 100 )
        self.image.fill(game_settings.hp_colors[hp_percent])







