numbers = []
for i in range(26):
    numbers.append(i*2)
print(numbers)

###########

numbers2 = [x*2 for x in range(26)]
numbers3 = [x for x in range(51) if x%2==0]
print(numbers2)
print(numbers3)
numbers4 = [i for i in range(100) if i%4 == 0 or i%5 == 0]
print(numbers4)
