import arcade
import math
import random
from abc import ABC, abstractmethod
import pyglet

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

BULLET_LENGTH = 35
BULLET_WIDTH = 25
BULLET_SPEED = 10
BULLET_LIFE = 60

POWER_UP_BULLET_LENGTH = 65
POWER_UP_BULLET_WIDTH = 20

ENEMY_BULLET_LENGTH = 65
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

POWER_UP_WIDTH = 40
POWER_UP_RADIUS = 50

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

INSTRUCTIONS = 0
GAME_RUNNING = 1
TRANSITION = 2
GAME_OVER = 3
QUIT = 4

MAX_SPEED = 15
SPAWN_DISTANCE = 200

# Types
P1 = 0
P2 = 1
ENEMY = 2
POWER = 3
ENEMY_FREIGHTER = 4


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


def is_collision(object_1, object_2):
    """
    Checks to see whether a collision occurred.
    :param object_1:
    :param object_2:
    :return: Bool
    """
    if object_1.alive and object_2.alive:
        too_close = object_1.radius + object_2.radius
        if (abs(object_1.center.x - object_2.center.x) < too_close and
                abs(object_1.center.y - object_2.center.y) < too_close):
            return True
        else:
            return False


class EndGame(Exception):
    def __str__(self):
        pass


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
        self.image = "Files/Millennium_Falcon.png"
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

    def check_off_screen(self, game_data):
        """
        Checks to see whether a flying object is off the screen.
        Relocates it on the other side.
        """
        if self.center.x <= 0:
            self.center.x = int(game_data[12]) - 1
        elif self.center.x >= int(game_data[12]):
            self.center.x = 1
        elif self.center.y <= 0:
            self.center.y = int(game_data[13]) - 1
        elif self.center.y >= int(game_data[13]):
            self.center.y = 1


class Asteroid(FlyingObject, ABC):
    """
    Asteroid class inherits from the Flying Object class. This class will be used to model other
    classes for different types of asteroids.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/meteorGrey_big1.png"
        self.radius = BIG_ROCK_RADIUS
        self.spin = BIG_ROCK_SPIN
        self.velocity_angle = random.uniform(0, 359)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.velocity_angle)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.velocity_angle)) * self.speed
        self._hit = {0: 20, 1: 10}
        self._damage = {0: 5, 1: 0}
        self._hit_ship = {0: BIG_ROCK_DAMAGE, 1: 0}

    def rotate(self):
        """
        Changes angle of asteroid depending on self.spin value.
        """
        self.angle += self.spin

    def advance(self):
        self.rotate()
        super().advance()

    @abstractmethod
    def split(self, asteroids, game_data):
        """
        Will be responsible for splitting up an asteroid after getting hit.
        :param asteroids: list containing all asteroids in game class.
        :param game_data: game data from loaded file
        :return: asteroids list
        """
        pass

    def hit(self, power):
        """
        Determines score to return when an asteroid is hit by a player
        :param power: bool for player's power up state
        :return: a score to be added to player's score
        """
        if power:
            return self._hit[0]
        else:
            return self._hit[1]

    def damage(self, power):
        """
        Determines amount that will be taken from a player's score when they hit an asteroid.
        :param power: bool for player's power up state
        :return: a score to be subtracted from player's score
        """
        if not power:
            return self._damage[0]
        else:
            return self._damage[1]

    def hit_ship(self, power):
        """
        Determines how much health a player will lose when they hit an asteroid.
        :param power: bool for player's power up state
        :return: an amount to be subtracted from player's health
        """
        if not power:
            return self._hit_ship[0]
        else:
            return self._hit_ship[1]


class LargeAsteroid(Asteroid):
    """
    Large Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()

    def split(self, asteroids, game_data):
        """
        Splits up large asteroid into smaller asteroids.
        :param asteroids: list containing all asteroids in game class.
        :param game_data: game data from loaded file
        :return: asteroids list
        """
        med_1 = MediumAsteroid()
        med_1.image = game_data[17]
        med_1 = set_new_asteroid(med_1, self, 0, 2)
        med_2 = MediumAsteroid()
        med_2.image = game_data[17]
        med_2 = set_new_asteroid(med_2, self, 0, -2)
        small_1 = SmallAsteroid()
        small_1.image = game_data[18]
        small_1 = set_new_asteroid(small_1, self, 5, 0)
        asteroids.extend([med_1, med_2, small_1])
        self.alive = False
        return asteroids


