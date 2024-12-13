import re
import csv
filename = "input"

with open(filename + ".txt") as f:
    lines = f.readlines()

with open(filename + '.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["effect_a_x", "effect_a_y", "effect_b_x", "effect_b_y", "prize_x", "prize_y"])
	newline = []
	for line in lines:
		if line.startswith("Button A"):
			m = re.match("Button A: X([+-][0-9]+), Y([+-][0-9]+)$", line)
			newline = [
			m.group(1), m.group(2)
			]
		elif line.startswith("Button B"):
			m = re.match("Button B: X([+-][0-9]+), Y([+-][0-9]+)$", line)
			newline.append(m.group(1))
			newline.append(m.group(2))
		elif line.startswith("Prize:"):
			m = re.match("Prize: X=([0-9]+), Y=([0-9]+)$", line)
			newline.append(m.group(1))
			newline.append(m.group(2))
			writer.writerow(newline)
		