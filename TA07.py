
from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, name=""):
        self.name = name
        self.type = ""
        self.amount = 0
        super().__init__()

    @abstractmethod
    def get_paycheck(self):
        pass

    # More intuitive... I like this better than how the assignment says to do it.
    # @abstractmethod
    def display(self):
        print("{} - ${}/{}".format(self.name, self.amount, self.type))


class HourlyEmployee(Employee):
    def __init__(self, name_input=""):
        super().__init__(name=name_input)
        self.hours = 0
        self.type = "hour"

    # def display(self):
    #   print("{} - ${}/hour".format(self.name, self.amount))

    def get_paycheck(self):
        return self.amount * self.hours


class SalaryEmployee(Employee):
    def __init__(self, name_input=""):
        super().__init__(name=name_input)
        self.type = "year"

    # def display(self):
    #   print("{} - ${}/year".format(self.name, self.amount))

    def get_paycheck(self):
        return self.amount / 24


def display_employee_data(employee):
    print()
    employee.display()
    print("${}/paycheck".format(employee.get_paycheck()))


def main():
    employees = []
    command = ""

    while command != "q":
        command = input("Please enter 'h' for hourly, 's' for salary or 'q' to quit: ")
        if command != "q" and (command == "h" or command == "s"):
            print()
            name = input("Enter name: ")
        else:
            pass

        if command == "h":
            employee = HourlyEmployee(name)
            employee.amount = float(input("Pay per hour: "))
            employee.hours = float(input("Hours worked: "))
            employees.append(employee)
            print()

        elif command == "s":
            employee = SalaryEmployee(name)
            employee.amount = float(input("Pay per year: "))
            employees.append(employee)
            print()

    for employee in employees:
        display_employee_data(employee)


if __name__ == "__main__":
    main()
