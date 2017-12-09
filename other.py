class BinaryError(Exception):
    def __str__(self):
        return "Not a valid binary number"


def bin2dec(input_string):
    r = 0
    for character in input_string:
        if character == '0':
            r = r * 2
        elif character == '1':
            r = r * 2 + 1
        else:
            raise BinaryError()
    return r


while True:
    try:
        print (bin2dec(input("Please enter a binary number: ")))
    except BinaryError:
        print ("Enter a Binary number. Please try again.\n")
    else:
        break