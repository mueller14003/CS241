"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 128
RIFLE_HEIGHT = 40

BULLET_RADIUS = 10
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10.0

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 25
TARGET_POINTS = 1
TARGET_STRONG_POINTS = 5
TARGET_SAFE_PENALTY = -10

POWER_UP_RADIUS = 25
POWER_UP_TIMER = 750

ONE_UP_RADIUS = 25

SPACE_TIMER = 2

INSTRUCTIONS = 0
GAME_RUNNING = 1
TRANSITION = 2
GAME_OVER = 3

BASE_LIVES = 5


class Point:
    """
    Creates Point class. This class will keep track of the
    position of an object.
    """
    def __init__(self, x=0, y=0):
        """
        Creates class variables x and y, sets to x and y parameters.
        :param x: X position
        :param y: Y position
        """
        self.x = x
        self.y = y


class Velocity:
    """
    Creates Velocity class. This class will contain information
    regarding speed in x and y axis of an object.
    """
    def __init__(self, dx=random.uniform(1, 5), dy=random.uniform(-2, 5)):
        """
        Creates class variables dx and dy, sets to dx and dy parameters.
        :param dx: Random number between 1 and 5
        :param dy: Random number between -2 and 5
        """
        self.dx = dx
        self.dy = dy


class FlyingObjects:
    """
    Creates class for Flying Objects. This is a base class for other
    flying objects classes that will be created. Contains methods:
        advance
        draw
        is_off_screen
    """
    def __init__(self, radius=10):
        """
        Creates and sets class variables.
        :param radius: Default radius size
        """
        self.center = Point()
        self.center.x = random.uniform(1, SCREEN_WIDTH / 2)
        self.center.y = random.uniform(SCREEN_HEIGHT / 2, SCREEN_HEIGHT - 1)
        self.velocity = Velocity()
        self.radius = radius
        self.alive = True
        self.image = "Goomba.png"
        self.angle = 0
        self.multiplier = 1
        self.spin_amount = 0

    def advance(self):
        """
        Changes the position of a flying object.
        """
        self.center.x += self.velocity.dx * self.multiplier
        self.center.y += self.velocity.dy * self.multiplier

    def spin(self):
        self.angle += self.spin_amount

    def draw(self):
        """
        Draws a flying object
        """
        self.spin()
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius * 2,
                                      self.radius * 2, texture, self.angle, alpha=1)

    def is_off_screen(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        """
        Checks to see if flying object is inside screen boundary. If object has left screen,
        returns a false value, else returns True.
        :param width: Screen Width
        :param height: Screen Height
        """
        if self.center.x < 0 or self.center.x >= width:
            self.alive = False
            return True
        elif self.center.y < 0 or self.center.y >= height:
            self.alive = False
            return True
        else:
            pass


class Bullet(FlyingObjects):
    """
    Creates Bullet class. Inherits instance variables and methods
    from Flying Objects class. Bullets are fired from rifle.
    """
    def __init__(self):
        """
        Creates and sets instance variables. Inherits instance variables from Flying
        Objects class.
        """
        FlyingObjects.__init__(self, radius=BULLET_RADIUS)
        self.center.x = 1
        self.center.y = 1
        self.image = "bullet.png"

    def fire(self, angle, speed=(BULLET_SPEED * 3)):
        """
        Fires a bullet in the direction of the rifle.
        I made the bullets fly faster because they were very slow...
        :param angle: Angle in which the mouse is pointing from the point (0, 0)
        :param speed: Speed at which the object will be fired at
        """
        self.angle = angle
        self.velocity.dx = math.cos(math.radians(angle)) * speed
        self.velocity.dy = math.sin(math.radians(angle)) * speed


class Target(FlyingObjects):
    """
    Creates Target class. Inherits from Flying Objects class. Targets are things you aim at...
    """
    def __init__(self):
        """
        Inherits instance variables from Flying Objects.
        Creates new instance variables.
        """
        FlyingObjects.__init__(self, radius=TARGET_RADIUS)
        self.hits_left = 1
        self.type = 1
        self.velocity.dx = random.uniform(1, 5)
        self.velocity.dy = random.uniform(-2, 5)
        self.spin_amount = random.uniform(-3, 3)
        self.points = TARGET_POINTS
        self.power_points = TARGET_POINTS * 2

    def hit(self):
        """
        Sets self.alive to false, returns TARGET_POINTS
        :return: TARGET_POINTS
        """
        self.alive = False
        return self.points

    def hit_power_up(self):
        """
        I created this method for when the user hits a power up. The user receives
        twice the amount of points per target than they would otherwise. Sets self.alive
        to false.
        :return: TARGET_POINTS * 2
        """
        self.alive = False
        return self.power_points


class NormalTarget(Target):
    """
    Creates a normal target class. Inherits from Target class.
    """
    def __init__(self):
        """
        Inherits everything from Target class.
        """
        Target.__init__(self)


class StrongTarget(Target):
    """
    Creates Strong Target class, inherits from Target class. Strong targets are harder
    to destroy than other targets, but they give the user more points for destroying them.
    """
    def __init__(self):
        """
        Inherits from Target class, sets instance variables.
        """
        Target.__init__(self)
        self.hits_left = 3
        self.type = 2
        self.points = TARGET_STRONG_POINTS
        self.power_points = TARGET_STRONG_POINTS * 2
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-2, 3)
        self.color = arcade.color.BLACK
        self.image = "ChainChomp.png"
        self.spin_amount = random.uniform(-4, 4)

    def draw(self):
        """
        Draws strong target with number of hits left until the target will be
        destroyed in the middle of the target.
        """
        super().draw()
        arcade.draw_text(str(self.hits_left), self.center.x - (self.radius / 5), self.center.y - 35,
                         font_size=12, color=self.color)

    def hit(self):
        """
        Keeps track of hits. Strong targets have to be hit 3 times to be destroyed.
        The instance variable self.hits_left keeps track of this.
        The corresponding hit value is returned for each hit on a strong target.
        :return: TARGET_POINTS or TARGET_STRONG_POINTS
        """
        if self.hits_left > 1:
            self.hits_left -= 1
            return TARGET_POINTS
        elif self.hits_left == 1:
            self.alive = False
            return self.points
        else:
            print("ERROR... Should be dead")


