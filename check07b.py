"""
File: check07b.py
Author: Br. Burton

Demonstrates abstract base classes.
"""


# DONE: Import anything you need for Abstract Base Classes / methods
from abc import ABC, abstractmethod


# DONE: convert this to an ABC
class Shape(ABC):
    def __init__(self, name=""):
        self.name = name
        super().__init__()

    def display(self):
        print("{} - {:.2f}".format(self.name, self.get_area()))

    @abstractmethod
    def get_area(self):
        return 0.0


# DONE: Create a Circle class here that derives from Shape
class Circle(Shape):
    def __init__(self):
        Shape.__init__(self, name="Circle")
        self.radius = 0.0

    def get_area(self):
        return 3.14 * self.radius * self.radius


# DONE: Create a Rectangle class here that derives from Shape
class Rectangle(Shape):
    def __init__(self):
        Shape.__init__(self, name="Rectangle")
        self.length = 0.0
        self.width = 0.0

    def get_area(self):
        return self.length * self.width


def main():
    # DONE: Declare your list of shapes here
    shapes = []

    command = ""

    while command != "q":
        command = input("Please enter 'c' for circle, 'r' for rectangle or 'q' to quit: ")

        if command == "c":
            radius = float(input("Enter the radius: "))
            # DONE: Declare your Circle here, set its radius, and
            # add it to the list
            circle = Circle()
            circle.radius = radius
            shapes.append(circle)

        elif command == "r":
            length = float(input("Enter the length: "))
            width = float(input("Enter the width: "))
            # DONE: Declare your Rectangle here, set its length
            # and width, and add it to the list
            rectangle = Rectangle()
            rectangle.length = length
            rectangle.width = width
            shapes.append(rectangle)

            # Done entering shapes, now lets print them all out:

            # DONE: Loop through each shape in the list, and call its display function
    for shape in shapes:
        shape.display()


if __name__ == "__main__":
    main()