class MediumAsteroid(Asteroid):
    """
    Medium Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/meteorGrey_med1.png"
        self.radius = MEDIUM_ROCK_RADIUS
        self.spin = MEDIUM_ROCK_SPIN
        self._hit = {0: 10, 1: 5}
        self._damage = {0: 3, 1: 0}
        self._hit_ship = {0: MEDIUM_ROCK_DAMAGE, 1: 0}

    def split(self, asteroids, game_data):
        """
        Splits up medium asteroid into smaller asteroids.
        :param asteroids: list containing all asteroids in game class.
        :param game_data: game data from loaded file
        :return: asteroids list
        """
        small_1 = SmallAsteroid()
        small_1.image = game_data[18]
        small_1 = set_new_asteroid(small_1, self, 1.5, 1.5)
        small_2 = SmallAsteroid()
        small_2.image = game_data[18]
        small_2 = set_new_asteroid(small_2, self, -1.5, -1.5)
        asteroids.extend([small_1, small_2])
        self.alive = False
        return asteroids


class SmallAsteroid(Asteroid):
    """
    Small Asteroid class. Inherits from the Asteroid class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/meteorGrey_small1.png"
        self.radius = SMALL_ROCK_RADIUS
        self.spin = SMALL_ROCK_SPIN
        self._hit = {0: 5, 1: 2}
        self._damage = {0: 1, 1: 0}
        self._hit_ship = {0: SMALL_ROCK_DAMAGE, 1: 0}

    def split(self, asteroids, game_data):
        """
        Sets alive to false, returns asteroids.
        :param asteroids: list containing all asteroids in game class.
        :param game_data: game data from loaded file
        :return: asteroids list
        """
        self.alive = False
        return asteroids


class Laser(FlyingObject):
    """
    Laser class, inherits from Flying Object class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/RED_LASER.png"
        self.center.x = 0
        self.center.y = 0
        self.radius = 25
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED
        self.type = P1
        self.length = 35
        self.width = 25

    def advance(self):
        """
        Moves bullet until the bullet dies.
        """
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


class PowerUp(FlyingObject):
    """
    Power up class, inherits from Flying Object class. Will cause a power up for user that
    comes into contact with it.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/REBEL.png"
        self.radius = POWER_UP_RADIUS
        self.timer = POWER_UP_ALIVE_TIMER


class ShipBase(FlyingObject):
    """
    Ship base class.
    """
    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.health = SHIP_BASE_HEALTH
        self.thrust = SHIP_THRUST_AMOUNT
        self.turn = SHIP_TURN_AMOUNT
        self.center.x = SCREEN_WIDTH/2
        self.center.y = (5 * SCREEN_HEIGHT)/8
        self.type = P1
        self.bullet_distance = 80
        self.bullet_length = BULLET_LENGTH
        self.bullet_width = BULLET_WIDTH

    def shoot(self, image):
        """
        Shoots bullets from ship, returns bullet object
        :param image: bullet image
        :return: bullet
        """
        bullet = Laser()
        bullet.type = self.type
        bullet.image = image
        bullet.length = self.bullet_length
        bullet.width = self.bullet_width
        bullet.center.x = self.center.x + math.cos(math.radians(self.angle)) * self.bullet_distance
        bullet.center.y = self.center.y + math.sin(math.radians(self.angle)) * self.bullet_distance
        bullet.angle = self.angle
        bullet.fire(self)
        return bullet


class Ship(ShipBase):
    """
    Ship class, inherits from Flying Object class. This is the ship that the user will
    control in the game class.
    """
    def __init__(self):
        super().__init__()

    def accelerate(self, max_speed):
        """
        Increases speed when triggered.
        :param max_speed: Max speed of ship
        """
        if abs(self.velocity.dx) < max_speed:
            self.velocity.dx += math.cos(math.radians(self.angle)) * self.thrust
        if abs(self.velocity.dy) < max_speed:
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
        :return: speed
        """
        speed = math.sqrt((self.velocity.dx ** 2) + (self.velocity.dy ** 2))
        speed = round(speed*4)/4
        return speed

    def set_power_up(self):
        """
        Changes settings of bullets for power up
        """
        self.bullet_length = POWER_UP_BULLET_LENGTH
        self.bullet_width = POWER_UP_BULLET_WIDTH
        self.bullet_distance = 100

    def reset_bullet(self):
        """
        Resets bullet settings after a power up
        """
        self.bullet_distance = 80
        self.bullet_length = BULLET_LENGTH
        self.bullet_width = BULLET_WIDTH


class PlayerTwoShip(Ship):
    """
    Player Two Ship class, inherits from ship class. This is the ship used by
    player two in the game class.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/X-Wing.png"
        self.center.x = SCREEN_WIDTH/2
        self.center.y = (3 * SCREEN_HEIGHT)/8
        self.type = P2


