
BASE_TWO_START_VALUE = 1048576
BINARY_START_VALUE = 100000000000000000000.0000


class BinaryError(Exception):
    def __str__(self):
        pass


class HexValue:
    def __init__(self, decimal="0", binary="0000", hexadecimal="0"):
        self.dec = decimal
        self.bin = binary
        self.hex = hexadecimal


class Hexadecimal:
    def __init__(self, d="0", b="0000", h="0"):
        self.value = HexValue(d, b, h)


class Zero(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self)


class One(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "1", "0001", "1")


class Two(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "2", "0010", "2")


class Three(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "3", "0011", "3")


class Four(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "4", "0100", "4")


class Five(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "5", "0101", "5")


class Six(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "6", "0110", "6")


class Seven(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "7", "0111", "7")


class Eight(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "8", "1000", "8")


class Nine(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "9", "1001", "9")


class A(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "10", "1010", "A")


class B(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "11", "1011", "B")


class C(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "12", "1100", "C")


class D(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "13", "1101", "D")


class E(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "14", "1110", "E")


class F(Hexadecimal):
    def __init__(self):
        Hexadecimal.__init__(self, "15", "1111", "F")


class Calculator:
    def __init__(self):
        self.user_in = ""
        self.base_two = BASE_TWO_START_VALUE
        self.binary = BINARY_START_VALUE
        self.total = ""
        self.done = False
        self.modulus = 0
        self.which = ""

    def display(self):
        while True:
            try:
                print("Value in {} is: {}".format(self.which, self.total))
            except BinaryError:
                print("\"{}\" is not a Binary number. Please try again.\n".format(self.user_in))
            else:
                break

    def ask(self, in_out=""):
        ask = input("{} is Binary, Decimal, or Hexadecimal (B, D, H)?".format(in_out))
        return ask

    def get_calc(self):
        user_in = self.ask("Input")
        q2 = self.ask("Output")
        valid = False
        while not valid:
            if user_in == "B" or user_in == "b":
                if q2 == "B" or q2 == "b":
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
                elif q2 == "D" or q2 == "d":
                    self.binary_to_decimal()
                    valid = True
                elif q2 == "H" or q2 == "h":
                    self.binary_to_hexadecimal()
                    valid = True
                else:
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
            elif user_in == "D" or user_in == "d":
                if q2 == "B" or q2 == "b":
                    self.decimal_to_binary()
                    valid = True
                elif q2 == "D" or q2 == "d":
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
                elif q2 == "H" or q2 == "h":
                    self.decimal_to_hexadecimal()
                    valid = True
                else:
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
            elif user_in == "H" or user_in == "h":
                if q2 == "B" or q2 == "b":
                    self.hexadecimal_to_binary()
                    valid = True
                elif q2 == "D" or q2 == "d":
                    self.decimal_to_hexadecimal()
                    valid = True
                elif q2 == "H" or q2 == "h":
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
                else:
                    print("Invalid Entry.")
                    user_in = self.ask("Input")
                    q2 = self.ask("Output")
            else:
                print("Invalid Entry.")
                user_in = self.ask("Input")
                q2 = self.ask("Output")

    def binary_to_decimal(self):
        self.user_in = input("Please enter a binary number: ")
        r = 0
        self.which = "decimal"
        for character in self.user_in:
            if character == '0':
                r = r * 2
            elif character == '1':
                r = r * 2 + 1
            else:
                raise BinaryError()
        self.total = r
        self.display()

    def decimal_to_binary(self):
        self.user_in = float(input("Please enter a decimal number: "))
        self.which = "binary"
        self.total = 0.0

        while not self.done:
            if self.user_in == 0:
                self.done = True
            elif self.user_in >= self.base_two:
                self.total += self.binary
                self.user_in -= self.base_two
                self.binary /= 10
                self.base_two /= 2
            elif self.user_in < self.base_two:
                self.binary /= 10
                self.base_two /= 2
        self.display()

    def hexadecimal_to_binary(self):
        self.user_in = input("Please enter a hexadecimal number: ")
        self.which = "binary"
        for value in self.user_in:
            if value == "0":
                self.total += "0000"
            elif value == "1":
                self.total += "0001"
            elif value == "2":
                self.total += "0010"
            elif value == "3":
                self.total += "0011"
            elif value == "4":
                self.total += "0100"
            elif value == "5":
                self.total += "0101"
            elif value == "6":
                self.total += "0110"
            elif value == "7":
                self.total += "0111"
            elif value == "8":
                self.total += "1000"
            elif value == "9":
                self.total += "1001"
            elif value == "A" or value == "a":
                self.total += "1010"
            elif value == "B" or value == "b":
                self.total += "1011"
            elif value == "C" or value == "c":
                self.total += "1100"
            elif value == "D" or value == "d":
                self.total += "1101"
            elif value == "E" or value == "e":
                self.total += "1110"
            elif value == "F" or value == "f":
                self.total += "1111"
        self.display()

    def binary_to_hexadecimal(self):
        self.user_in = input("Please enter a binary number: ")
        if len(self.user_in) % 4 == 0:
            pass
        elif len(self.user_in) % 4 == 1:
            self.user_in = "0" + self.user_in

        elif len(self.user_in) % 4 == 2:
            self.user_in = "00" + self.user_in

        elif len(self.user_in) % 4 == 3:
            self.user_in = "000" + self.user_in

    def decimal_to_hexadecimal(self):
        self.user_in = input("Please enter a decimal number: ")

    def hexadecimal_to_decimal(self):
        self.user_in = input("Please enter a hexadecimal number: ")


def main():
    calc = Calculator()
    calc.get_calc()


if __name__ == "__main__":
    main()
