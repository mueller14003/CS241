class BalanceError(Exception):
    def __init__(self, message, start, withdraw):
        super().__init__(message)
        self.overage_amount = start - withdraw
        print(message)
        print("Would have taken out ${} more than was in balance.".format(abs(self.overage_amount)))


class OutOfChecksError(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(message)


class CheckingAccount:
    def __init__(self, starting_balance=0.0, num_checks=0):
        if starting_balance < 0:
            raise BalanceError("ERROR: Negative input for balance", 0, starting_balance)
        else:
            self._balance = starting_balance

        self.check_count = num_checks

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise BalanceError("ERROR: Negative input for balance", self.balance, amount)
        self._balance = amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError
        else:
            self.balance += amount

    def write_check(self, amount):
        if amount < 0:
            raise ValueError
        else:
            if amount > self.balance:
                raise BalanceError("ERROR: Withdrawal larger than balance amount", self.balance, amount)
            else:
                self.balance -= amount

            if self.check_count <= 0:
                raise OutOfChecksError("ERROR: No more checks")
            else:
                self.check_count -= 1

    def buy_checks(self):
        self.check_count += 25
        self.balance -= 5

    def display(self):
        print("\nCurrent balance:", self.balance, "\nChecks left:", self.check_count)

    def apply_for_credit(self, amount):
        raise NotImplementedError


def display_menu():
    """
    Displays the available commands.
    """
    print()
    print("Commands:")
    print("  quit - Quit")
    print("  new - Create new account")
    print("  display - Display account information")
    print("  deposit - Deposit money")
    print("  check - Write a check")


def main():
    """
    Used to test the CheckingAccount class.
    """
    acc = None
    command = ""

    while command != "quit":
        display_menu()
        command = input("Enter a command: ")

        if command == "new":

            balance = float(input("Starting balance: "))
            num_checks = int(input("Numbers of checks: "))

            try:
                acc = CheckingAccount(balance, num_checks)
            except BalanceError:
                pass

        elif command == "display":
            acc.display()
        elif command == "deposit":
            amount = float(input("Amount: "))
            try:
                acc.deposit(amount)
            except ValueError:
                print("ERROR: Value entered is negative")
        elif command == "check":
            amount = float(input("Amount: "))
            try:
                try:
                    acc.write_check(amount)
                except BalanceError:
                    pass
                except OutOfChecksError:
                    prompt = input("Would you like to purchase more checks? ")
                    if prompt == "yes":
                        acc.buy_checks()
                    else:
                        pass
            except ValueError:
                print("ERROR: Value entered is negative")
        elif command == "credit":
            try:
                amount = float(input("Amount: "))
                acc.apply_for_credit(amount)
            except NotImplementedError:
                print("ERROR: Empty method")


if __name__ == "__main__":
    main()
