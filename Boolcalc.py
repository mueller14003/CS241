class Table:
    def __init__(self):
        self.variables = 1
        self.rows = 2
        self.row = [0,1]
        self.f = []
        self.var_names = ["A", "B", "C", "D", "E", "F"]

    def prompt(self):
        self.variables = int(input("How many variables? "))
        self.rows = self.variables ** 2

    def prompt_f(self):
        if self.variables == 1:
            print("{} | F".format(self.var_names[0]))
            self.f.append(int(input("{} | ".format(self.row[0]))))
            self.f.append(int(input("{} | ".format(self.row[1]))))
        elif self.variables == 2:
            print("A B | F")
            self.f.append(int(input("{0} {0} | ".format(self.row[0],self.row[1]))))
            self.f.append(int(input("{0} {1} | ".format(self.row[0], self.row[1]))))
            self.f.append(int(input("{1} {0} | ".format(self.row[0], self.row[1]))))
            self.f.append(int(input("{1} {1} | ".format(self.row[0], self.row[1]))))

    def equation(self):
        pass


def main():
    boolean = Table()
    boolean.prompt()
    boolean.prompt_f()


if __name__ == "__main__":
    main()
