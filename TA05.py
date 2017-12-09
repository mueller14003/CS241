"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

A walk-through of this code is available at:
https://vimeo.com/168051968
"""
import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
BALL_RADIUS = 40

VELOCITY_MULTIPLIER = 1.5


class MyApplication(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        self.ball_x_position = BALL_RADIUS
        self.ball_x_pixels_per_second = 70
        self.key_press = False

        arcade.set_background_color(arcade.color.WHITE)

        # Note:
        # You can change how often the animate() method is called by using the
        # set_update_rate() method in the parent class.
        # The default is once every 1/80 of a second.
        # self.set_update_rate(1/80)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the circle

        arcade.draw_circle_filled(self.ball_x_position, SCREEN_HEIGHT // 2,
                                  BALL_RADIUS, arcade.color.RED)

        # Draw the text
        arcade.draw_text("HOLY GUACAMOLE.",
                         (SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT // 2, arcade.color.BLACK, 20)

        if self.key_press:
            arcade.draw_rectangle_filled((SCREEN_WIDTH // 2), (SCREEN_HEIGHT / 2) - 35, 70, 70, arcade.color.GREEN)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        # Move the ball
        self.ball_x_position += self.ball_x_pixels_per_second * delta_time

        # Did the ball hit the right side of the screen while moving right?
        if self.ball_x_position > SCREEN_WIDTH - BALL_RADIUS \
                and self.ball_x_pixels_per_second > 0:
            self.ball_x_pixels_per_second *= -1

        # Did the ball hit the left side of the screen while moving left?
        if self.ball_x_position < BALL_RADIUS \
                and self.ball_x_pixels_per_second < 0:
            self.ball_x_pixels_per_second *= -1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://pythonhosted.org/arcade/arcade.key.html
        """

        # See if the user hit Shift-Space
        # (Key modifiers are in powers of two, so you can detect multiple
        # modifiers by using a bit-wise 'and'.)
        if key == arcade.key.SPACE and key_modifiers == arcade.key.MOD_SHIFT:
            print("You pressed shift-space")

        # See if the user just hit space.
        elif key == arcade.key.SPACE:
            self.key_press = True
            print("You pressed the space bar.")

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.SPACE:
            self.key_press = False
            print("You stopped pressing the space bar.")

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.ball_x_pixels_per_second *= VELOCITY_MULTIPLIER

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    MyApplication(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
