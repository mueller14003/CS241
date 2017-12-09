def main():
    while True:
        try:
            num = input("Enter a number: ")
            num = int(num)
        except ValueError:
            print("The value entered is not valid")
        else:
            break

    print("The result is: {}".format(num * 2))


if __name__ == "__main__":
    main()
