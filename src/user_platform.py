import pygame
import game_settings

class UserPlatform(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface

        # Every sprite needs an image and a rect attribute
        self.image = pygame.Surface((250, 25))
        self.image.fill("#DDDDDD")
        self.rect = self.image.get_rect()

        # Create a mask
        self.mask = pygame.mask.from_surface(self.image)

        # Create vectors
        self.position = pygame.Vector2(surface.get_width() / 2, surface.get_height() - 40)
        self.velocity = pygame.Vector2(0,0)

        # Speed variable
        self.max_speed = 500
        self.base_speed = 100
        self.speed = 0
        self.acceleration = .2
        self.friction = .3
        self.changing_direction = False

        # Update the rect to be the position
        self.rect.center = self.position

    #Update method fires every time the game loops
    def update(self):
        self.update_velocity()
        self.update_position()

        self.rect.center = self.position

    # Calculate new vector position
    def update_position(self):
        self.position += self.velocity

        if self.rect.left <= self.surface.get_rect().left and not self.velocity.x > 0:
            self.position.x = self.surface.get_rect().left + self.rect.width / 2
            self.velocity.x = 0
            self.speed = 0
        if self.rect.right >= self.surface.get_rect().right and not self.velocity.x < 0:
            self.position.x = self.surface.get_rect().right - self.rect.width / 2
            self.velocity.x = 0
            self.speed = 0




    # Calculate the velocity from the user input
    def update_velocity(self):
        key_presses = pygame.key.get_pressed()
        key_pressed = False
        left = self.velocity.x < 0
        right = self.velocity.x > 0

        if key_presses[pygame.K_a]:
            self.velocity.x -= 1
            key_pressed = True
            if right:
                self.changing_direction = True
        if key_presses[pygame.K_d]:
            self.velocity.x += 1
            key_pressed = True
            if left:
                self.changing_direction = True


        if self.velocity.magnitude() !=0:

            self.velocity = self.velocity.normalize()

            if key_pressed and not self.changing_direction:
                self.speed += self.base_speed * self.acceleration
            elif not key_pressed or self.changing_direction:
                self.speed -= self.base_speed * self.friction

            if self.speed <= 0:
                self.changing_direction = False
                self.speed = 0
            elif self.speed >= self.max_speed:
                self.speed = self.max_speed

            self.velocity.scale_to_length(self.speed * game_settings.dt)