class AggressiveEnemyShip(ShipBase):
    """
    Class for Aggressive enemy ship, inherits from ship class. This ship will attack the player(s).
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/Tie_Fighter.png"
        self.radius = ENEMY_SHIP_RADIUS
        self.health = ENEMY_SHIP_HEALTH
        self.enemy_speed = ENEMY_SHIP_SPEED
        self.type = ENEMY
        self.outside_ship = None
        self.multiplier = random.uniform(.5, 1)
        self.bullet_distance = 50
        self.bullet_length = ENEMY_BULLET_LENGTH
        self.bullet_width = ENEMY_BULLET_WIDTH

    def set_target(self, ship):
        """
        Sets target as ship that is closest.
        :param ship: outside ship input
        """
        self.outside_ship = ship

    def set_speed(self, actual_dist):
        """
        Sets speed of enemies.
        :param actual_dist: distance from target
        """
        self.enemy_speed = (actual_dist / 100) * self.multiplier

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

    def hit(self, ship, score):
        """
        Completes appropriate actions when an aggressive enemy is hit by a player's bullet.
        :param ship: The ship that shot the bullet that hit the enemy
        :param score: The score for the ship that shot
        :return: ship, score
        """
        self.health -= 15
        if self.health <= 0:
            ship.health += 10
            score += 20
            self.alive = False
        return ship, score


class EnemyFreighter(ShipBase):
    """
    Large enemy ship, inherits from ship class. This ship is large and has lots of health.
    When the user destroys it, a power up will appear.
    """
    def __init__(self):
        super().__init__()
        self.image = "Files/Imperial_Star_Destroyer.png"
        self.radius = ENEMY_FREIGHTER_RADIUS
        self.health = ENEMY_FREIGHTER_HEALTH
        self.type = ENEMY_FREIGHTER
        self.velocity.dx = random.uniform(-1, 1)
        self.velocity.dy = random.uniform(-1, 1)
        self.length = 200
        self.width = 75

    def draw(self):
        """
        Changes draw to use length and width.
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.length, self.width, texture,
                                      self.angle, self.alpha)

    def hit(self, ship, score):
        """
        Completes appropriate actions when an enemy freighter is hit by a player's bullet.
        :param ship: The ship that shot the bullet that hit the enemy
        :param score: The score for the ship that shot
        :return: ship, score
        """
        self.health -= 15
        if self.health <= 0:
            score += 50
            self.alive = False
        return ship, score


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height, game_data):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.media_player = pyglet.media.Player()
        self.game_over_sound = arcade.load_sound(str(game_data[0]))
        self.sound = pyglet.media.load(str(game_data[1]))
        self.play_sound = True
        self.play_game_over = False
        self.game_over_player = pyglet.media.Player()
        self.game_over_player.queue(self.game_over_sound)
        self.sound_loop = pyglet.media.SourceGroup(self.sound.audio_format, None)
        self.sound_loop.loop = True
        self.sound_loop.queue(self.sound)
        self.blast = {P1: arcade.load_sound(str(game_data[4])), P2: arcade.load_sound(str(game_data[3])),
                      ENEMY: arcade.load_sound(str(game_data[2]))}
        self.pause_sound = arcade.load_sound(str(game_data[5]))
        self.background = arcade.load_texture(str(game_data[6]))
        self.media_player.queue(self.sound_loop)
        self.mute = False
        self.quit = False
        self.power_up_sound = pyglet.media.load(str(game_data[28]))
        self.power_up_loop = pyglet.media.SourceGroup(self.power_up_sound.audio_format, None)
        self.power_up_loop.loop = True
        self.power_up_loop.queue(self.power_up_sound)
        self.power_up_player = pyglet.media.Player()
        self.power_up_player.queue(self.power_up_loop)
        self.play_power_up = False

        self.held_keys = set()

        # I made all of these variables...
        self.ship = {P1: Ship(), P2: PlayerTwoShip()}
        self.ship_image = {P1: game_data[14], P2: game_data[15]}
        for s in self.ship:
            self.ship[s].image = self.ship_image[s]
        self.asteroids = []
        self.bullets = []
        self.initial_rocks = int(game_data[7])
        self.enemies = []
        self.score = {P1: 0, P2: 0}
        self.current_state = INSTRUCTIONS
        self.final_scores = []
        self.power_ups = []
        self.final_score = {P1: 0, P2: 0}
        self.play_count = 0
        self.high_score = 0
        self.game_over = False
        self.power_up = {P1: False, P2: False}
        self.power_up_timer = {P1: int(game_data[8]), P2: int(game_data[8])}
        self.shoot_timer = {P1: int(game_data[10]), P2: int(game_data[10])}
        self.pause = False

        self.game_data = game_data
        self.screen_width = width
        self.screen_height = height
        self._initial_rocks = game_data[7]
        self._power_up_timer = game_data[8]
        self._power_up_alive = game_data[9]
        self._shoot_timer = game_data[10]
        self._max_speed = game_data[11]
        self.a_enemy_image = game_data[19]
        self.b_enemy_image = game_data[20]
        self.bullet_image = {P1: game_data[21], P2: game_data[22], ENEMY: game_data[23], POWER: game_data[24]}
        self.power_image = game_data[25]
        self.asteroid_image = self.game_data[16]
        self.b_enemy_length = game_data[26]
        self.b_enemy_width = game_data[27]
        self.hide_hud = False

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()

        if self.current_state == QUIT:
            raise EndGame()

        elif self.quit:
            self.draw_quit()
            self.game_over_player.pause()

        else:
            if self.current_state == INSTRUCTIONS:
                self.draw_instructions()

            if self.current_state == GAME_RUNNING:
                arcade.draw_texture_rectangle(self.screen_width // 2, self.screen_height // 2,
                                              self.screen_width, self.screen_height, self.background)

                if self.play_sound:
                    self.game_over_player.pause()
                    self.media_player.seek(0)
                    self.media_player.play()
                    self.play_sound = False

                if self.play_power_up:
                    if not self.power_up[0] and not self.power_up[1]:
                        self.power_up_player.pause()
                        self.media_player.play()
                        self.play_power_up = False

                if not self.play_power_up:
                    if self.power_up[0] or self.power_up[1]:
                        self.media_player.pause()
                        self.power_up_player.seek(0)
                        self.power_up_player.play()
                        self.play_power_up = True

                if not self.hide_hud:
                    self.draw_score()
                    self.draw_health()
                    self.draw_speed()

                for player in self.ship:
                    if self.ship[player].alive:
                        self.ship[player].draw()

                for bullet in self.bullets:
                    bullet.draw()

                for asteroid in self.asteroids:
                    asteroid.draw()

                for enemy in self.enemies:
                    enemy.draw()

                for power in self.power_ups:
                    power.draw()

                if self.pause:
                    if not self.power_up[0] and not self.power_up[1]:
                        self.media_player.pause()
                    else:
                        self.power_up_player.pause()
                    self.draw_pause()

            elif self.current_state == TRANSITION:
                self.final_score[P1] = self.score[P1]
                self.final_score[P2] = self.score[P2]
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
        self.final_scores.extend([self.final_score[P1], self.final_score[P2]])
        self.current_state = GAME_OVER

    def get_high_score(self):
        """
        Calculates high score. Sets self.high_score to this value.
        """
        self.high_score = max(self.final_scores)

    def draw_final(self):
        """
        Displays game over screen, including final score(s), high score, and times played.
        """
        arcade.set_background_color(arcade.color.BLACK)
        self.get_high_score()
        score_text = "Final Score P1: {}        Final Score P2: {}".format(self.final_score[P1], self.final_score[P2])
        high_text = "High Score: {}".format(self.high_score)
        other_text = "Total times played: {}".format(self.play_count + 1)
        start_x = 10
        start_y = self.screen_height - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text("GAME OVER!", start_x=self.screen_width / 5 + 47, start_y=(self.screen_height / 2),
                         font_size=72, color=arcade.color.WHITE)
        arcade.draw_text(high_text, start_x=(self.screen_width - 150), start_y=start_y, font_size=12,
                         color=arcade.color.WHITE)
        arcade.draw_text("Press Enter to continue", start_x=(self.screen_width/2 - 155),
                         start_y=(self.screen_height / 2) - 35, font_size=24, color=arcade.color.WHITE)
        arcade.draw_text("Press 'Q' to quit", start_x=(self.screen_width / 2 - 110),
                         start_y=(self.screen_height / 2) - 70, font_size=24, color=arcade.color.WHITE)
        arcade.draw_text(other_text, start_x=10, start_y=12, font_size=12,
                         color=arcade.color.WHITE)
        if self.pause:
            arcade.draw_text("Music Paused", start_x=self.screen_width - 110, start_y=12, font_size=12,
                             color=arcade.color.WHITE)

    def draw_speed(self):
        """
        Puts the current speed on the screen
        """
        text_1 = "P1 Speed: {}".format(self.ship[P1].speed)
        text_2 = "P2 Speed: {}".format(self.ship[P2].speed)
        start_x_1 = self.screen_width / 2 - 190
        start_x_2 = self.screen_width / 2 - 70
        start_y = self.screen_height - 20
        arcade.draw_text(text_1, start_x=start_x_1, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text(text_2, start_x=start_x_2, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score P1: {}      Score P2: {}".format(self.score[P1], self.score[P2])
        start_x = 10
        start_y = self.screen_height - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_health(self):
        """
        Puts health left on screen.
        """
        health = "Health P1: {}%        Health P2: {}%".format(self.ship[P1].health, self.ship[P2].health)
        start_x = self.screen_width - 270
        start_y = self.screen_height - 20
        arcade.draw_text(health, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_pause(self):
        """
        Draws pause.
        """
        text = "PAUSE"
        start_x = self.screen_width/2 - 140
        start_y = self.screen_height/2
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=76, color=arcade.color.WHITE)
        restart = "Press 'R' to restart"
        x = self.screen_width/2 - 134
        y = self.screen_height/2 - 40
        arcade.draw_text(restart, start_x=x, start_y=y, font_size=26, color=arcade.color.WHITE)
        quit_game = "Press 'Q' to quit"
        y_quit = self.screen_height/2 - 80
        arcade.draw_text(quit_game, start_x=x+19, start_y=y_quit, font_size=26, color=arcade.color.WHITE)

    def draw_instructions(self):
        """
        Draws instructions
        """
        arcade.draw_text("INSTRUCTIONS:", start_x=15, start_y=self.screen_height - 60,
                         font_size=50, color=arcade.color.WHITE)
        text_0 = "- The objective is to get as many points as possible. This is done by trying"
        text_1 = "  not to get hit, and destroying as many enemies as possible."
        text_2 = "- To move Player 1, use UP, DOWN, LEFT, and RIGHT. Use SPACE to shoot."
        text_3 = "- To move Player 2, use W, A, S, and D. Use the GRAVE key to shoot (`~)."
        text_4 = "- Health, speed and current score for both players are displayed at the top of the screen."
        text_5 = "- When you destroy an large enemy, you can get a power-up. These will make you"
        text_6 = "  invulnerable for a short time, and you will shoot a constant stream of bullets."
        text_7 = "- Press 'P' to pause or 'M' to mute. When paused, push 'R' to reset or 'Q' to quit."
        text_8 = "- Good luck!"
        text_9 = "Press ENTER to continue"
        arcade.draw_text(text_0, 15, self.screen_height - 100, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_1, 15, self.screen_height - 140, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_2, 15, self.screen_height - 180, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_3, 15, self.screen_height - 220, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_4, 15, self.screen_height - 260, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_5, 15, self.screen_height - 300, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_6, 15, self.screen_height - 340, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_7, 15, self.screen_height - 380, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_8, 15, self.screen_height - 420, font_size=19, color=arcade.color.WHITE)
        arcade.draw_text(text_9, 90, 65, font_size=60, color=arcade.color.WHITE)

    def draw_mute(self):
        """
        Draws mute.
        """
        text = "Audio Muted"
        start_x = self.screen_width / 2 - 30
        start_y = 12
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    def draw_quit(self):
        """
        Draws quit screen
        """
        text = "Are you sure you want to quit?"
        start_x = 10
        start_y = self.screen_height / 2
        arcade.draw_text(text, start_x=start_x, start_y=start_y, font_size=58, color=arcade.color.WHITE)
        response = "'Y' for yes, 'N' for no"
        x = self.screen_width / 2 - 130
        y = self.screen_height / 2 - 40
        arcade.draw_text(response, start_x=x, start_y=y, font_size=24, color=arcade.color.WHITE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        if not self.pause and self.current_state == GAME_RUNNING:
            self.check_keys()
            self.check_collisions()
            self.check_off_screen()
            self.ship[P1].advance()
            self.ship[P2].advance()
            self.create_asteroids()
            self.check_death()

            if random.randint(1, ENEMY_SHIP_SPAWN_TIMER) == 1:
                enemy = AggressiveEnemyShip()
                enemy.image = self.a_enemy_image
                enemy.center.new_location(self.ship[P1], self.ship[P2])
                self.enemies.append(enemy)

            if random.randint(1, ENEMY_FREIGHTER_SPAWN_TIMER) == 1:
                enemy = EnemyFreighter()
                enemy.image = self.b_enemy_image
                enemy.length = int(self.b_enemy_length)
                enemy.width = int(self.b_enemy_width)
                enemy.center.new_location(self.ship[P1], self.ship[P2])
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
                    if enemy.type != ENEMY_FREIGHTER:
                        self.enemy_attack(enemy)
                    enemy.advance()
                else:
                    enemy.alive = False

            for player in self.ship:
                if self.ship[player].health > SHIP_BASE_HEALTH:
                    self.ship[player].health = SHIP_BASE_HEALTH

            for user in self.power_up:
                if self.power_up[user] and (self.power_up_timer[user] > 0):
                    self.shoot(self.ship[user])
                    self.power_up_timer[user] -= 1
                else:
                    self.power_up[user] = False
                    self.power_up_timer[user] = int(self._power_up_timer)
                    self.ship[user].reset_bullet()

    def enemy_attack(self, enemy):
        """
        Determines which player the enemy should shoot at, and shoots at the player.
        :param enemy:
        """
        x_diff = {}
        y_diff = {}
        total_dist = {}
        for player in self.ship:
            x_diff[player] = enemy.center.x - self.ship[player].center.x
            y_diff[player] = enemy.center.y - self.ship[player].center.y
            total_dist[player] = math.sqrt((x_diff[player] ** 2) + (y_diff[player] ** 2))
        angle = 0
        target = self.ship[P1]
        if total_dist[P1] > total_dist[P2]:
            if self.ship[P2].alive:
                angle = math.atan2(y_diff[P2], x_diff[P2])
                target = self.ship[P2]
            else:
                angle = math.atan2(y_diff[P1], x_diff[P1])
        elif total_dist[P2] > total_dist[P1]:
            if self.ship[P1].alive:
                angle = math.atan2(y_diff[P1], x_diff[P1])
            else:
                angle = math.atan2(y_diff[P2], x_diff[P2])
                target = self.ship[P2]

        enemy.angle = math.degrees(angle) - 180
        enemy.set_target(target)

        if random.randint(1, 20) == 1 and (self.ship[P1].alive or self.ship[P2].alive):
            self.shoot(enemy)

    def check_death(self):
        """
        Checks to see whether a ship or both ships have died, and performs the appropriate actions.
        """
        for i in self.ship:
            if self.ship[i].health <= 0:
                self.ship[i].health = 0
                self.ship[i].alive = False
                self.ship[i].velocity.dx = 0
                self.ship[i].velocity.dy = 0
                if self.ship[abs(i-1)].health <= 0:
                    self.ship[abs(i-1)].health = 0
                    self.ship[abs(i-1)].alive = False
                    if not self.game_over:
                        self.current_state = TRANSITION
                        self.game_over = True

    def create_asteroids(self):
        """
        Creates new asteroids.
        """
        if self.initial_rocks > 0:
            asteroid = LargeAsteroid()
            asteroid.image = self.asteroid_image
            asteroid.center.new_location(self.ship[P1], self.ship[P2])
            self.asteroids.append(asteroid)
            self.initial_rocks -= 1
        else:
            rand = random.randint(1, ASTEROID_SPAWN_TIMER)
            if rand == 1:
                asteroid = LargeAsteroid()
                asteroid.image = self.asteroid_image
                asteroid.center.new_location(self.ship[P1], self.ship[P2])
                self.asteroids.append(asteroid)

    def check_collisions(self):
        """
        Checks to see if bullets have hit asteroids, and checks other collisions as well.
        Updates scores and removes dead items.
        """

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.type != ENEMY:
                    if is_collision(bullet, asteroid):
                        bullet.alive = False
                        self.score[bullet.type] += asteroid.hit(self.power_up[bullet.type])
                        self.asteroids = asteroid.split(self.asteroids, self.game_data)

        for asteroid in self.asteroids:
            for s in self.ship:
                if is_collision(asteroid, self.ship[s]):
                    self.ship[s].health -= asteroid.hit_ship(self.power_up[s])
                    self.score[s] -= asteroid.damage(self.power_up[s])
                    self.asteroids = asteroid.split(self.asteroids, self.game_data)

        for enemy in self.enemies:
            for s in self.ship:
                if is_collision(enemy, self.ship[s]):
                    if not self.power_up[s]:
                        self.ship[s].health -= 5
                    enemy.health -= 10

        for bullet in self.bullets:
            for enemy in self.enemies:
                if is_collision(bullet, enemy) and bullet.type != ENEMY:
                    t = bullet.type
                    if self.ship[t].alive:
                        bullet.alive = False
                        self.ship[t], self.score[t] = enemy.hit(self.ship[t], self.score[t])

        for bullet in self.bullets:
            for power in self.power_ups:
                if is_collision(bullet, power):
                    if bullet.type != ENEMY:
                        power.alive = False
                        self.set_power_up(bullet.type)
                        bullet.alive = False

        for power in self.power_ups:
            for s in self.ship:
                if is_collision(power, self.ship[s]):
                    power.alive = False
                    self.set_power_up(s)

        for bullet in self.bullets:
            if bullet.type == ENEMY:
                for s in self.ship:
                    if is_collision(bullet, self.ship[s]):
                        bullet.alive = False
                        if not self.power_up[s]:
                            self.ship[s].health -= 5

        for bullet1 in self.bullets:
            for bullet2 in self.bullets:
                if bullet1.type != bullet2.type:
                    if is_collision(bullet1, bullet2):
                        bullet1.alive = False
                        bullet2.alive = False

        self.cleanup_zombies()

    def set_power_up(self, s):
        """
        Sets up the conditions for powering up the appropriate ship.
        :param s: the ship that is getting a power up
        """
        self.ship[s].alive = True
        self.power_up[s] = True
        self.power_up_timer[s] = int(self._power_up_timer)
        self.ship[s].health = SHIP_BASE_HEALTH
        self.ship[s].set_power_up()

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
                if enemy.type == ENEMY_FREIGHTER:
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
        power.image = self.power_image
        power.center.x = enemy.center.x
        power.center.y = enemy.center.y
        power.velocity.dx = enemy.velocity.dx + random.uniform(-1, 1)
        power.velocity.dy = enemy.velocity.dy + random.uniform(-1, 1)
        self.power_ups.append(power)

    def check_off_screen(self):
        """
        Checks to see if bullets or asteroids have left the screen
        and if so, removes them from their lists.
        """
        for s in self.ship:
            self.ship[s].check_off_screen(self.game_data)

        for bullet in self.bullets:
            bullet.check_off_screen(self.game_data)

        for asteroid in self.asteroids:
            asteroid.check_off_screen(self.game_data)

        for enemy in self.enemies:
            enemy.check_off_screen(self.game_data)

        for power in self.power_ups:
            power.check_off_screen(self.game_data)

    def set_alpha(self, alpha):
        """
        Sets Alpha for all objects on screen.
        :param alpha: alpha input
        """
        for asteroid in self.asteroids:
            asteroid.alpha = alpha
        for bullet in self.bullets:
            bullet.alpha = alpha
        for enemy in self.enemies:
            enemy.alpha = alpha
        for s in self.ship:
            self.ship[s].alpha = alpha

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        """
        if arcade.key.LEFT in self.held_keys:
            # 'm' is a multiplier that will allow for variance in the speed at which one can turn their ship
            # This is true for all other occurrences of 'm' in this method.
            m = 1
            if arcade.key.DOWN in self.held_keys:
                m = 2
            self.ship[P1].turn_left(m)

        if arcade.key.RIGHT in self.held_keys:
            m = 1
            if arcade.key.DOWN in self.held_keys:
                m = 2
            self.ship[P1].turn_right(m)

        if arcade.key.UP in self.held_keys:
            self.ship[P1].accelerate(int(self._max_speed))

        if arcade.key.DOWN in self.held_keys:
            self.ship[P1].decelerate()

        if arcade.key.A in self.held_keys:
            m = 1
            if arcade.key.S in self.held_keys:
                m = 2
            self.ship[P2].turn_left(m)

        if arcade.key.D in self.held_keys:
            m = 1
            if arcade.key.S in self.held_keys:
                m = 2
            self.ship[P2].turn_right(m)

        if arcade.key.W in self.held_keys:
            self.ship[P2].accelerate(int(self._max_speed))

        if arcade.key.S in self.held_keys:
            self.ship[P2].decelerate()

        # Machine gun mode...
        # I also made it so that it plays the sound for shooting only once per cycle of shots by a player
        # This was to make the game bearable... Otherwise there would be too much noise.
        for s in self.ship:
            if self.ship[s].alive:
                if (s == P1 and arcade.key.SPACE in self.held_keys) or (s == P2 and arcade.key.GRAVE in self.held_keys):
                    if self.shoot_timer[s] == int(self._shoot_timer) and not self.mute:
                        arcade.play_sound(self.blast[s])
                    if self.shoot_timer[s] >= 0:
                        self.shoot(self.ship[s])
                        self.shoot_timer[s] -= 1
                    else:
                        if self.shoot_timer[s] <= -(int(self._shoot_timer) * 3):
                            self.shoot_timer[s] = int(self._shoot_timer)
                        else:
                            self.shoot_timer[s] -= 1

    def shoot(self, ship):
        """
        Fires bullets from a ship.
        :param ship: the ship from which the bullet shoots
        """
        image = self.get_bullet_image(ship)
        if not self.pause:
            if ship.type == ENEMY and not self.mute:
                arcade.play_sound(self.blast[ENEMY])
            self.bullets.append(ship.shoot(image))

    def get_bullet_image(self, ship):
        """
        Determines which image to use when shooting from a ship
        :param ship: the ship from which the bullet shoots
        :return: the correct bullet image
        """
        if (ship.type == P1 and self.power_up[P1]) or (ship.type == P2 and self.power_up[P2]):
            image = self.bullet_image[POWER]
        else:
            image = self.bullet_image[ship.type]
        return image

    def reset(self):
        """
        Resets values to previous state for a new game.
        """
        self.ship = {P1: Ship(), P2: PlayerTwoShip()}
        for user in self.ship:
            self.ship[user].image = self.ship_image[user]
            self.ship[user].reset_bullet()
        self.asteroids = []
        self.bullets = []
        self.initial_rocks = int(self._initial_rocks)
        self.enemies = []
        self.score = {P1: 0, P2: 0}
        self.current_state = INSTRUCTIONS
        self.final_scores = []
        self.power_ups = []
        self.power_up = {P1: False, P2: False}
        self.power_up_timer = {P1: int(self._power_up_timer), P2: int(self._power_up_timer)}
        self.shoot_timer = {P1: int(self._shoot_timer), P2: int(self._shoot_timer)}
        self.pause = False
        self.mute = False
        self.quit = False
        self.play_power_up = False
        if self.game_over:
            self.play_count += 1
        self.play_sound = True
        self.game_over = False

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        """
        if not self.game_over and self.pause:
            if key == arcade.key.R:
                self.reset()
                self.pause = False

        if self.ship[P1].alive:
            self.held_keys.add(key)
            if key == arcade.key.SPACE:
                self.shoot(self.ship[P1])

        if self.ship[P2].alive:
            self.held_keys.add(key)
            if key == arcade.key.GRAVE:
                self.shoot(self.ship[P2])

        if self.current_state == GAME_RUNNING:
            if key == arcade.key.H:
                if self.hide_hud:
                    self.hide_hud = False
                else:
                    self.hide_hud = True

        if self.current_state == INSTRUCTIONS:
            if key == arcade.key.ENTER:
                self.current_state = GAME_RUNNING

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
                    if not self.power_up[0] and not self.power_up[1]:
                        self.media_player.play()
                    else:
                        self.power_up_player.play()
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
                self.current_state = QUIT
            if key == arcade.key.N:
                self.quit = False
                if not self.pause:
                    self.game_over_player.play()

        if key == arcade.key.M:
            if not self.mute:
                self.media_player.volume = 0
                self.game_over_player.volume = 0
                self.power_up_player.volume = 0
                self.mute = True
            else:
                self.media_player.volume = 1
                self.game_over_player.volume = 1
                self.power_up_player.volume = 1
                self.mute = False

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


def prompt_filename():
    """
    Prompts user for a filename of a different game
    :return: filename
    """
    filename = input("Please enter filename of a different game setup: ")
    return filename


def prompt_new_game():
    """
    Prompts user whether they would like to import another game.
    :return: filename
    """
    invalid_response = True
    new_game = ""
    filename = ""

    while invalid_response:
        if new_game != "y" and new_game != "n":
            if new_game == "q":
                raise EndGame
            else:
                new_game = input("Do you want to load a different game? (y / n): ")
        else:
            invalid_response = False

    if new_game == "y":
        filename = prompt_filename()
    else:
        valid = False
        while not valid:
            game_type = input("Do you want to play Star Wars or Meme Battle? (s / m): ")
            if game_type != "m" and game_type != "s":
                if game_type == "q":
                    raise EndGame
                else:
                    print("Invalid response")
            else:
                if game_type == "s":
                    filename = "Files/star_wars.txt"
                elif game_type == "m":
                    filename = "Files/doge.txt"
                valid = True

    return filename


def read_file():
    """
    Reads file to get game data, stores game data and returns it
    :return: game_data
    """
    filename = prompt_new_game()
    game_data = []
    try:
        open(filename)
    except FileNotFoundError:
        print("Invalid filename. Please try again.")
        filename = prompt_new_game()
    with open(filename, "r") as f:
        for line in f:
            split = line.split()
            for i in split:
                r = i.split(',')
                game_data.append(r[2])

    return game_data


def main():
    """
    Creates the game and starts it going
    """
    try:
        game_data = read_file()
        Game(int(game_data[12]), int(game_data[13]), game_data)
        pyglet.app.run()
        arcade.run()
    except EndGame:
        print("Thanks for playing!")


if __name__ == "__main__":
    main()
