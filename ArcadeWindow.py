import arcade
import arcade.gui
import random

class GameWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.score = 0
        self.lives = 3
        self.bullets = arcade.SpriteList()
        self.player = None
        self.enemies = None
        self.hearts = arcade.SpriteList()
        self.enemyBullets = arcade.SpriteList()
        self.player_dx =0
        self.player_dy = 0
        self.time = 0.0
        self.soundexplosion = None
        self.soundplayershoot = None
        self.soundenemyshoot = None
        self.soundgameover = None
        self.victory_sound = None
        self.gameOverMessage = None
        self.victoryMessage = None
        self.scoreMessage = None
        self.scoreTitle = "Score : "
        self.buttonTracker = None
        self.victoryTracker = None
        self.EnemySpeed = 6
        self.CurrentLevel = 0
        self.lastTimeFired = None
        self.victorySoundHasPlayed = False


    def createVictoryButton(self):
        self.victoryTracker = arcade.gui.UIManager()
        self.victoryTracker.enable()
        boxLayout = arcade.gui.UIBoxLayout()

        self.victoryTracker.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=boxLayout)
        )

        victoryButton = arcade.gui.UIFlatButton(text="Proceed to next level", width=200)
        boxLayout.add(victoryButton.with_space_around(bottom=20))
        victoryButton.on_click = self.on_click_next_level


    def createResetButton(self):
        self.buttonTracker = arcade.gui.UIManager()
        self.buttonTracker.enable()
        self.boxLayout = arcade.gui.UIBoxLayout()

        self.buttonTracker.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.boxLayout)
        )
        self.restartButton = arcade.gui.UIFlatButton(text="Retry", width=200)
        self.boxLayout.add(self.restartButton.with_space_around(bottom=20))
        self.restartButton.on_click = self.on_click_restart


    def on_click_restart(self, event):

        self.gameOverMessage = None
        self.buttonTracker = None
        #clear all current string of enemies off screen?
        self.setup()
        #self.update()
        #arcade.run()

    def on_click_next_level(self, event):
        print("goingtonextlevel")
        self.victoryMessage = None
        self.victoryTracker = None
        self.createVictoryButton()
        enemy_x = 100

        for n in range(8):
            enemy = arcade.Sprite("enemy.png")
            enemy.center_x = enemy_x
            enemy.center_y = 700
            enemy.scale = 0.1
            self.enemies.append(enemy)
            enemy_x = enemy_x + 100
        for n in range(8):
            enemy = arcade.Sprite("enemy.png")
            enemy.center_x = enemy_x
            enemy.center_y = 600
            enemy.scale = 0.1
            self.enemies.append(enemy)
            enemy_x = enemy_x + 100

        self.victorySoundHasPlayed = False

    def setup(self):

        enemy_x = 100
        enemy_y = 700

        heart_x = 40
        heart_y = 750

        self.soundexplosion = arcade.load_sound("explosion.wav")
        self.soundgameover = arcade.load_sound("GameOver.wav")
        self.soundenemyshoot = arcade.load_sound("enemyshooting.wav")
        self.soundplayershoot = arcade.load_sound("PlayerShooting.wav")
        self.victory_sound = arcade.load_sound("victory.wav")

        self.scoreMessage = arcade.Text(f"Score : {self.score}", 900, 750, arcade.color.WHITE, 30, 80, 'left')

       # Create six enemies!
        self.enemies = arcade.SpriteList()
        for n in range(6):
            enemy = arcade.Sprite("enemy.png")
            enemy.center_x = enemy_x
            enemy.center_y = enemy_y
            enemy.scale = 0.1
            self.enemies.append(enemy)
            enemy_x = enemy_x + 100

       # Create Three Hearts!
        for h in range(self.lives):
            heart = arcade.Sprite("heart.png")
            heart.center_x = heart_x
            heart.center_y = heart_y
            heart.scale = 0.15
            self.hearts.append(heart)
            heart_x = heart_x + 60

        self.player = arcade.Sprite("f1-ship1-6.png")
        self.player.center_x = self.width/2
        self.player.center_y = 50
        self.player.angle = 90

        #GUI BUTTON ETC STUFF BELOW
        #self.createResetButton()
        #self.createVictoryButton()

    def on_update(self, delta_time):
        self.player.center_x += self.player_dx
        if self.player.center_x >1200:
            self.player.center_x = 0
        if self.player.center_x <0:
            self.player.center_x = 1199

        self.moveBulletsUp()
        self.moveEnemy()

        # Check each enemy to see if any bullets hit it
        for enemy in self.enemies:
            bulletsHit = arcade.check_for_collision_with_list(enemy, self.bullets)
            # If there is anything in this list of bullets that collided, destroy it and the enemy
            if bulletsHit:
                # Destroy every bullet that collided with the enemy
                for bullet in bulletsHit:
                    self.bullets.remove(bullet)
                # Destroy the enemy
                self.enemies.remove(enemy)
                enemy.remove_from_sprite_lists()
                self.score = self.score + 20

        # Check whether all the enemies have been shot
        if len(self.enemies) == 0 and not self.victorySoundHasPlayed:
            # PLAYER WON!
            arcade.play_sound(self.victory_sound)
            self.victorySoundHasPlayed = True
            self.createVictoryButton()
            self.victorytext()

        # Check whether any enemies crashed into the player
        for enemy in self.enemies:
            enemiesThatHitThePlayer = arcade.check_for_collision_with_list(self.player, self.enemies)
            # If any enemies in this list collided with the player, destroy it and the player
            if enemiesThatHitThePlayer:
                # Destroy the enemy
                self.enemies.remove(enemiesThatHitThePlayer[0])
                arcade.play_sound(self.soundexplosion)
                if len(self.hearts) > 0:
                    self.hearts.remove(self.hearts[len(self.hearts) - 1])
                if len(self.hearts) <= 0:
                    # THE GAME IS OVER!!!!!
                    self.player.kill()
                    self.createResetButton()
                    self.gameovertext()
                if len(self.enemies) == 0 and len(self.hearts) >= 0 and not self.victorySoundHasPlayed:
                    # PLAYER WON!!!
                    arcade.play_sound(self.victory_sound)
                    self.victorySoundHasPlayed = True
                    self.createVictoryButton()
                    self.victorytext()
                    #self.victoryTrackTracker.draw()

        # ENEMY BULLETS HITTING THE PLAYER!!
        for enemy in self.enemies:
            EnemybulletsHitPlayer = arcade.check_for_collision_with_list(self.player, self.enemyBullets)
            # If there is anything in this list of bullets that collided, take away a player life
            if EnemybulletsHitPlayer:
                arcade.play_sound(self.soundexplosion)
                # Destroy every bullet that collided with the player
                for enemyBullets in EnemybulletsHitPlayer:
                    self.enemyBullets.remove(enemyBullets)
                    if len(self.hearts) > 0:
                        self.hearts.remove(self.hearts[len(self.hearts) - 1])
                    if len(self.hearts) <= 0:
                        # THE GAME IS OVER!!!!!!!!
                        self.player.kill()
                        self.createResetButton()
                        self.gameovertext()

        self.enemyShoot(delta_time)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullets:
            if bullet.bottom > self.height - 200:
                bullet.remove_from_sprite_lists()


    def on_draw(self):

        self.clear()

        arcade.start_render()
        self.player.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.hearts.draw()
        self.enemyBullets.draw()

        #self.button_tracker.draw()
        self.scoreMessage = arcade.Text(f"Score : {self.score}", 900, 750, arcade.color.WHITE, 30, 80, 'left')
        self.scoreMessage.draw()

        if (self.gameOverMessage):
            self.gameOverMessage.draw()
            #self.createResetButton()
            self.buttonTracker.draw()

        if (self.victoryMessage):
            self.victoryMessage.draw()
            self.victoryTracker.draw()


        # self.targets.draw()
        arcade.finish_render()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player_dx = -3
        elif symbol == arcade.key.RIGHT:
            self.player_dx = 3
       # elif symbol == arcade.key.UP:
       #     self.player_dy = 3

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.player_dx = 0
        elif symbol == arcade.key.RIGHT:
            self.player_dx = 0
        #elif symbol == arcade.key.UP:
        #    self.player_dy = 0

    def on_mouse_press(self, x, y, button, modifiers):
        # Check to limit 5 visible bullets at a time
        numBulletsOnScreen = len(self.bullets)
        print(f"There are {numBulletsOnScreen} bullets on the screen")
        if len(self.bullets) < 5:
            print("Adding a bullet")
            shootgun = arcade.Sprite("shoot.png")
            shootgun.center_x = self.player.center_x
            shootgun.center_y = self.player.center_y + 74
            shootgun.angle = 90
            self.bullets.append(shootgun)
            arcade.play_sound(self.soundgameover)

    def gameovertext(self):
        self.gameOverMessage = arcade.Text("Game Over! Retry? : ", 450, 300, arcade.color.RED_DEVIL, 30, 80, 'left')
        #self.gameOverMessage.draw()

    def victorytext(self):
        #self.victoryMessage = None
        self.victoryMessage = arcade.Text("Congrats! : ", 280, 400, arcade.color.WHITE, 30, 80, 'left')

    def moveBulletsUp(self):
        for bullet in self.bullets:
            bullet.center_y += 7

    def moveEnemy(self):
        for enemy in self.enemies:
            enemy.center_x += self.EnemySpeed #19 #6 #1.5
        for enemy in self.enemies:
            if enemy.center_x > 1200:
                enemy.center_x = 0
                enemy.center_y = enemy.center_y - 100
            if enemy.center_y < 50:
                enemy.center_y = enemy.center_y = 50


    def enemyShoot(self, delta_time):
        #print("deltaTime is " )
        #print(deltaTime)
        for enemy in self.enemies:
            odds = 500
            adj_odds = int(odds * (1 / 60) / delta_time)

            if random.randrange(adj_odds) == 0:
                enemybullet = arcade.Sprite("EnemyLazer2.png")
                enemybullet.angle = -90
                enemybullet.scale = 0.2
                enemybullet.center_x = enemy.center_x
                enemybullet.top = enemy.bottom
                enemybullet.change_y = -5
                self.enemyBullets.append(enemybullet)
                arcade.play_sound(self.soundenemyshoot)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.enemyBullets:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.enemyBullets.update()