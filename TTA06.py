class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def prompt_for_point(self):
        self.x = int(input("Enter x: "))
        self.y = int(input("Enter y: "))

    def display(self):
        print("Center:\n({}, {})".format(self.x, self.y))


class Circle(Point):
    def __init__(self):
        Point.__init__(self)
        self.radius = 0

    def prompt_for_circle(self):
        Point.prompt_for_point(self)
        self.radius = int(input("Enter radius: "))

    def display(self):
        Point.display(self)
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