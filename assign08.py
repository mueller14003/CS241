"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random
from abc import ABC, abstractmethod
import pyglet

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

BULLET_LENGTH = 35
BULLET_WIDTH = 25
BULLET_SPEED = 10
BULLET_LIFE = 60

POWER_UP_BULLET_LENGTH = 65
POWER_UP_BULLET_WIDTH = 20

ENEMY_BULLET_LENGTH = 70
ENEMY_BULLET_WIDTH = 20

SHIP_TURN_AMOUNT = 3
SHIP_TURN_MULTIPLIER = 2
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 65
PLAYER_TWO_RADIUS = 45
SHIP_BASE_HEALTH = 100

ENEMY_SHIP_RADIUS = 35
ENEMY_SHIP_HEALTH = 100
ENEMY_SHIP_SPAWN_TIMER = 500
ENEMY_SHIP_SPEED = 2

ENEMY_FREIGHTER_RADIUS = 55
ENEMY_FREIGHTER_HEALTH = 200
ENEMY_FREIGHTER_SPAWN_TIMER = 2000

POWER_UP_HEIGHT = 75
POWER_UP_WIDTH = 30
POWER_UP_RADIUS = 40

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30
BIG_ROCK_DAMAGE = 10

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 20
MEDIUM_ROCK_DAMAGE = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 10
SMALL_ROCK_DAMAGE = 2

ASTEROID_SPAWN_TIMER = 300
DEFAULT_SHOOT_TIMER = 3

POWER_UP_TIMER = 750
POWER_UP_ALIVE_TIMER = 150

MAIN_MENU = 0
GAME_RUNNING = 1
TRANSITION = 2
GAME_OVER = 3

MAX_SPEED = 15
SPAWN_DISTANCE = 200


def set_new_asteroid(new, old, dx, dy):
    """
    This function receives the old and the new asteroid as input, and also receives
    another dx and dy value to be added to the old asteroid's dx and dy. This function
    essentially sets up the new asteroid.
    :param new: Asteroid being created
    :param old: Asteroid that was destroyed
    :param dx: dx that will be added to old dx for new asteroid
    :param dy: dy that will be added to old dy for new asteroid
    :return: new asteroid (modified)
    """
    new.center.x = old.center.x
    new.center.y = old.center.y
    new.velocity.dx = old.velocity.dx + dx
    new.velocity.dy = old.velocity.dy + dy
    return new


class Point:
    """
    Creates a class that will store a location in the xy plane.
    """
    def __init__(self):
        self.x = 0
        self.y = 0

    def new_location(self, ship_1, ship_2):
        self.x = random.uniform(1, SCREEN_WIDTH - 1)
        self.y = random.uniform(1, SCREEN_HEIGHT - 1)
        while (abs(ship_1.center.x - self.x) < SPAWN_DISTANCE or abs(ship_1.center.y - self.y) < SPAWN_DISTANCE) and \
                (abs(ship_2.center.x - self.x) < SPAWN_DISTANCE or abs(ship_2.center.y - self.y) < SPAWN_DISTANCE):
            self.x = random.uniform(1, SCREEN_WIDTH - 1)
            self.y = random.uniform(1, SCREEN_HEIGHT - 1)


class Velocity:
    """
    Creates a class that will store velocity values.
    """
    def __init__(self):
        self.dx = 0
        self.dy = 0


class FlyingObject:
    """
    Creates class for Flying Objects. This is a base class for other
    flying objects classes that will be created. Contains methods:
        advance
        draw
        check_off_screen
    """
    def __init__(self):
        """
        Creates and sets class variables.
        """
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0
        self.alive = True
        self.angle = 0
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.image = "Doge.png"
        self.alpha = 1

    def advance(self):
        """
        Changes the position of a flying object
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def draw(self):
        """
        Draws a flying object
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius * 2, self.radius * 2, texture,
                                      self.angle, self.alpha)

    def check_off_screen(self):
        """
        Checks to see whether a flying object is off the screen.
        Relocates it on the other side.
        """
        if self.center.x <= 0:
            self.center.x = SCREEN_WIDTH - 1
        elif self.center.x >= SCREEN_WIDTH:
            self.center.x = 1
        elif self.center.y <= 0:
            self.center.y = SCREEN_HEIGHT - 1
        elif self.center.y >= SCREEN_HEIGHT:
            self.center.y = 1


