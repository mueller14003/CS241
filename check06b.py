class Phone:
    def __init__(self):
        self.area_code = 0
        self.prefix = 0
        self.suffix = 0

    def prompt_number(self, phone="Phone"):
        self.area_code = int(input("\n{}:\nArea Code: ".format(phone)))
        self.prefix = int(input("Prefix: "))
        self.suffix = int(input("Suffix: "))

    def display(self):
        print("\nPhone info:\n({}){}-{}".format(self.area_code, self.prefix, self.suffix))


class SmartPhone(Phone):
    def __init__(self):
        Phone.__init__(self)
        self.email = ""

    def prompt(self):
        Phone.prompt_number(self, "Smart phone")
        self.email = input("Email: ")

    def display(self):
        Phone.display(self)
        print(self.email)


def main():
    phone = Phone()
    phone.prompt_number()
    phone.display()

    smart_phone = SmartPhone()
    smart_phone.prompt()
    smart_phone.display()


if __name__ == "__main__":
    main()
