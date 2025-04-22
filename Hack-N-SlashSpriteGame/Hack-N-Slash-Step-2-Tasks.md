# Step 2 Task List
- **All of my improvement code snippets can be found below comments starting with '##'**
---
***Balance: Winning and Losing (5 points)***
- Create a mechanic for winning and losing the game.

Student Comments:
- A winning and losing mechanic was added to the game by adding a score that is incremented when a monster is defeated and the player losing when a certain number of monsters make it to the center of the map.
- First, a few variables were added to keep track of the score as well as monsters who are idling in the center:
```
## Player score to win and current score
win_score = 25 <- sets how many monsters the player needs to defeat to win
score = 0 <- score starts at zero, increments each time a monster sprite initiates a faint action

## Monster count to cause game loss
game_loss_count = 5 <- sets how many monsters need to make it to the middle for the player to lose
monsters_succeeded = 0 <- get incremented when a monster makes it to the center and idles
```

- Next, in the Monster subclass in the `character.py` file, the following was added to the init method:
```
## For the duration of an action, use this flag so the score doesnt update every frame
self.score_incremented = False
```
- Then in the else chain for the Monster's `update` method, this score is incremented:
```
if self.actions[action].is_active:
    self.run_action(self.actions[action])
    ## Increment score if the action results in a sprite being killed
    if not self.score_incremented: <- this is neccesary otherwise the score will increment every frame
        game_settings.score += 1
    self.score_incremented = True <- sets the monster score incremented to true so the next loop in the frame doesn't add more than 1 to the player score
```

- The monster also has another attribute added :`self.is_idling = False`. This is a flag that allows tracking if the monster is at idle. If the monster has made it to the center of the map, it will idle, and therefore should increment the monsters that have succeeded and count against the player losing.
```
## If idling, have the monsters.succeeded incremented
if self.is_running:
    self.image = self.animations["run"].run_animation(80, True)
    self.is_idling = False <- make sure that if the monster isn't idling the monster isn't counted against the player losing
elif self.velocity.magnitude() !=0:
    self.image = self.animations["walk"].run_animation(80, True)
    self.is_idling = False <- make sure that if the monster isn't idling the monster isn't counted against the player losing
else:
    self.image = self.animations["idle"].run_animation(80,True)
    if not self.is_idling:
        game_settings.monsters_succeeded += 1 <- similar logic to the monster score update method. Updates the monsters_succeded variable in the game settings once the action is initiated and not every frame
    self.is_idling = True
```


- Within the `main.py` game loop, the first if check is the following:
```
if game_settings.monsters_succeeded == game_settings.game_loss_count: <- if the player has let the monsters take over the center, they lose
    ## Print the player lost
    ## Informative text
    text = font.render(f"Monsters conquered your village...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    screen.blit(text, text_rect)
```
- This also cuts any further update methods from being applied so the game and sprite freeze in their last frame and position before the game was won.
- If the player has not reached the score, the main game loop begins with the following:
 ```
## Continue the game if the player hasn't killed x amount of monsters
elif game_settings.score < game_settings.win_score: <- if the user hasnt exceeded the score to win, the game continues
    ## Print the players current score:
    text = font.render(f"Score: {game_settings.score}", True, "#d8e7e0")
    text_rect = text.get_rect(center=(screen.get_width() - 570, screen.get_height() - 610))
    screen.blit(text, text_rect) <- the players current score is printed onto the screen real time
 ```

- Else, if the score has exceeded the needed points to win and the monsters have not made it to the center, blit that the player has won:
```
  else:
  ## Print the player won
  ## Informative text
  text = font.render(f"You defended your village!", True, (255, 255, 255))
  text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
  screen.blit(text, text_rect)
```


---

***Informative Text (5 points)***
- Add text to the game. At a minimum, the text should inform the user how to perform actions. 
 
*Student Comments:*
- In the game, multiple points of informative text have been added. First, if the player wins or loses, all sprites stop updating and the game is frozen with a win or loss message shown across the screen. This text was shown in the above example for the player win and lose mechanic.
- The other informative text was added like so to show the player how to play:
```
## Informative text
text = font.render(f"Space and h to attack, wasd to move.", True, "#d8e7e0")
text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 20))
screen.blit(text, text_rect)
```
---

***Additional Action (10 points)***
- Your character should have an additional action. 

Student Comments:
- The player character was given an additional heavy attack. The standard attack happens much faster and has less cooldown time, but the hitbox is much smaller and is more for an indivindual monster. The heavy attack is a slow but wide arcing swing with a big hitbox for taking out a horde of enemies. 
- The monster_hit function in `main.py` was modified to allow this to happen:
```
def monster_hit(monster, user, attack_type):
## Modify hit boxes based on attack style
if attack_type == "attack_3": <- the regular attack animation
shrunk_user_hitbox = user.rect.inflate(-100, -100) <- shrink the user hitbox 
shrunk_monster_hitbox = monster.rect.inflate(-70, -70) <- shrink the monster hitbox 
elif attack_type == "attack_1": <- the heavy attack
shrunk_monster_hitbox = monster.rect.inflate(-30, -30)
shrunk_user_hitbox = user.rect.inflate(-10, -20)
else: <- have an else here to keep the IDE from yelling at me
shrunk_monster_hitbox = monster.rect.inflate(0, 0)
shrunk_user_hitbox = user.rect.inflate(0, 0)

    if shrunk_monster_hitbox.colliderect(shrunk_user_hitbox): <- check if the hitboxes collide, then act accordingly
        monster.is_in_action = True
        monster.actions["faint"].is_active = True
        monster.actions["faint"].tick_of_action_start = pygame.time.get_ticks()
        return True
    return False
```

- The second attack was added to the User character subclass in the `character.py` file like so:
```
self.animations["attack_3"] = SpriteSurface("images/sprites/samurai/Attack_3.png",
                                         4,
                                         128,
                                         128)
# Set up character actions
self.actions["attack_1"] = CharacterAction("attack_1", self.animations["attack_1"], 200, False)
self.actions["attack_3"] = CharacterAction("attack_3", self.animations["attack_3"], 100, False) <- add the heavy attack to the players actions
```

- With the additional attack, we have to be able to listen for a keypress. I used 'h' standing for the 'h'eavy attack
``` 
## Additional heavy attack
if keys[pygame.K_h]:
    self.run_action(self.actions["attack_1"])
```

---
