num = 0
den = 0
Mass = {}
ask = True
index = []
count = 0
prompt = "y"

while ask:
    if count != 0:
        prompt = input("Would you like to enter another object? (y / n): ")
    if prompt != "n" and prompt != "y":
        print("Invalid Response")
    elif prompt == "n":
        ask = False
    else:
        index.append(float(input("Please enter a location: ")))
        Mass[index[count]] = float(input("Please enter a mass for the {} location: ".format(index[count])))
        count += 1

for i in Mass:
    num += i * Mass[i]
    den += Mass[i]
c_of_m = num/den
print("Center of mass is: ", c_of_m)

# Finish by prompting user and having an interface with ability to quit
