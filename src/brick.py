import pygame
import game_settings

class Brick(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, hp, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


        # HP
        self.max_hp = hp
        self.hp = hp

        self.rect.topleft = (x, y)


        # Update the color
        self.update_color()

    def update_color(self):
        percent = int(round((self.hp / self.max_hp),1)*100)
        self.image.fill(game_settings.hp_colors[percent])

    def update(self):
        pass

    def brick_hit(self, ball):
        collision = pygame.sprite.collide_mask(self, ball)
        if collision:
            self.hp -= ball.damage
            if self.hp <= 0:
                self.kill()
            else:
                self.update_color()


