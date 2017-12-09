class GPA:
    def __init__(self):
        self._gpa = 0.0

    @property
    def gpa(self):
        if self._gpa < 0:
            return 0
        elif self._gpa > 4:
            return 4
        else:
            return self._gpa

    @gpa.setter
    def gpa(self, value):
        if value < 0:
            self._gpa = 0
        elif value > 4:
            self._gpa = 4
        else:
            self._gpa = value

    @property
    def letter(self):
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

    @letter.setter
    def letter(self, letter):
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
    print("GPA: {:.2f}".format(student.gpa))
    print("Letter: {}".format(student.letter))

    value = float(input("Enter a new GPA: "))

    student.gpa = value

    print("After setting value:")
    print("GPA: {:.2f}".format(student.gpa))
    print("Letter: {}".format(student.letter))

    letter = input("Enter a new letter: ")

    student.letter = letter

    print("After setting letter:")
    print("GPA: {:.2f}".format(student.gpa))
    print("Letter: {}".format(student.letter))


if __name__ == "__main__":
    main()
