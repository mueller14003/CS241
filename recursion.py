class PowerCalculator:
    def __init__(self):
        self.a = 0
        self.n = 0

    def power_function(self, n):
        if n == 0:
            return 1
        else:
            return self.a * self.power_function(n - 1)

    def prompt(self):
        self.a = int(input("Please enter a number: "))
        self.n = int(input("Please enter an exponent: "))

    def display(self):
        print("{} to the {} power is: {}".format(self.a, self.n, self.power_function(self.n)))


def main():
    power = PowerCalculator()
    power.prompt()
    power.display()


if __name__ == "__main__":
    main()
