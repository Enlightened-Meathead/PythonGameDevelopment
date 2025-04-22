import pygame
import random

import game_settings
from character import User, Monster


pygame.init()
screen = pygame.display.set_mode((game_settings.GAME_WIDTH, game_settings.GAME_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
monsters_in_middle = 0

# A dictionary of background images
background_images = {}
background_images["bg1"] = pygame.image.load("images/backgrounds/ancient_ruins.png")

# Sprite groups
user_sprite = pygame.sprite.GroupSingle()
user_sprite.add(User(screen, screen.get_width() / 2, screen.get_height() / 2))

monster_sprites = pygame.sprite.Group()

def monster_hit(monster, user, attack_type):
    ## Modify hit boxes based on attack style
    if attack_type == "attack_3":
        shrunk_user_hitbox = user.rect.inflate(-100, -100)
        shrunk_monster_hitbox = monster.rect.inflate(-70, -70)
    elif attack_type == "attack_1":
        shrunk_monster_hitbox = monster.rect.inflate(-30, -30)
        shrunk_user_hitbox = user.rect.inflate(-10, -20)
    else:
        shrunk_monster_hitbox = monster.rect.inflate(0, 0)
        shrunk_user_hitbox = user.rect.inflate(0, 0)

    if shrunk_monster_hitbox.colliderect(shrunk_user_hitbox):
        monster.is_in_action = True
        monster.actions["faint"].is_active = True
        monster.actions["faint"].tick_of_action_start = pygame.time.get_ticks()
        return True
    return False


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Load background image
    screen.blit(background_images["bg1"], (0,0))
    ## Check if the monsters have made it to the middle
    if game_settings.monsters_succeeded == game_settings.game_loss_count:
        ## Print the player lost
        ## Informative text
        text = font.render(f"Monsters conquered your village...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
        screen.blit(text, text_rect)

    ## Continue the game if the player hasn't killed x amount of monsters
    elif game_settings.score < game_settings.win_score:
        ## Print the players current score:
        text = font.render(f"Score: {game_settings.score}", True, "#d8e7e0")
        text_rect = text.get_rect(center=(screen.get_width() - 570, screen.get_height() - 610))
        screen.blit(text, text_rect)

        ## Informative text
        text = font.render(f"Space and h to attack, wasd to move.", True, "#d8e7e0")
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 20))
        screen.blit(text, text_rect)

        # Spawn monsters
        while len(monster_sprites) < game_settings.monster_count:
            spawn_threshold = 100
            random_x = 0
            random_y = 0
            monster = Monster(screen, random_x, random_y)

            while True:
                random_x = random.randint(screen.get_rect().left + int(monster.rect.width/2),
                                          screen.get_rect().right - int(monster.rect.width/2))
                random_y = random.randint(screen.get_rect().top + monster.rect.height,
                                          screen.get_rect().bottom)
                if abs(random_x - user_sprite.sprite.position.x) > spawn_threshold and abs(random_y - user_sprite.sprite.position.y) > spawn_threshold:
                    break
            monster.position = pygame.Vector2(random_x, random_y)
            monster.rect.midbottom = monster.position

            monster_sprites.add(monster)


        # Call the update methods
        user_sprite.update()
        monster_sprites.update(user_sprite)

        if user_sprite.sprite.actions["attack_3"].is_active:
            pygame.sprite.groupcollide(monster_sprites, user_sprite, False, False, lambda m, u: monster_hit(m, u,"attack_3"))
        elif user_sprite.sprite.actions["attack_1"].is_active:
            pygame.sprite.groupcollide(monster_sprites, user_sprite, False, False,
                                       lambda m, u: monster_hit(m, u, "attack_1"))
    else:
        ## Print the player won
        ## Informative text
        text = font.render(f"You defended your village!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
        screen.blit(text, text_rect)

    # Draw the sprites
    monster_sprites.draw(screen)
    user_sprite.draw(screen)

    pygame.display.flip()
    game_settings.dt = clock.tick(game_settings.fps) / 1000

