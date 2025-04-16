# Step 2 Task List 
- **All of my improvement code snippets can be found below comments starting with '##'**

***Randomized Ball Start (5 points)***
- Have the ball start in a random downward direction when the user presses spacebar. This should work with the existing structure of the game (i.e. keep track of the angle)

Student Comments:
- The ball will start moving in a random direction via the following code addition to the "listen_to_start" function in "ball.py" class file:
```
## Randomized ball start (5 points)
random_angle = random.randint(10,80) <- This creates a random angle between 10 and 80 degrees 
radians = math.radians(random_angle) <- Grabs the radian values for the randomly generated angle
self.velocity.x = math.cos(radians) <--- The two radian values are assigned to the correlating sine and cosine 
self.velocity.y = math.sin(radians) <-'
self.angle = random_angle <- Angle value is updated with the random angle
```


---
***Informative Text (5 points)***
- Add text to the game. At a minimum, the text should inform the user to hit spacebar to start (leaving after the user hits spacebar) and when the game is over (appearing only after the user loses)

Student Comments:
    Text was added to the game when it begins asking the player to hit the spacebar to start and when the game has ended. Text is also displayed for the life counter in the top left corner of the game screen, described the "Player Life" section.

- The code below comes from the "listen_to_start" function in the "ball.py" class. If the player hasn't pressed space and the game has not started, the text telling the player to press start is rendered on the screen.
```
## Start font (2.5 Points)
if not self.game_started:
    text = font.render("Press SPACE to Start!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 1.5))
    self.surface.blit(text, text_rect)
```

- In the "main.py", each game loop checks that their is a ball object in the ball_sprites group. If not, the game over text is rendered to the screen.
```
## Print game over if the game is over (2.5 point)
if not ball_sprites:
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 1.5))
    screen.blit(text, text_rect)
```
---

***Player Life (10 points)***
- Keep track of the player life. The player life should go down when a ball makes it past the user's platform. The players number of lives should be displayed on the screen. 
- After the ball goes of the screen, another one should take its place

Student Comments:
- In the ball class' init method, the life attribute is declared:
```
## Number of lives for the game
self.lives = game_settings.lives
```
- If the ball goes below the screen bottom, the lives are decremented by 1, the game_started attribute is set to false, and the ball resets to the starting position while the "listen_to_start" function is called to pause the ball again until the user presses space. Once lives are at zero, the ball does "self.kill()" and the ball sprite no longer exists.
```
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
```

- The "update" function for the ball class calls this function every frame to print out the lives remaining in the top left corner of the screen:
```
## Print the lives on the top left of the screen every frame (10 points)
def print_lives(self):
    text = lives_font.render(f"Remaining Lives: {self.lives}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(self.surface.get_width() // 9, self.surface.get_height() // 12))
    self.surface.blit(text, text_rect)
```
