class GPA:
    def __init__(self):
        self.gpa = 0.0

    def get_gpa(self):
        if self.gpa < 0:
            return 0
        elif self.gpa > 4:
            return 4
        else:
            return self.gpa

    def set_gpa(self, value):
        if value < 0:
            self.gpa = 0
        elif value > 4:
            self.gpa = 4
        else:
            self.gpa = value

    def get_letter(self):
        letter = ""
        if 0 <= self.gpa < 1:
            letter = "F"
        elif 1 <= self.gpa < 2:
            letter = "D"
        elif 2 <= self.gpa < 3:
            letter = "C"
        elif 3 <= self.gpa < 4:
            letter = "B"
        elif self.gpa == 4:
            letter = "A"
        else:
            pass
        return letter

    def set_letter(self, letter):
        possible_gpa = 0.0
        if letter == "A":
            possible_gpa = 4.0
        elif letter == "B":
            possible_gpa = 3.0
        elif letter == "C":
            possible_gpa = 2.0
        elif letter == "D":
            possible_gpa = 1.0
        elif letter == "F":
            possible_gpa = 0.0
        else:
            pass
        self.gpa = possible_gpa


def main():
    student = GPA()

    print("Initial values:")
    print("GPA: {:.2f}".format(student.get_gpa()))
    print("Letter: {}".format(student.get_letter()))

    value = float(input("Enter a new GPA: "))

    student.set_gpa(value)

    print("After setting value:")
    print("GPA: {:.2f}".format(student.get_gpa()))
    print("Letter: {}".format(student.get_letter()))

    letter = input("Enter a new letter: ")

    student.set_letter(letter)

    print("After setting letter:")
    print("GPA: {:.2f}".format(student.get_gpa()))
    print("Letter: {}".format(student.get_letter()))


if __name__ == "__main__":
    main()