class Asteroid(FlyingObject, ABC):
    """
    Asteroid class inherits from the Flying Object class. This class will be used to model other
    classes for different types of asteroids.
    """
    def __init__(self):
        super().__init__()
        self.image = "GrumpyCat.png"
        self.radius = BIG_ROCK_RADIUS
        self.spin = BIG_ROCK_SPIN
        self.velocity_angle = random.uniform(0, 359)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.velocity_angle)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.velocity_angle)) * self.speed
        self.type = 1

    def rotate(self):
        """
        Changes angle of asteroid depending on self.spin value.
        """
        self.angle += self.spin

    def advance(self):
        self.rotate()
        super().advance()

    @abstractmethod
    def split(self, asteroids):
        """
        Will be responsible for splitting up an asteroid after getting hit.
        :param asteroids: list containing all asteroids in game class.
        """
        pass

    @abstractmethod
    def hit(self, power):
        pass

    @abstractmethod
    def damage(self, power):
        pass

    @abstractmethod
    def hit_ship(self, power):
        pass


class LargeAsteroid(Asteroid):
    """
    Large Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()

    def split(self, asteroids):
        """
        Splits up large asteroid into smaller asteroids.
        :param asteroids: list containing all asteroids from game.
        :return: asteroids
        """
        med_1 = MediumAsteroid()
        med_1 = set_new_asteroid(med_1, self, 0, 2)
        med_2 = MediumAsteroid()
        med_2 = set_new_asteroid(med_2, self, 0, -2)
        small_1 = SmallAsteroid()
        small_1 = set_new_asteroid(small_1, self, 5, 0)
        asteroids.extend([med_1, med_2, small_1])
        self.alive = False
        return asteroids

    def hit(self, power):
        if power:
            return 20
        else:
            return 10

    def damage(self, power):
        if not power:
            return 5
        else:
            return 0

    def hit_ship(self, power):
        if not power:
            return BIG_ROCK_DAMAGE
        else:
            return 0


class MediumAsteroid(Asteroid):
    """
    Medium Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()
        self.image = "GrumpyCat.png"
        self.radius = MEDIUM_ROCK_RADIUS
        self.spin = MEDIUM_ROCK_SPIN
        self.type = 2

    def split(self, asteroids):
        """
        Splits up medium asteroid into smaller asteroids.
        :param asteroids: list containing all asteroids from game.
        :return: asteroids
        """
        small_1 = SmallAsteroid()
        small_1 = set_new_asteroid(small_1, self, 1.5, 1.5)
        small_2 = SmallAsteroid()
        small_2 = set_new_asteroid(small_2, self, -1.5, -1.5)
        asteroids.extend([small_1, small_2])
        self.alive = False
        return asteroids

    def hit(self, power):
        if power:
            return 10
        else:
            return 5

    def damage(self, power):
        if not power:
            return 3
        else:
            return 0

    def hit_ship(self, power):
        if not power:
            return MEDIUM_ROCK_DAMAGE
        else:
            return 0


class SmallAsteroid(Asteroid):
    """
    Small Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()
        self.image = "GrumpyCat.png"
        self.radius = SMALL_ROCK_RADIUS
        self.spin = SMALL_ROCK_SPIN
        self.type = 3

    def split(self, asteroids):
        """
        Sets alive to false, returns asteroids.
        :param asteroids: list containing all asteroids from game.
        :return: asteroids
        """
        self.alive = False
        return asteroids

    def hit(self, power):
        if power:
            return 5
        else:
            return 2

    def damage(self, power):
        if not power:
            return 1
        else:
            return 0

    def hit_ship(self, power):
        if not power:
            return SMALL_ROCK_DAMAGE
        else:
            return 0


class Laser(FlyingObject):
    """
    Laser class, inherits from Flying Object class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/REDLASER.png"
        self.center.x = 0
        self.center.y = 0
        self.radius = 25
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED
        self.type = 1
        self.length = 35
        self.width = 25

    def advance(self):
        if self.life > 0:
            super().advance()
            self.life -= 1
        else:
            self.alive = False

    def draw(self):
        """
        Changes draw to use length and width.
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.length, self.width, texture,
                                      self.angle, self.alpha)

    def fire(self, ship):
        """
        Fires bullet at an angle and a speed.
        :param ship: ship from game
        """
        self.velocity.dx = ship.velocity.dx + (math.cos(math.radians(ship.angle)) * self.speed)
        self.velocity.dy = ship.velocity.dy + (math.sin(math.radians(ship.angle)) * self.speed)


class EnemyLaser(Laser):
    """
    Enemy laser class, inherits from Laser class.
    """
    def __init__(self):
        super().__init__()
        self.image = "NYAN_CAT.png"
        self.type = 2
        self.length = ENEMY_BULLET_LENGTH
        self.width = ENEMY_BULLET_WIDTH


class PowerUp(FlyingObject):
    """
    Power up class, inherits from Flying Object class. Will cause a power up for user that
    comes into contact with it.
    """
    def __init__(self):
        super().__init__()
        self.image = "Old_Spice.png"
        self.height = POWER_UP_HEIGHT
        self.width = POWER_UP_WIDTH
        self.radius = POWER_UP_RADIUS
        self.timer = POWER_UP_ALIVE_TIMER

    def draw(self):
        """
        Changes draw to use length and width.
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, texture,
                                      self.angle, self.alpha)


