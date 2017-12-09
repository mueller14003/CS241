"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 45

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 7

ASTEROID_SPAWN_TIMER = 300


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0


class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0


class FlyingObjects:
    """
    Creates class for Flying Objects. This is a base class for other
    flying objects classes that will be created. Contains methods:
        advance
        draw
        is_off_screen
        fire
        hit
    """
    def __init__(self):
        """
        Creates and sets class variables.
        """
        self.center = Point()
        self.center.x = random.uniform(1, SCREEN_WIDTH - 1)
        self.center.y = random.uniform(1, SCREEN_HEIGHT - 1)
        self.velocity = Velocity()
        self.radius = 0
        self.color = arcade.color.ORANGE
        self.alive = True
        self.angle = 0
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.image = "Trump.png"
        self.alpha = 1

    def advance(self, multiplier=1):
        """
        Changes the position of a flying object
        :param multiplier: Value can be changed to increase speed of flying object
        """
        self.center.x += self.velocity.dx * multiplier
        self.center.y += self.velocity.dy * multiplier

    def draw(self):
        """
        Draws a flying object
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius * 2, self.radius * 2, texture,
                                      self.angle, self.alpha)

    def check_off_screen(self):
        if self.center.x <= 0:
            self.center.x = SCREEN_WIDTH - 1
        elif self.center.x >= SCREEN_WIDTH:
            self.center.x = 1
        elif self.center.y <= 0:
            self.center.y = SCREEN_HEIGHT - 1
        elif self.center.y >= SCREEN_HEIGHT:
            self.center.y = 1

    #def is_off_screen(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    #    """
    #    Checks to see if flying object is inside screen boundary. If object has left screen,
    #    returns a false value, else returns True.
    #    :param width: Screen Width
    #    :param height: Screen Height
    #    """
    #    if self.center.x < 0 or self.center.x >= width:
    #        self.alive = False
    #        return True
    #    elif self.center.y < 0 or self.center.y >= height:
    #        self.alive = False
    #        return True
    #    else:
    #        pass


class Asteroid(FlyingObjects):
    def __init__(self):
        super().__init__()
        self.image = "CNN.png"
        self.radius = BIG_ROCK_RADIUS
        self.spin = BIG_ROCK_SPIN
        self.velocity_angle = random.uniform(0, 359)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.velocity_angle)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.velocity_angle)) * self.speed
        self.type = 1

    def rotate(self):
        self.angle += self.spin

    def draw(self):
        self.rotate()
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius * 4, self.radius * 2, texture,
                                      self.angle, self.alpha)


class MediumAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.image = "CNN.png"
        self.radius = MEDIUM_ROCK_RADIUS
        self.spin = MEDIUM_ROCK_SPIN
        self.type = 2


class SmallAsteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.image = "CNN.png"
        self.radius = SMALL_ROCK_RADIUS
        self.spin = SMALL_ROCK_SPIN
        self.type = 3


class Laser(FlyingObjects):
    def __init__(self):
        super().__init__()
        self.image = "Twitter.png"
        self.center.x = 0
        self.center.y = 0
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED

    def fire(self, ship):
        self.velocity.dx = ship.velocity.dx + (math.cos(math.radians(ship.angle)) * self.speed)
        self.velocity.dy = ship.velocity.dy + (math.sin(math.radians(ship.angle)) * self.speed)


class Ship(FlyingObjects):
    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.speed = 1

    def move(self):
        self.velocity.dx = math.cos(math.radians(self.angle)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.angle)) * self.speed

    def accelerate(self):
        self.speed += SHIP_THRUST_AMOUNT
        self.move()

    def decelerate(self):
        self.speed -= SHIP_THRUST_AMOUNT
        self.move()

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
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.asteroids = []
        self.bullets = []
        self.count = INITIAL_ROCK_COUNT

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        self.ship.draw()

        for bullet in self.bullets:
            bullet.draw()

        for asteroid in self.asteroids:
            asteroid.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        self.check_off_screen()
        self.ship.advance()

        if self.count > 0:
            asteroid = Asteroid()
            self.asteroids.append(asteroid)
            self.count -= 1

        else:
            rand = random.randint(1, ASTEROID_SPAWN_TIMER)
            if rand == 1:
                asteroid = Asteroid()
                self.asteroids.append(asteroid)
            else:
                pass

        for bullet in self.bullets:
            if bullet.life > 0:
                bullet.advance()
                bullet.life -= 1
            else:
                bullet.alive = False

        for asteroid in self.asteroids:
            asteroid.advance()

    # TODO: THIS
    def asteroid_split(self, asteroid):
        if asteroid.type == 1:
            med_1 = MediumAsteroid()
            med_1.center.x = asteroid.center.x
            med_1.center.y = asteroid.center.y
            med_1.velocity.dx = asteroid.velocity.dx
            med_1.velocity.dy = asteroid.velocity.dy + 2
            med_2 = MediumAsteroid()
            med_2.center.x = asteroid.center.x
            med_2.center.y = asteroid.center.y
            med_2.velocity.dx = asteroid.velocity.dx
            med_2.velocity.dy = asteroid.velocity.dy - 2
            small_1 = SmallAsteroid()
            small_1.center.x = asteroid.center.x
            small_1.center.y = asteroid.center.y
            small_1.velocity.dx = asteroid.velocity.dx + 5
            small_1.velocity.dy = asteroid.velocity.dy
            self.asteroids.extend([med_1, med_2, small_1])
        elif asteroid.type == 2:
            small_1 = SmallAsteroid()
            small_1.center.x = asteroid.center.x
            small_1.center.y = asteroid.center.y
            small_1.velocity.dx = asteroid.velocity.dx + 1.5
            small_1.velocity.dy = asteroid.velocity.dy + 1.5
            small_2 = SmallAsteroid()
            small_2.center.x = asteroid.center.x
            small_2.center.y = asteroid.center.y
            small_2.velocity.dx = asteroid.velocity.dx - 1.5
            small_2.velocity.dy = asteroid.velocity.dy - 1.5
            self.asteroids.extend([small_1, small_2])
        elif asteroid.type == 3:
            pass
        asteroid.alive = False

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                # Make sure they are all alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.asteroid_split(asteroid)

        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or asteroids from the list.
        """

        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        """
        self.ship.check_off_screen()

        for bullet in self.bullets:
            bullet.check_off_screen()

        for asteroid in self.asteroids:
            asteroid.check_off_screen()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += SHIP_TURN_AMOUNT

        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= SHIP_TURN_AMOUNT

        if arcade.key.UP in self.held_keys:
            self.ship.accelerate()

        if arcade.key.DOWN in self.held_keys:
            self.ship.decelerate()

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            if self.ship.alive:
                bullet = Laser()
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                bullet.angle = self.ship.angle
                bullet.fire(self.ship)
                self.bullets.append(bullet)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Laser()
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                bullet.angle = self.ship.angle
                bullet.fire(self.ship)
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


def main():
    # Creates the game and starts it going
    Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
