class NegativeNumberError(Exception):
    def __str__(self):
        pass


def get_inverse(n):
    try:
        n = int(n)
    except ValueError:
        raise ValueError
    if abs(n) != n:
        raise NegativeNumberError()
    elif n == 0:
        raise ZeroDivisionError
    else:
        return 1/n


def main():
    n = input("Enter a number: ")
    try:
        print("The result is: {}".format(get_inverse(n)))
    except ValueError:
        print("Error: The value must be a number")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except NegativeNumberError:
        print("Error: The value cannot be negative")


if __name__ == "__main__":
    main()
