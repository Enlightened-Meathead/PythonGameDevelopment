import math
import random
import pygame
pygame.font.init()
# Set Text font on screen
font = pygame.font.SysFont(None, 48)
lives_font = pygame.font.SysFont(None, 24)

import game_settings

class Ball(pygame.sprite.Sprite):
    def __init__(self, surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game_started = False
        ## Number of lives for the game
        self.lives = game_settings.lives

        self.surface = surface
        self.radius = 10

        # Sprites need an image and rect !
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        circle = pygame.draw.circle(self.image, "#DDDDDD", (self.radius, self.radius), self.radius)
        self.rect = circle

        # Create a mask
        self.mask = pygame.mask.from_surface(self.image)


        # Create our vectors
        self.start_x = x
        self.start_y = y
        self.position = pygame.Vector2(self.start_x,self.start_y)
        self.velocity = pygame.Vector2(0,0)

        # Set up our speed variables
        self.max_speed = 800
        self.min_speed = 200
        self.speed = 500
        self.angle = 0

        # Damage to the bricks
        self.damage = 1

        # Center the rect on the position
        self.rect.center = self.position

    # Run this every frame
    def update(self):
        self.update_velocity()
        self.update_position()
        self.print_lives()

        self.rect.center = self.position


    # Run every update
    def update_position(self):
        # Bouncing off the sides
        if self.rect.left <= self.surface.get_rect().left or self.rect.right >= self.surface.get_rect().right:
            self.velocity.reflect_ip((self.velocity.x * -1, 0))
            # Safety to make ball not get stuck
            if self.rect.left <= self.surface.get_rect().left:
                self.position.x = self.surface.get_rect().left + self.rect.width / 2 + 1
            if self.rect.right >= self.surface.get_rect().right:
                self.position.x = self.surface.get_rect().right - self.rect.width / 2 - 1

        # Bouncing off the top and bottom
        if self.rect.top <= self.surface.get_rect().top:
            self.velocity.reflect_ip((0, self.velocity.y * -1))
            # Safety to make ball not get stuck
            if self.rect.top <= self.surface.get_rect().top:
                self.position.y = self.surface.get_rect().top + self.rect.height / 2 + 1

        # Lower play lives if ball goes off bottom and end the game if player is out of lives
        if self.rect.top >= self.surface.get_rect().bottom:
            ## If the ball goes under, decrement the lives
            self.lives -= 1
            self.game_started = False
            self.listen_to_start()
            self.position = pygame.Vector2(self.start_x, self.start_y)
            self.velocity = pygame.Vector2(0, 0)
            # If out of lives, end the game
            if self.lives == 0:
                self.kill()

        self.position += self.velocity

    def update_velocity(self):
        if self.velocity.magnitude() !=0:
            self.velocity = self.velocity.normalize()
            self.velocity.scale_to_length(self.speed * game_settings.dt)
        else:
            self.listen_to_start()

    def listen_to_start(self):
        keys = pygame.key.get_pressed()
        ## Start font (2.5 Points)
        if not self.game_started:
            text = font.render("Press SPACE to Start!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 1.5))
            self.surface.blit(text, text_rect)
        if keys[pygame.K_SPACE]:
            self.game_started = True
            ## Randomized ball start (5 points)
            random_angle = random.randint(10,80)
            radians = math.radians(random_angle)
            self.velocity.x = math.cos(radians)
            self.velocity.y = math.sin(radians)
            self.angle = random_angle

    def platform_hit(self, platform):
        # Do a more accurate check for collision
        collison = pygame.sprite.collide_mask(self, platform)
        if collison:
            self.velocity.reflect_ip((0, self.velocity.y * -1))
            # Add a safety to make sure ball doesn't go through platform
            if self.rect.centery - self.radius <= platform.rect.top:
                self.rect.centery = platform.rect.top - self.radius - 1
                self.position.y = platform.rect.top - self.radius - 1

            # Faking physics for sake of the game :P
            # If the platform and balling moving in the same direction, angle the ball down, speed it up
            # If the platform and ball are moving in opposite directions, angle the ball up, slow it down

            if platform.velocity.x != 0:
                previous_angle = self.angle
                new_angle = self.angle

                # Max angle the ball can change in a bounce
                MAX_ANGLE_CHANGE = 15
                # Max speed applied to a bounce
                MAX_SPEED_CHANGE = 50
                # Highest and lowest angles we want
                HIGHEST_ANGLE = 80
                LOWEST_ANGLE = 30

                platform_speed = platform.speed / platform.max_speed

                bounce_angle = int(platform_speed * MAX_ANGLE_CHANGE)
                speed_change = int(platform_speed * MAX_SPEED_CHANGE)

                # Both moving in the same direction
                if (platform.velocity.x > 0 and self.velocity.x > 0) or (platform.velocity.x < 0 and self.velocity.x < 0):
                    if HIGHEST_ANGLE >= self.angle - bounce_angle >= LOWEST_ANGLE:
                        new_angle -=bounce_angle
                    elif self.angle - bounce_angle < LOWEST_ANGLE:
                        angle_to_lowest = LOWEST_ANGLE - (self.angle - bounce_angle)
                        new_angle -= bounce_angle - angle_to_lowest

                    if self.speed + speed_change <= self.max_speed:
                        self.speed += speed_change
                    else:
                        self.speed = self.max_speed

                # Ball and platform moving in opposite direction
                if (platform.velocity.x > 0 and self.velocity.x < 0) or (platform.velocity.x < 0 and self.velocity.x >0):
                    if HIGHEST_ANGLE >= self.angle + bounce_angle >= LOWEST_ANGLE:
                        new_angle += bounce_angle
                    elif self.angle + bounce_angle > HIGHEST_ANGLE:
                        angle_to_highest = (self.angle + bounce_angle) - HIGHEST_ANGLE
                        new_angle += bounce_angle - angle_to_highest

                    if self.speed - speed_change >= self.min_speed:
                        self.speed -= speed_change
                    else:
                        self.speed = self.min_speed

                self.angle = new_angle
                rotation = previous_angle - new_angle
                if self.velocity.x < 0:
                    rotation *= -1
                self.velocity.rotate_ip(rotation)
    def brick_hit(self, brick):
        collision = pygame.sprite.collide_mask(self, brick)
        if collision:
            delta_x = 0
            delta_y = 0

            if self.velocity.x > 0:
                delta_x = self.rect.right - brick.rect.left
            elif self.velocity.x < 0:
                delta_x = brick.rect.right - self.rect.left

            if self.velocity.y > 0:
                delta_y = self.rect.bottom - brick.rect.top
            elif self.velocity.y > 0:
                delta_y = brick.rect.bottom -self.rect.top

            # Corner hits
            if abs(delta_x - delta_y) < 2:
                self.velocity.reflect_ip((self.velocity.x * -1, self.velocity.y * - 1))
            # Left or right hit
            elif delta_x > delta_y:
                self.velocity.reflect_ip((0, self.velocity.y * -1))
            # Top or bottom hit
            elif delta_x < delta_y:
                self.velocity.reflect_ip((self.velocity.x * -1, 0))
    ## Print the lives on the top left of the screen every frame (10 points)
    def print_lives(self):
        text = lives_font.render(f"Remaining Lives: {self.lives}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() // 9, self.surface.get_height() // 12))
        self.surface.blit(text, text_rect)


