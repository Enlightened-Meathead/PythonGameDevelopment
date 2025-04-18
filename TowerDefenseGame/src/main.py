import pygame
import game_settings
from level_data import level_one
from enemy import Enemy
from tower import Tower
from spritegroups import enemies, towers, projectiles

pygame.init()
screen = pygame.display.set_mode((game_settings.GAME_WIDTH, game_settings.GAME_HEIGHT))
clock = pygame.time.Clock()


# Mouse cursors
blue_cursor = pygame.image.load('images/cursors/blue-cursor.png')
red_x_cursor = pygame.image.load('images/cursors/red-x-cursor.png')

# Collision callback function
def enemy_hit(enemy, projectile):
    collided = pygame.sprite.collide_rect(enemy, projectile)
    if collided:
        enemy.hp -= projectile.damage
        if enemy.hp <= 0:
            game_settings.player_money += enemy.bounty
            enemy.kill()
        else:
            pass
        #     enemy.update_color()
        return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(level_one.background, (0,0))

    # Grab mouse position to overlay cursor
    mouse_position = pygame.mouse.get_pos()
    col = mouse_position[0] // game_settings.COL_SIZE
    row = mouse_position[1] // game_settings.ROW_SIZE
    # Lets you know if your mouse is in the game area
    mouse_position_in_bounds = (row >= 0 and row <= game_settings.NUM_OF_ROWS and col >= 0 and
                                col <= game_settings.NUM_OF_COLS)
    mouse_pressed = pygame.mouse.get_pressed(3)
    if mouse_position_in_bounds:
        mouse_cursor_position = pygame.Rect((col * game_settings.COL_SIZE, row * game_settings.ROW_SIZE),
                                            (game_settings.COL_SIZE,game_settings.ROW_SIZE))
        if not level_one.blocked_tiles[row][col]:
            screen.blit(blue_cursor, mouse_cursor_position)
            if mouse_pressed[0]:
                tower = (Tower((col, row)))
                if game_settings.player_money - tower.cost >= 0:
                    towers.add(tower)
                    level_one.add_cell_to_tiles((row, col), level_one.blocked_tiles)
                    game_settings.player_money -= tower.cost
                else:
                    tower.kill()
        else:
            screen.blit(red_x_cursor, mouse_cursor_position)

    if len(enemies) < game_settings.enemy_wave_size and pygame.time.get_ticks() - game_settings.tick_of_last_enemy_spawn >= 500:
        enemies.add(Enemy(level_one))

    # Game text
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    money_text = pygame.font.Font.render(font,f"${game_settings.player_money}", True, "#FFFFFF")
    ## Print player lives
    lives_text = pygame.font.Font.render(font,f"Lives: {game_settings.player_lives}", True, "#FFFFFF")
    screen.blit(money_text, (40, game_settings.GAME_HEIGHT - 550))
    screen.blit(lives_text, (40, game_settings.GAME_HEIGHT - 520))
    # Updates
    ## Check player lives are above zero, otherwise stop rendering new frames and print the game over
    if game_settings.player_lives > 0:
        enemies.update()
        towers.update()
        projectiles.update()

        # Check for collisions
        enemies_hit = pygame.sprite.groupcollide(enemies, projectiles, False, True, enemy_hit)

        #Render the sprite groups
        enemies.draw(screen)
        towers.draw(screen)
        projectiles.draw(screen)

    else:
        ## If player runs out of lives, print game over sign
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        game_over_sign = pygame.font.Font.render(font, f"The Goblins blew up your gold mine!", True, "#FFFFFF")
        game_over_rect = game_over_sign.get_rect(center = (game_settings.GAME_WIDTH // 2, game_settings.GAME_HEIGHT // 2))
        screen.blit(game_over_sign, game_over_rect)


    pygame.display.flip()
    game_settings.dt = clock.tick(game_settings.fps) / 1000