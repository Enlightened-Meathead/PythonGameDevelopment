import pygame
import game_settings
from user_platform import UserPlatform
from brick import Brick
from ball import Ball
from sprite_groups import user_sprite, ball_sprites, brick_sprites
pygame.init()
screen = pygame.display.set_mode((game_settings.GAME_WIDTH, game_settings.GAME_HEIGHT))
clock = pygame.time.Clock()

pygame.font.init()
# Set Text font on screen
font = pygame.font.SysFont(None, 48)
running = True

background = pygame.Surface((screen.get_width(), screen.get_height()))
#background = pygame.image.load()
background.fill("#353535")



user_sprite.add(UserPlatform(screen))
ball_sprites.add(Ball(screen, screen.get_width() / 2, screen.get_height() /2))

def add_bricks():
    brick_width = 100
    brick_height = 40
    brick_hp = 2
    brick_gutter = 20

    bricks_across = int(screen.get_rect().width // brick_width)
    bricks_stack = int((screen.get_rect().height / 3) // brick_height)

    current_x = screen.get_rect().left
    current_y = screen.get_rect().top + 60

    for row in range(bricks_stack):
        for col in range(bricks_across):
            brick_sprites.add(Brick(screen,
                                    current_x + brick_gutter /2,
                                    current_y + brick_gutter /2,
                                    brick_hp,
                                    brick_width - brick_gutter/2,
                                    brick_height - brick_gutter/2))
            current_x += brick_width
        current_x = screen.get_rect().left
        current_y += brick_height

add_bricks()

def platform_bounce(platform, ball):
    collision = pygame.sprite.collide_rect(platform, ball)
    if collision:
        ball.platform_hit(platform)
        return True
    return False

def brick_hit(brick, ball):
    collision = pygame.sprite.collide_rect(brick, ball)
    if collision:
        brick.brick_hit(ball)
        ball.brick_hit(brick)
        return True
    return False

# Game loop is always running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0))

    user_sprite.update()
    ball_sprites.update()
    brick_sprites.update()

    pygame.sprite.groupcollide(user_sprite, ball_sprites, False, False, platform_bounce)
    pygame.sprite.groupcollide(brick_sprites, ball_sprites, False, False, brick_hit)

    user_sprite.draw(screen)
    ball_sprites.draw(screen)
    brick_sprites.draw(screen)


    ## Print game over if the game is over (2.5 point)
    if not ball_sprites:
        text = font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 1.5))
        screen.blit(text, text_rect)

    # last step of game loop
    pygame.display.flip()
    game_settings.dt = clock.tick(game_settings.fps) / 1000