class Ship(FlyingObject):
    """
    Ship class, inherits from Flying Object class. This is the ship that the user will
    control in the game class.
    """
    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.health = SHIP_BASE_HEALTH
        self.type = 0
        self.thrust = SHIP_THRUST_AMOUNT
        self.turn = SHIP_TURN_AMOUNT
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 8

    def accelerate(self):
        """
        Increases speed when triggered.
        """
        if abs(self.velocity.dx) < MAX_SPEED:
            self.velocity.dx += math.cos(math.radians(self.angle)) * self.thrust
        if abs(self.velocity.dy) < MAX_SPEED:
            self.velocity.dy += math.sin(math.radians(self.angle)) * self.thrust

    def decelerate(self):
        """
        Decreases speed when triggered.
        """
        self.velocity.dx /= 2
        self.velocity.dy /= 2

    def turn_left(self, m=1):
        """
        Changes angle of ship (rotates  left)
        :param m: multiplier
        """
        self.angle += self.turn * m

    def turn_right(self, m=1):
        """
        Changes angle of ship (rotates  right)
        :param m: multiplier
        """
        self.angle -= self.turn * m

    @property
    def speed(self):
        """
        Returns speed of ship (rounded to nearest .25)
        :return:
        """
        speed = math.sqrt((self.velocity.dx ** 2) + (self.velocity.dy ** 2))
        speed = round(speed*4)/4
        return speed


