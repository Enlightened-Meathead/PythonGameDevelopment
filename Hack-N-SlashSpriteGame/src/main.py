import pygame
import game_settings
from character import User

pygame.init()
screen = pygame.display.set_mode((game_settings.GAME_WIDTH, game_settings.GAME_HEIGHT))
clock = pygame.time.Clock()


# A dictionary of background images
background_images = {}
background_images["bg1"] = pygame.image.load("images/backgrounds/ancient_ruins.png")

# Sprite groups
user_sprite = pygame.sprite.GroupSingle()
user_sprite.add(User(screen, screen.get_width() / 2, screen.get_height() / 2))


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Load background image
    screen.blit(background_images["bg1"], (0,0))
    # Call the update methods
    user_sprite.update()

    # Draw the sprites
    user_sprite.draw(screen)

    pygame.display.flip()
    game_settings.dt = clock.tick(game_settings.fps) / 1000





