"""
I think that this approach is better because a circle is not a type of point, but rather,
it has a location, or point. Thus, it should not inherit from Point, but rather, it should create
a class variable that is a point type. This makes much more sense, as a circle will have a point
attribute, but is not a type of point.
"""


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def prompt_for_point(self):
        self.x = int(input("Enter x: "))
        self.y = int(input("Enter y: "))

    def display(self):
        print("Center:\n({}, {})".format(self.x, self.y))


class Circle:
    def __init__(self):
        self.point = Point()
        self.radius = 0

    def prompt_for_circle(self):
        self.point.prompt_for_point()
        self.radius = int(input("Enter radius: "))

    def display(self):
        self.point.display()
        print("Radius: {}".format(self.radius))


def main():
    point = Point()
    point.prompt_for_point()
    point.display()

    print()
    circle = Circle()
    circle.prompt_for_circle()
    circle.display()


if __name__ == "__main__":
    main()