# Step 2 Task List
- **All of my improvement code snippets can be found below comments starting with '##'**
---
***Tower Sprite (5 points)***
- Download or create a sprite that will serve as the image for the towers. This only needs to be a singular image, but you could an animation if you would like.

Student Comments:
- For the tower, an archer sprite was used. This sprite used an animation of an archer firing and the animation would halt when no enemies were near to be fired at. The sprite image tileset and json data can be found in `src/images/sprites/`

- The code to implement this was as follows:
    - in the tower.py file Tower class init method:
```

    ## Tower Animation setup
    self.frames = self.load_frames("images/sprites/Archer_Blue.png", "images/sprites/Archer_Blue.json") <- load in the frames from the asset files
    ## get rid of the last two frames because they are just arrows
    self.frames = self.frames[:-2]
    self.index = 0
    self.image = self.frames[self.index] <- Set the frames sprite image to the index attribute
    # Get the position of the tile center
    tile_x = cell[0] * game_settings.COL_SIZE + game_settings.COL_SIZE // 2
    tile_y = cell[1] * game_settings.ROW_SIZE + game_settings.ROW_SIZE // 2
    ## Animation timing
    self.counter = 0
    self.animation_speed = 0.2

```
- The load frames function was as follows:
```

    ## Load the frames for the tower animation
    def load_frames(self, sprite_sheet_path, json_path): <- pass in the sprite sheet and json data
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        with open(json_path) as f:
            data = json.load(f) <- load in the json

        frames = []
        for frame_name in data["frames"]: <- for each frame in the data sheet, create an image from it and append to the frames list to be loaded into the object
            frame = data["frames"][frame_name]["frame"]
            rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
            image = sheet.subsurface(rect)
            frames.append(image)
        return frames

```
- The update method for the Tower was updated to this:
```
    def update(self):
        # Firing logic
        if pygame.time.get_ticks() - self.tick_of_last_shot >= self.fire_rate:
            self.fire_at_closest_target()
            self.is_firing = True <- if the target is withing firing range, set to true
        else:
            self.is_firing = False

        ## Animate tower if its firing
        if not self.is_firing:
            self.counter += self.animation_speed
            if self.counter >= 1:
                self.index = (self.index + 1) % len(self.frames)
                self.image = self.frames[self.index]
                self.counter = 0

```
---

***Enemy Sprites (10 points)***
- Download or Create sprites for the enemies. 
- Enemies should have at least three sprites in their sprite sheet--moving down (positive y), moving left or right (x != 0), and moving up (negative y). These should be visually different.

Student Comments:
- A goblin carrying tnt was used for the enemy sprite. The animation process was the same as above for the tower sprite, with the only additional logic highlighted below. When the goblin was moving left or right, the image is mirrored to reflect this. As the sprite animation did not have a specific upward and downward animation, only left and right mirroring was implemented.

- In the Enemy init method `self.facing_right = True` is set. Within the `update` method, the following logic is added:
```
## Determine direction toward the next waypoint
if self.current_waypoint + 1 < len(self.waypoints):
    next_wp = self.waypoints[self.current_waypoint + 1]
    dx = next_wp.x - self.position.x
    if dx < -1:
        self.facing_right = False <- if the x direction is moving left, make the facing attribtue false
    elif dx > 1:
        self.facing_right = True

## Flip the image if needed
if not self.facing_right: <- if the x direction is left, then mirror the image to face the left
    frame = pygame.transform.flip(frame, True, False)

self.image = frame
```
---

***Player Life (10 points)***
- Keep track of the player life. The player life should go down when a enemy makes it through the maze. The players number of lives should be displayed on the screen. 


Student Comments:

- In the game settings file, a player life variable was added to keep track of how many enemies have made it to the final waypoint. If an enemy makes it to the final waypoint, the user gets a life decremented. If all lives are lost, then the game ends, no new frames are rendered, and a game over banner is rendered to the screen.

- If the enemy has no more waypoints to go, then they are logically at the end of the map. When they despawn, decrement a player life
```
else:
    ## If the enemy makes it to the end of the level, decrement the player life
    game_settings.player_lives -= 1
    self.kill()
```

- In the main game loop, the following logic takes care of the rest:
```
## Print player lives
lives_text = pygame.font.Font.render(font,f"Lives: {game_settings.player_lives}", True, "#FFFFFF") <- player life text
screen.blit(money_text, (40, game_settings.GAME_HEIGHT - 550))
screen.blit(lives_text, (40, game_settings.GAME_HEIGHT - 520)) <- render lives to the screen
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

```

---
