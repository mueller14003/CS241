
count = {}

with open("census.csv", "r") as f:
    for line in f:
        words = line.split(',')
        key = words[3]
        if key not in count:
            count[key] = 1
        else:
            count[key] += 1

for key in count:
    print(count[key], "--", key)
