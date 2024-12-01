list_1 = []
list_2 = []

with open("input.txt") as f:
    for line in f:
        o1, o2 = line.strip().split("   ")
        list_1.append(o1)
        list_2.append(o2)

list_1.sort()
list_2.sort()

sum = 0

for i in range(len(list_1)):
    sum += abs(int(list_1[i]) - int(list_2[i]))

print(sum)