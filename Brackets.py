class Stack:
    def __init__(self):
        self.list = []
        self.top = 0

    def push(self, item):
        self.list.append(item)
        self.top += 1

    def pop(self):
        self.list.pop()
        self.top -= 1


class File:
    def __init__(self):
        self.filename = ''
        self.file = Stack()
        self.balanced = True

    def prompt(self):
        self.filename = input("Enter a filename: ")

    def open_file(self):
        count = 0
        with open(self.filename, "r") as f:
            for i in f:
                line = i.split()
                self.file.push(line)
                if self.file.list[count] == "(":
                    if line == ")":
                        self.file.pop()
                    elif line != ")":
                        if line == "(" or "{" or "[":
                            self.file.push(line)
                        else:
                            self.balanced = False
                elif self.file.list[count] == "{":
                    if line == "}":
                        self.file.pop()
                    elif line != "}":
                        if line == "(" or "{" or "[":
                            self.file.push(line)
                        else:
                            self.balanced = False
                elif self.file.list[count] == "[":
                    if line == "]":
                        self.file.pop()
                    elif line != "]":
                        if line == "(" or "{" or "[":
                            self.file.push(line)
                        else:
                            self.balanced = False
                else:
                    self.balanced = False
                count += 1

        if len(self.file.list) != 0:
            self.balanced = False


def main():
    file = File()
    file.prompt()
    file.open_file()
    if file.balanced:
        print("Balanced")
    else:
        print("Not balanced")


if __name__ == "__main__":
    main()
