list_1 = []
list_2 = []

with open("input.txt") as f:
    for line in f:
        o1, o2 = line.strip().split("   ")
        list_1.append(o1)
        list_2.append(o2)

score = 0

for i in range(len(list_1)):
    count = 0
    for j in range(len(list_2)):
        if(list_2[j] == list_1[i]):
            count += 1
    score += int(list_1[i]) * count


print(score)