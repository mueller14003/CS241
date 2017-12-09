import arcade

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600


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
    def __init__(self, radius=10, color=arcade.color.CARROT_ORANGE):
        """
        Creates and sets class variables.
        :param radius: Default radius size
        :param color: Color default
        """
        self.center = Point()
        self.center.x = 50
        self.center.y = 50
        self.velocity = Velocity()
        self.velocity.dx = 4
        self.velocity.dy = 4

    def advance(self, multiplier=1):
        """
        Changes the position of a flying object
        :param multiplier: Value can be changed to increase speed of flying object
        """
        self.center.x += self.velocity.dx * multiplier
        self.center.y += self.velocity.dy * multiplier

    def bounce_horizontal(self):
        """
        Causes the ball to bounce horizontally
        """
        self.velocity.dx = self.velocity.dx * (-1)

    def bounce_vertical(self):
        """
        Causes the ball to bounce vertically
        """
        self.velocity.dy = self.velocity.dy * (-1)


class Doge(FlyingObjects):
    def __init__(self):
        super().__init__()

    def draw(self):
        img = "Doge.png"
        texture = arcade.load_texture(img)

        width = texture.width / 2.5
        height = texture.height / 2.5
        alpha = 1  # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y

        arcade.draw_texture_rectangle(x, y, width, height, texture, alpha)


class Game(arcade.Window):
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.doge = Doge()

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: Set game states
        self.doge.draw()
        arcade.draw_text("wow",400,400, color=arcade.color.ORANGE, font_size=35)
        arcade.draw_text("such bounce", 200, 200, color=arcade.color.BLUE, font_size=30)
        arcade.draw_text("many cool", 700, 300, color=arcade.color.RED, font_size=25)
        arcade.draw_text("much python", 600, 150, color=arcade.color.GREEN, font_size=30)
        arcade.draw_text("very computer", 350, 500, color=arcade.color.BLACK, font_size=25)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_bounce()
        self.doge.advance()

    def check_bounce(self):
        if self.doge.center.x < 0 or self.doge.center.x > SCREEN_WIDTH:
            self.doge.bounce_horizontal()
        elif self.doge.center.y < 0 or self.doge.center.y > SCREEN_HEIGHT:
            self.doge.bounce_vertical()


# Creates the game and starts it going
def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