class PlayerTwoShip(Ship):
    """
    Player Two Ship class, inherits from ship class. This is the ship used by
    player two in the game class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Jar_Jar_Binks.png"
        self.type = 2
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 8


class LaserTwo(Laser):
    """
    Laser shot by player two.
    """
    def __init__(self):
        super().__init__()
        self.type = 3


class AggressiveEnemyShip(Ship):
    """
    Class for Aggressive enemy ship, inherits from ship class. This ship will attack the player(s).
    """
    def __init__(self):
        super().__init__()
        self.image = "WOW.png"
        self.radius = ENEMY_SHIP_RADIUS
        self.health = ENEMY_SHIP_HEALTH
        self.enemy_speed = ENEMY_SHIP_SPEED
        self.type = 1
        self.outside_ship = None

    def set_target(self, ship):
        """
        Sets target as ship that is closest.
        :param ship:
        """
        self.outside_ship = ship

    def set_speed(self, actual_dist):
        """
        Sets speed of enemies.
        :param actual_dist: distance from target
        """
        self.enemy_speed = actual_dist / 100

    def advance(self):
        """
        Enemy advances according to proximity to target.
        """
        dist_x = self.center.x - self.outside_ship.center.x
        dist_y = self.center.y - self.outside_ship.center.y
        actual_dist = math.sqrt((dist_x ** 2) + (dist_y ** 2))
        self.set_speed(actual_dist)
        if actual_dist > SPAWN_DISTANCE:
            self.velocity.dx = math.cos(math.radians(self.angle)) * self.enemy_speed
            self.velocity.dy = math.sin(math.radians(self.angle)) * self.enemy_speed
        elif abs(dist_x) < SPAWN_DISTANCE:
            self.velocity.dx = 0
        elif abs(dist_y) < SPAWN_DISTANCE:
            self.velocity.dy = 0
        super().advance()

    def avoid_bullets(self, bullet):
        """
        Will allow enemy to avoid incoming bullets
        :param bullet: closest bullet
        """
        dist_x = self.center.x - bullet.center.x
        dist_y = self.center.y - bullet.center.y
        actual_dist = math.sqrt((dist_x ** 2) + (dist_y ** 2))
        #TODO: Not sure how to implement yet.
        pass


class EnemyFreighter(Ship):
    """
    Large enemy ship, inherits from ship class. This ship is large and has lots of health.
    When the user destroys it, a power up will appear.
    """
    def __init__(self):
        super().__init__()
        self.image = "NicolasCage.png"
        self.radius = ENEMY_FREIGHTER_RADIUS
        self.health = ENEMY_FREIGHTER_HEALTH
        self.type = 2
        self.velocity.dx = random.uniform(-1, 1)
        self.velocity.dy = random.uniform(-1, 1)
        self.length = 200
        self.width = 75


# TODO: Make main menu, better a.i., etc.
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.media_player = pyglet.media.Player()
        self.game_over_sound = pyglet.media.load("GameOver.wav")
        self.play_game_over = False
        self.game_over_player = pyglet.media.Player()
        self.game_over_player.queue(self.game_over_sound)
        self.sound = pyglet.media.load("HEYYEYAAEYAAAEYAEYAA.wav")
        self.play_sound = True
        self.play_game_over = False
        self.looper = pyglet.media.SourceGroup(self.sound.audio_format, None)
        self.looper.loop = True
        self.looper.queue(self.sound)
        self.tie_fighter_blast = arcade.load_sound("Wow!.wav")
        self.x_wing_blast = arcade.load_sound("PEW.wav")
        self.millennium_falcon_blast = arcade.load_sound("PEW.wav")
        self.pause_sound = arcade.load_sound("PAUSE.wav")
        self.background = arcade.load_texture("388.jpg")
        self.media_player.queue(self.looper)
        self.mute = False
        self.quit = False

        self.held_keys = set()

        # I made all of these variables...
        self.ship = Ship()
        self.player_two = PlayerTwoShip()
        self.asteroids = []
        self.bullets = []
        self.initial_rocks = INITIAL_ROCK_COUNT
        self.enemies = []
        self.score = 0
        self.score_2 = 0
        self.current_state = GAME_RUNNING
        self.final_scores = []
        self.power_ups = []
        self.final_score = 0
        self.final_score_2 = 0
        self.play_count = 0
        self.high_score = 0
        self.game_over = False
        self.power_up = False
        self.power_up_2 = False
        self.power_up_timer = POWER_UP_TIMER
        self.power_up_timer_2 = POWER_UP_TIMER
        self.shoot_timer = DEFAULT_SHOOT_TIMER
        self.shoot_timer_2 = DEFAULT_SHOOT_TIMER
        self.pause = False

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        if self.current_state == 4:
            pyglet.app.exit()
            arcade.close_window()
        elif self.quit:
            self.draw_quit()
            self.game_over_player.pause()
        else:
            if self.current_state == GAME_RUNNING:
                arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                              SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

                if self.play_sound:
                    self.game_over_player.pause()
                    self.media_player.seek(0)
                    self.media_player.play()
                    self.play_sound = False

                self.draw_score()
                self.draw_health()
                if self.ship.alive:
                    self.ship.draw()
                if self.player_two.alive:
                    self.player_two.draw()
                self.draw_speed()

                for bullet in self.bullets:
                    bullet.draw()

                for asteroid in self.asteroids:
                    asteroid.draw()

                for enemy in self.enemies:
                    enemy.draw()

                for power in self.power_ups:
                    power.draw()

                if self.pause:
                    self.media_player.pause()
                    self.draw_pause()

            elif self.current_state == TRANSITION:
                self.final_scores.append(self.score)
                self.final_scores.append(self.score_2)
                self.get_final_value()
                self.play_game_over = True

            elif self.current_state == GAME_OVER:
                if self.play_game_over:
                    self.game_over_player.seek(0)
                    self.media_player.pause()
                    self.game_over_player.play()
                    self.play_game_over = False
                self.draw_final()

            if self.mute:
                self.draw_mute()

    def get_final_value(self):
        """
        Gets final value, stores into list, changes current state to game over.
        """
        self.final_score = self.final_scores[int(self.play_count * 2)]
        self.final_score_2 = self.final_scores[int(self.play_count * 2 + 1)]
        self.current_state = GAME_OVER

    def get_high_score(self):
        """
        Calculates high score. Sets self.high_score to this value.
        """
        high_score = -1000
        for score in self.final_scores:
            if score > high_score:
                high_score = score
        self.high_score = high_score

    def draw_final(self):
        """
        Displays game over screen, including final score(s), high score, and times played.
        """
        arcade.set_background_color(arcade.color.BLACK)
        self.get_high_score()
        score_text = "Final Score P1: {}        Final Score P2: {}".format(self.final_score, self.final_score_2)
        high_text = "High Score: {}".format(self.high_score)
        other_text = "Total times played: {}".format(self.play_count + 1)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text("GAME OVER!", start_x=SCREEN_WIDTH / 5 + 47, start_y=(SCREEN_HEIGHT / 2), font_size=72,
                         color=arcade.color.WHITE)
        arcade.draw_text(high_text, start_x=(SCREEN_WIDTH - 150), start_y=start_y, font_size=12,
                         color=arcade.color.WHITE)
        arcade.draw_text("Press Enter to continue", start_x=(SCREEN_WIDTH / 2 - 155), start_y=(SCREEN_HEIGHT / 2) - 35,
                         font_size=24, color=arcade.color.WHITE)
        arcade.draw_text("Press 'Q' to quit", start_x=(SCREEN_WIDTH / 2 - 110), start_y=(SCREEN_HEIGHT / 2) - 70,
                         font_size=24, color=arcade.color.WHITE)
        arcade.draw_text(other_text, start_x=10, start_y=12, font_size=12,
                         color=arcade.color.WHITE)
        if self.pause:
            arcade.draw_text("Music Paused", start_x=SCREEN_WIDTH - 110, start_y=12, font_size=12,
                             color=arcade.color.WHITE)

    def draw_speed(self):
        """
        Puts the current speed on the screen
        """
        text_1 = "P1 Speed: {}".format(self.ship.speed)
        text_2 = "P2 Speed: {}".format(self.player_two.speed)
        start_x_1 = SCREEN_WIDTH / 2 - 190
        start_x_2 = SCREEN_WIDTH / 2 - 70
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(text_1, start_x=start_x_1, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text(text_2, start_x=start_x_2, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score P1: {}      Score P2: {}".format(self.score, self.score_2)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_health(self):
        """
        Puts health left on screen.
        """
        health = "Health P1: {}%        Health P2: {}%".format(self.ship.health, self.player_two.health)
        start_x = SCREEN_WIDTH - 270
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(health, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_pause(self):
        """
        Draws pause.
        """
        text = "PAUSE"
        start_x = SCREEN_WIDTH / 2 - 140
        start_y = SCREEN_HEIGHT / 2
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=76, color=arcade.color.WHITE)
        restart = "Press 'R' to restart"
        x = SCREEN_WIDTH / 2 - 134
        y = SCREEN_HEIGHT / 2 - 40
        arcade.draw_text(restart, start_x=x, start_y=y, font_size=26, color=arcade.color.WHITE)
        quit_game = "Press 'Q' to quit"
        y_quit = SCREEN_HEIGHT / 2 - 80
        arcade.draw_text(quit_game, start_x=x + 19, start_y=y_quit, font_size=26, color=arcade.color.WHITE)

    def draw_mute(self):
        """
        Draws mute.
        """
        text = "Audio Muted"
        start_x = SCREEN_WIDTH / 2 - 30
        start_y = 12
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_quit(self):
        text = "Are you sure you want to quit?"
        start_x = 10
        start_y = SCREEN_HEIGHT / 2
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=58, color=arcade.color.WHITE)
        response = "Y for yes, N for no"
        x = SCREEN_WIDTH / 2 - 134
        y = SCREEN_HEIGHT / 2 - 40
        arcade.draw_text(response, start_x=x, start_y=y, font_size=24, color=arcade.color.WHITE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        if not self.pause:
            self.check_keys()
            self.check_collisions()
            self.check_off_screen()
            self.ship.advance()
            self.player_two.advance()
            self.create_asteroids()
            self.check_death()

            if random.randint(1, ENEMY_SHIP_SPAWN_TIMER) == 1:
                enemy = AggressiveEnemyShip()
                enemy.center.new_location(self.ship, self.player_two)
                self.enemies.append(enemy)

            if random.randint(1, ENEMY_FREIGHTER_SPAWN_TIMER) == 1:
                enemy = EnemyFreighter()
                enemy.center.new_location(self.ship, self.player_two)
                self.enemies.append(enemy)

            for asteroid in self.asteroids:
                asteroid.advance()

            for bullet in self.bullets:
                bullet.advance()

            # Power ups will disappear after a while
            for power in self.power_ups:
                if power.timer > 0:
                    power.timer -= 1
                    power.advance()
                else:
                    power.alive = False

            for enemy in self.enemies:
                if enemy.health > 0:
                    if enemy.type == 1:
                        self.enemy_attack(enemy)
                    enemy.advance()
                else:
                    enemy.alive = False

            if self.ship.health > SHIP_BASE_HEALTH:
                self.ship.health = SHIP_BASE_HEALTH

            if self.player_two.health > SHIP_BASE_HEALTH:
                self.player_two.health = SHIP_BASE_HEALTH

            if self.power_up:
                if self.power_up_timer > 1:
                    self.shoot(self.ship)
                    self.power_up_timer -= 1
                else:
                    self.power_up = False
                    self.power_up_timer = POWER_UP_TIMER

            if self.power_up_2:
                if self.power_up_timer_2 > 1:
                    self.shoot(self.player_two)
                    self.power_up_timer_2 -= 1
                else:
                    self.power_up_2 = False
                    self.power_up_timer_2 = POWER_UP_TIMER

    def enemy_attack(self, enemy):
        """
        Determines which player the enemy should shoot at, and shoots at the player.
        :param enemy:
        """
        x_diff_s = enemy.center.x - self.ship.center.x
        y_diff_s = enemy.center.y - self.ship.center.y
        x_diff_2 = enemy.center.x - self.player_two.center.x
        y_diff_2 = enemy.center.y - self.player_two.center.y
        ship_distance = math.sqrt((x_diff_s ** 2) + (y_diff_s ** 2))
        p2_distance = math.sqrt((x_diff_2 ** 2) + (y_diff_2 ** 2))
        angle = 0
        target = self.ship
        if ship_distance > p2_distance:
            if self.player_two.alive:
                angle = math.atan2(y_diff_2, x_diff_2)
                target = self.player_two
            else:
                angle = math.atan2(y_diff_s, x_diff_s)
        elif ship_distance < p2_distance:
            if self.ship.alive:
                angle = math.atan2(y_diff_s, x_diff_s)
            else:
                angle = math.atan2(y_diff_2, x_diff_2)
                target = self.player_two

        enemy.angle = math.degrees(angle) - 180
        enemy.set_target(target)

        if random.randint(1, 20) == 1 and (self.ship.alive or self.player_two.alive):
            self.shoot(enemy)

    def check_death(self):
        """
        Checks to see whether a ship or both ships have died, and performs the appropriate actions.
        """
        if self.ship.health <= 0:
            self.ship.health = 0
            self.ship.alive = False
            self.ship.velocity.dx = 0
            self.ship.velocity.dy = 0
            if self.player_two.health <= 0:
                self.player_two.health = 0
                self.player_two.alive = False
                if not self.game_over:
                    self.current_state = TRANSITION
                    self.game_over = True

        elif self.player_two.health <= 0:
            self.player_two.health = 0
            self.player_two.alive = False
            self.player_two.velocity.dx = 0
            self.player_two.velocity.dy = 0
            if self.ship.health <= 0:
                self.ship.health = 0
                self.ship.alive = False
                if not self.game_over:
                    self.current_state = TRANSITION
                    self.game_over = True

    def create_asteroids(self):
        """
        Creates new asteroids.
        """
        if self.initial_rocks > 0:
            asteroid = LargeAsteroid()
            asteroid.center.new_location(self.ship, self.player_two)
            self.asteroids.append(asteroid)
            self.initial_rocks -= 1
        else:
            rand = random.randint(1, ASTEROID_SPAWN_TIMER)
            if rand == 1:
                asteroid = LargeAsteroid()
                asteroid.center.new_location(self.ship, self.player_two)
                self.asteroids.append(asteroid)
            else:
                pass

    def check_collisions(self):
        """
        Checks to see if bullets have hit asteroids, and checks other collisions as well.
        Updates scores and removes dead items.
        """

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if self.is_collision(bullet, asteroid):
                    bullet.alive = False
                    if bullet.type == 1:
                        self.score += asteroid.hit(self.power_up)
                    elif bullet.type == 3:
                        self.score_2 += asteroid.hit(self.power_up_2)
                    self.asteroids = asteroid.split(self.asteroids)

        for asteroid in self.asteroids:
            if self.is_collision(asteroid, self.ship):
                self.ship.health -= asteroid.hit_ship(self.power_up)
                self.score -= asteroid.damage(self.power_up)
                self.asteroids = asteroid.split(self.asteroids)
            if self.is_collision(asteroid, self.player_two):
                self.player_two.health -= asteroid.hit_ship(self.power_up_2)
                self.score_2 -= asteroid.damage(self.power_up_2)
                self.asteroids = asteroid.split(self.asteroids)

        for enemy in self.enemies:
            if self.is_collision(enemy, self.ship):
                if not self.power_up:
                    self.ship.health -= 5
                enemy.health -= 10
            if self.is_collision(enemy, self.player_two):
                if not self.power_up_2:
                    self.player_two.health -= 5
                enemy.health -= 10

        for bullet in self.bullets:
            for enemy in self.enemies:
                if self.is_collision(bullet, enemy):
                    if bullet.type == 1:
                        self.ship, self.score, bullet, enemy = self.hit_enemy(self.ship, self.score, bullet, enemy)
                    elif bullet.type == 3:
                        self.player_two, self.score_2, bullet, enemy = self.hit_enemy(self.player_two, self.score_2,
                                                                                      bullet, enemy)

        for bullet in self.bullets:
            for power in self.power_ups:
                if self.is_collision(bullet, power):
                    if bullet.type == 1:
                        power.alive = False
                        self.ship.alive = True
                        self.power_up = True
                        self.power_up_timer = POWER_UP_TIMER
                        self.ship.health = SHIP_BASE_HEALTH
                    elif bullet.type == 3:
                        power.alive = False
                        self.player_two.alive = True
                        self.power_up_2 = True
                        self.power_up_timer_2 = POWER_UP_TIMER
                        self.player_two.health = SHIP_BASE_HEALTH
                    bullet.alive = False

        for power in self.power_ups:
            if self.is_collision(power, self.player_two):
                power.alive = False
                self.player_two.alive = True
                self.power_up_2 = True
                self.power_up_timer_2 = POWER_UP_TIMER
                self.player_two.health = SHIP_BASE_HEALTH
            if self.is_collision(power, self.ship):
                power.alive = False
                self.ship.alive = True
                self.power_up = True
                self.power_up_timer = POWER_UP_TIMER
                self.ship.health = SHIP_BASE_HEALTH

        for bullet in self.bullets:
            if bullet.type == 2:
                if self.is_collision(bullet, self.ship):
                    if not self.power_up:
                        bullet.alive = False
                        self.ship.health -= 5
                    else:
                        bullet.alive = False
                if self.is_collision(bullet, self.player_two):
                    if not self.power_up_2:
                        bullet.alive = False
                        self.player_two.health -= 3
                    else:
                        bullet.alive = False

        for bullet1 in self.bullets:
            for bullet2 in self.bullets:
                if bullet1.type != bullet2.type:
                    if self.is_collision(bullet1, bullet2):
                        bullet1.alive = False
                        bullet2.alive = False

        self.cleanup_zombies()

    def is_collision(self, object_1, object_2):
        """
        Checks to see whether a collision occurred.
        :param object_1:
        :param object_2:
        :return:
        """
        if object_1.alive and object_2.alive:
            too_close = object_1.radius + object_2.radius
            if (abs(object_1.center.x - object_2.center.x) < too_close and
                abs(object_1.center.y - object_2.center.y) < too_close):
                return True
            else:
                return False

    def hit_enemy(self, ship, score, bullet, enemy):
        """
        Performs all necessary actions when an enemy is hit.
        :param ship:
        :param score:
        :param bullet:
        :param enemy:
        """
        if ship.alive:
            if enemy.health <= 0:
                if enemy.type == 1:
                    ship.health += 10
                    score += 20
                else:
                    score += 50
                enemy.alive = False
        bullet.alive = False
        enemy.health -= 15
        return ship, score, bullet, enemy

    def cleanup_zombies(self):
        """
        Removes any dead bullets, asteroids, enemies, etc. from the list.
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

        for enemy in self.enemies:
            if not enemy.alive:
                if enemy.type == 2:
                    self.create_power_up(enemy)
                self.enemies.remove(enemy)

        for power in self.power_ups:
            if not power.alive:
                self.power_ups.remove(power)

    def create_power_up(self, enemy):
        """
        Creates a new Power up.
        :param enemy: Imports an enemy
        """
        power = PowerUp()
        power.center.x = enemy.center.x
        power.center.y = enemy.center.y
        power.velocity.dx = enemy.velocity.dx + 2
        power.velocity.dy = enemy.velocity.dy
        self.power_ups.append(power)

    def check_off_screen(self):
        """
        Checks to see if bullets or asteroids have left the screen
        and if so, removes them from their lists.
        """
        self.ship.check_off_screen()
        self.player_two.check_off_screen()

        for bullet in self.bullets:
            bullet.check_off_screen()

        for asteroid in self.asteroids:
            asteroid.check_off_screen()

        for enemy in self.enemies:
            enemy.check_off_screen()

        for power in self.power_ups:
            power.check_off_screen()

    def set_alpha(self, alpha):
        """
        Sets Alpha for all objects on screen.
        :param alpha:
        """
        for asteroid in self.asteroids:
            asteroid.alpha = alpha
        for bullet in self.bullets:
            bullet.alpha = alpha
        for enemy in self.enemies:
            enemy.alpha = alpha
        self.ship.alpha = alpha
        self.player_two.alpha = alpha

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            m = 1
            if arcade.key.DOWN in self.held_keys:
                m = 2
            self.ship.turn_left(m)

        if arcade.key.RIGHT in self.held_keys:
            m = 1
            if arcade.key.DOWN in self.held_keys:
                m = 2
            self.ship.turn_right(m)

        if arcade.key.UP in self.held_keys:
            self.ship.accelerate()

        if arcade.key.DOWN in self.held_keys:
            self.ship.decelerate()

        if arcade.key.A in self.held_keys:
            m = 1
            if arcade.key.S in self.held_keys:
                m = 2
            self.player_two.turn_left(m)

        if arcade.key.D in self.held_keys:
            m = 1
            if arcade.key.S in self.held_keys:
                m = 2
            self.player_two.turn_right(m)

        if arcade.key.W in self.held_keys:
            self.player_two.accelerate()

        if arcade.key.S in self.held_keys:
            self.player_two.decelerate()

        # Machine gun mode...
        if self.ship.alive:
            if arcade.key.SPACE in self.held_keys:
                if self.shoot_timer == DEFAULT_SHOOT_TIMER and not self.mute:
                    arcade.play_sound(self.millennium_falcon_blast)
                if self.shoot_timer >= 0:
                    self.shoot(self.ship)
                    self.shoot_timer -= 1
                else:
                    if self.shoot_timer <= -(DEFAULT_SHOOT_TIMER * 3):
                        self.shoot_timer = DEFAULT_SHOOT_TIMER
                    else:
                        self.shoot_timer -= 1

        if self.player_two.alive:
            if arcade.key.GRAVE in self.held_keys:
                if self.shoot_timer_2 == DEFAULT_SHOOT_TIMER and not self.mute:
                    arcade.play_sound(self.x_wing_blast)
                if self.shoot_timer_2 >= 0:
                    self.shoot(self.player_two)
                    self.shoot_timer_2 -= 1
                else:
                    if self.shoot_timer_2 <= -(DEFAULT_SHOOT_TIMER * 3):
                        self.shoot_timer_2 = DEFAULT_SHOOT_TIMER
                    else:
                        self.shoot_timer_2 -= 1

    def shoot(self, ship):
        """
        Fires bullets from a ship.
        :param ship:
        """
        if not self.pause:
            bullet = ""
            distance = 80
            if ship.type == 0:
                bullet = Laser()
            elif ship.type == 1:
                bullet = EnemyLaser()
                if not self.mute:
                    arcade.play_sound(self.tie_fighter_blast)
                distance = 50
            elif ship.type == 2:
                bullet = LaserTwo()
            if ship.type != 1:
                if self.power_up or self.power_up_2:
                    bullet.image = "PURPLE_LASER.png"
                    bullet.length = POWER_UP_BULLET_LENGTH
                    bullet.width = POWER_UP_BULLET_WIDTH
                    distance = 100
            bullet.center.x = ship.center.x + math.cos(math.radians(ship.angle)) * distance
            bullet.center.y = ship.center.y + math.sin(math.radians(ship.angle)) * distance
            bullet.angle = ship.angle
            bullet.fire(ship)
            self.bullets.append(bullet)

    def reset(self):
        """
        Resets values to previous state for a new game.
        """
        self.held_keys = set()
        self.ship = Ship()
        self.player_two = PlayerTwoShip()
        self.asteroids = []
        self.bullets = []
        self.initial_rocks = INITIAL_ROCK_COUNT
        self.enemies = []
        self.power_ups = []
        self.score = 0
        self.score_2 = 0
        self.final_score = 0
        self.final_score_2 = 0
        self.power_up = False
        self.power_up_2 = False
        self.power_up_timer = POWER_UP_TIMER
        self.power_up_timer_2 = POWER_UP_TIMER
        self.shoot_timer = DEFAULT_SHOOT_TIMER
        self.shoot_timer_2 = DEFAULT_SHOOT_TIMER
        if self.game_over:
            self.play_count += 1
        self.play_sound = True
        self.game_over = False

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if not self.game_over and self.pause:
            if key == arcade.key.R:
                self.reset()
                self.pause = False

        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                self.shoot(self.ship)

        if self.player_two.alive:
            self.held_keys.add(key)

            if key == arcade.key.GRAVE:
                self.shoot(self.player_two)

        if self.current_state == GAME_OVER:
            if key == arcade.key.ENTER:
                self.reset()
                self.current_state = GAME_RUNNING

        if key == arcade.key.P:
            if not self.pause:
                self.pause = True
                if not self.mute:
                    arcade.play_sound(self.pause_sound)

                if not self.game_over:
                    self.set_alpha(.5)
                else:
                    self.game_over_player.pause()
            else:
                self.pause = False

                if not self.game_over:
                    self.media_player.play()
                    self.set_alpha(1)
                else:
                    self.game_over_player.play()

        if key == arcade.key.Q:
            if self.pause:
                self.quit = True
            if self.game_over:
                self.quit = True

        if self.quit:
            if key == arcade.key.Y:
                self.current_state = 4
            if key == arcade.key.N:
                self.quit = False
                if not self.pause:
                    self.game_over_player.play()

        if key == arcade.key.M:
            if not self.mute:
                self.media_player.volume = 0
                self.game_over_player.volume = 0
                self.mute = True
            else:
                self.media_player.volume = 1
                self.game_over_player.volume = 1
                self.mute = False

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


def main():
    """
    Creates the game and starts it going
    """
    Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        pyglet.app.run()
        arcade.run()
    except AttributeError:
        print("Thanks for playing!")


if __name__ == "__main__":
        main()