class SafeTarget(Target):
    """
    Creates Safe Target class. These targets are not meant to be hit.
    When the user hits one of these targets, they lose a certain amount
    of points and they also lose a life. This class inherits from the Target class.
    """
    def __init__(self):
        """
        Inherits from Target class, sets instance variables.
        """
        Target.__init__(self)
        self.radius = TARGET_SAFE_RADIUS
        self.type = 3
        self.points = TARGET_SAFE_PENALTY
        self.power_points = 0
        self.velocity.dx = random.uniform(1, 2)
        self.velocity.dy = random.uniform(-2, 2)
        self.image = "mario.png"
        self.spin_amount = random.uniform(-5, 5)


class PowerUp(FlyingObjects):
    """
    I created this Power Up class to add a bit of spice to the game. This class
    allows for power ups to be created. Power ups will allow you to hit any target
    without any penalty, and for the period that a power up is activated, a constant
    stream of bullets will be fired from the rifle. One can gain many points when using
    a power up. This class inherits from the Flying Objects class.
    """
    def __init__(self):
        """
        This class inherits all instance variables from Flying Objects.
        """
        FlyingObjects.__init__(self, radius=POWER_UP_RADIUS)
        self.image = "STAR.png"
        self.multiplier = 1.5
        self.spin_amount = 0


class OneUp(FlyingObjects):
    """
    The One Up class is for flying objects that will increase the lives you have by one.
    They are green one up mushrooms from Mario. The One Up class inherits from the Flying Objects class.
    """
    def __init__(self):
        """
        Inherits all instance variables from Flying Objects, sets radius and color accordingly.
        """
        FlyingObjects.__init__(self, radius=ONE_UP_RADIUS)
        self.image = "1UP-Mushroom.png"
        self.spin_amount = random.uniform(-2, 2)


