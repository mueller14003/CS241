class Factorial:
    def __init__(self):
        self.n = 0

    def factorial(self, n):
        if n <= 0:
            return 1
        else:
            return n * self.factorial(n - 1)

    def prompt(self):
        self.n = int(input("Please enter a number: "))

    def display(self):
        print("The factorial of {} is {}".format(self.n, self.factorial(self.n)))


def main():
    power = Factorial()
    power.prompt()
    power.display()


if __name__ == "__main__":
    main()
