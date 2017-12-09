class Money:
    def __init__(self):
        self._dollars = 0
        self._cents = 0

    @property
    def dollars(self):
        return self._dollars

    @dollars.setter
    def dollars(self, value):
        self._dollars = value

    @property
    def cents(self):
        return self._cents

    @cents.setter
    def cents(self, value):
        if value >= 100:
            self._dollars += value // 100
            self._cents = value % 100
        else:
            self._cents = value

    def display(self):
        print("{}.{}".format(self._dollars, self._cents))


def main():
    wallet = Money()
    wallet.display()
    wallet.dollars = 20
    wallet.cents = 350
    wallet.display()


if __name__ == "__main__":
    main()