class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        """
        Initializes instance variables.
        """
        self.center = Point()
        self.center.x = 0
        self.center.y = 0
        self.angle = 45
        self.image = "Minigun.png"

    def draw(self):
        """
        Draws the Rifle.
        """
        texture = arcade.load_texture(self.image)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, RIFLE_WIDTH,
                                      RIFLE_HEIGHT, texture, self.angle, alpha=1)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []
        self.targets = []
        self.holding_space = False
        self.power = False
        self.power_ups = []
        self.one_ups = []
        self.timer = POWER_UP_TIMER
        self.space_timer = SPACE_TIMER
        self.lives = BASE_LIVES
        self.current_state = INSTRUCTIONS
        self.final_scores = []
        self.final_score = 0
        self.play_count = 0
        self.high_score = 0
        self.level = 0
        self.game_over = False

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # Draws different things depending on state of game

        # Draws instructions at start of game
        if self.current_state == INSTRUCTIONS:
            self.draw_instructions()

        # Draws the game
        if self.current_state == GAME_RUNNING:
            # draw each object
            self.rifle.draw()
            for bullet in self.bullets:
                bullet.draw()
            for target in self.targets:
                target.draw()
            for power_up in self.power_ups:
                power_up.draw()
            for one_up in self.one_ups:
                one_up.draw()
            self.draw_score()
            self.draw_lives()

        # Completes transitional actions before game over.
        elif self.current_state == TRANSITION:
            self.final_scores.append(self.score)
            self.get_final_value()

        # Displays game over screen
        elif self.current_state == GAME_OVER:
            self.draw_final()

    def draw_instructions(self):
        """
        Draws pre-game instructions.
        """
        arcade.draw_text("INSTRUCTIONS:", start_x=80, start_y=SCREEN_HEIGHT - 70,
                         font_size=50, color=arcade.color.BLACK)
        arcade.draw_text("Try to hit as many enemy targets as you can!", start_x=30,
                         start_y=SCREEN_HEIGHT - 140, font_size=16, color=arcade.color.BLACK)
        arcade.draw_text("Avoid hitting Mario! You will lose a life and points.", start_x=30,
                         start_y=SCREEN_HEIGHT - 200, font_size=16, color=arcade.color.BLACK)
        arcade.draw_text("The stars will give you invincibility, but they're hard to hit!", start_x=30,
                         start_y=SCREEN_HEIGHT - 260, font_size=16, color=arcade.color.BLACK)
        arcade.draw_text("The green mushrooms give you more lives.", start_x=30,
                         start_y=SCREEN_HEIGHT - 320, font_size=16, color=arcade.color.BLACK)
        arcade.draw_text("Press ENTER to play!", start_x=110,
                         start_y=SCREEN_HEIGHT - 420, font_size=32, color=arcade.color.BLACK)

    def get_final_value(self):
        """
        Gets final value, stores into list, changes current state to game over.
        """
        self.final_score = self.final_scores[self.play_count]
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
        Displays game over screen, including final score, high score, and times played.
        """

        self.get_high_score()
        arcade.set_background_color(arcade.color.BLACK)
        score_text = "Final Score: {}".format(self.final_score)
        high_text = "High Score: {}".format(self.high_score)
        other_text = "Total times played: {}".format(self.play_count + 1)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)
        arcade.draw_text("GAME OVER!", start_x=70, start_y=(SCREEN_HEIGHT / 2), font_size=64,
                         color=arcade.color.WHITE)
        arcade.draw_text(high_text, start_x=(SCREEN_WIDTH - 120), start_y=start_y, font_size=12,
                         color=arcade.color.WHITE)
        arcade.draw_text("Press Enter to continue", start_x=(SCREEN_WIDTH/2 - 155), start_y=(SCREEN_HEIGHT / 2) - 35,
                         font_size=24, color=arcade.color.WHITE)
        arcade.draw_text(other_text, start_x=10, start_y=12, font_size=12,
                         color=arcade.color.WHITE)

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def draw_lives(self):
        """
        Puts lives left on screen.
        """
        lives = "Lives: {}".format(self.lives)
        start_x = SCREEN_WIDTH - 80
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(lives, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()
        self.check_clicker()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        if random.randint(1, 1500) == 1:
            self.create_power_up()

        if random.randint(1, 750) == 1:
            self.create_one_up()

        for bullet in self.bullets:
            bullet.advance()

        for target in self.targets:
            target.advance()

        for power_up in self.power_ups:
            power_up.advance()

        for one_up in self.one_ups:
            one_up.advance()

        if self.power:
            self.continuous_fire()

        if self.lives <= 0:
            if not self.game_over:
                self.current_state = TRANSITION
                self.game_over = True

    def create_power_up(self):
        """
        Creates Power Ups, adds to list.
        """
        power_up = PowerUp()
        self.power_ups.append(power_up)

    def create_one_up(self):
        """
        Creates Power Ups, adds to list.
        """
        one_up = OneUp()
        self.one_ups.append(one_up)

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        """
        rand = random.randint(1, 3)
        target = None

        if rand == 1:
            target = NormalTarget()
        elif rand == 2:
            target = StrongTarget()
        elif rand == 3:
            target = SafeTarget()

        self.targets.append(target)

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:
                # Make sure they are all alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                            abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        if not self.power:
                            self.score += target.hit()
                            if target.type == 3:
                                self.lives -= 1
                        if self.power:
                            self.score += target.hit_power_up()

        for bullet in self.bullets:
            for power_up in self.power_ups:
                if bullet.alive and power_up.alive:
                    too_close = bullet.radius + power_up.radius

                    if (abs(bullet.center.x - power_up.center.x) < too_close and
                            abs(bullet.center.y - power_up.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        power_up.alive = False
                        self.timer = POWER_UP_TIMER
                        self.apply_power_up()

        for bullet in self.bullets:
            for one_up in self.one_ups:
                if bullet.alive and one_up.alive:
                    too_close = bullet.radius + one_up.radius

                    if (abs(bullet.center.x - one_up.center.x) < too_close and
                            abs(bullet.center.y - one_up.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        one_up.alive = False
                        self.lives += 1

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def apply_power_up(self):
        """
        Applies Power Up
        """
        self.power = True

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        """

        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

        for power_up in self.power_ups:
            if not power_up.alive:
                self.power_ups.remove(power_up)

        for one_up in self.one_ups:
            if not one_up.alive:
                self.one_ups.remove(one_up)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        """

        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

        for power_up in self.power_ups:
            if power_up.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.power_ups.remove(power_up)

        for one_up in self.one_ups:
            if one_up.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.one_ups.remove(one_up)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        set the rifle angle in degrees
        :param x:
        :param y:
        :param dx:
        :param dy:
        """

        self.rifle.angle = self._get_angle_degrees(x, y)

    def check_clicker(self):
        """
        Checks to see if the user is holding down the
        mouse button, and if so, takes appropriate action.
        """

        if self.holding_space:
            self.continuous_fire()

    def on_key_press(self, key, key_modifiers):
        """
        When key is pressed performs action.
        :param key:
        :param key_modifiers:
        """

        if key == arcade.key.SPACE:
            self.holding_space = True

        if self.current_state == INSTRUCTIONS:
            if key == arcade.key.ENTER:
                self.current_state = GAME_RUNNING
                arcade.set_background_color(arcade.color.BABY_BLUE)

        if self.current_state == GAME_OVER:
            if key == arcade.key.ENTER:
                self.reset()
                self.current_state = GAME_RUNNING

    def reset(self):
        """
        Resets values to previous state for a new game.
        """

        self.score = 0
        self.bullets = []
        self.targets = []
        self.one_ups = []
        self.holding_space = False
        self.power = False
        self.power_ups = []
        self.timer = POWER_UP_TIMER
        self.space_timer = SPACE_TIMER
        self.lives = BASE_LIVES
        self.level = 0
        arcade.set_background_color(arcade.color.BABY_BLUE)
        self.game_over = False
        self.play_count += 1

    def on_key_release(self, key, key_modifiers):
        """
        When key is released, performs action.
        :param key:
        :param key_modifiers:
        """

        if key == arcade.key.SPACE:
            self.holding_space = False

    def continuous_fire(self):
        """
        MACHINE GUN! If you hold space, you can use a watered down version of the machine gun.
        However, if you have a power up, you get the complete awesomeness!
        """

        if not self.power:
            if self.space_timer >= 0:
                bullet = Bullet()
                bullet.fire(self.rifle.angle, (BULLET_SPEED * 2))
                self.space_timer -= 1
                self.bullets.append(bullet)
            else:
                if self.space_timer <= -10:
                    self.space_timer = SPACE_TIMER
                else:
                    self.space_timer -= 1

        # This is awesome! It changes the background color, it changes the bullets to
        # huge fireballs, and the bullets continuously rapid fire.
        # There also is no penalty for hitting safe targets.
        elif self.power:
            if self.timer >= 0:
                bullet = Bullet()
                bullet.image = "Fireball.png"
                bullet.radius = 30
                arcade.set_background_color(arcade.color.GRAPE)
                bullet.fire(self.rifle.angle, (BULLET_SPEED * 5))
                self.timer -= 1
                self.bullets.append(bullet)
            # Resets everything
            else:
                self.power = False
                self.timer = POWER_UP_TIMER
                arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Fire!
        """
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()

        if not self.power:
            bullet.fire(angle)
        elif self.power:
            bullet.fire(angle)
            self.continuous_fire()

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees


def main():
    """
    Creates the game and starts it going
    """
    Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
