class MOD:
    def __init__(self):
        self.x = 101101
        self.mod = 0

    def modulus(self):
        self.mod = int(self.x % 10)
        self.x = self.x / 10

    def display(self):
        print("X: {}\nMOD: {}\n".format(self.x, self.mod))


def main():
    x = MOD()
    x.display()
    x.modulus()
    x.display()
    x.modulus()
    x.display()
    x.modulus()
    x.display()
    x.modulus()
    x.display()


if __name__ == "__main__":
    main()