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

    def display(self):
        print("$$$ LOOK AT MY STACKS $$$")
        index = 0
        # TODO: later
        while index < self.top:
            index += 1
            print(self.list[-index])


def main():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.pop()
    stack.push(3)
    stack.push(4)
    stack.pop()
    stack.push(5)
    stack.pop()
    stack.pop()
    stack.push(6)
    stack.push(7)
    stack.pop()
    stack.display()


if __name__ == "__main__":
    main()
