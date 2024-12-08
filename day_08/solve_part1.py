import itertools


def main():
    with open("input.txt") as f:
        lines = f.readlines()
    all_nodes = collate_nodes(lines)
    antinodes = in_range(get_antinodes(all_nodes), lines)
    #print_results(antinodes, lines)
    print(set(antinodes))
    print(len(set(antinodes)))

def collate_nodes(lines):
    nodes = {}
    for y in range(len(lines)):
        for x in range(len(lines[0]) - 1):
            if(lines[y][x] != '.'):
                nodes.setdefault(str(lines[y][x]), []).append((x, y))
    return nodes

def get_antinodes(nodes):
    all_antinodes = []
    for key in nodes:
        for pair in itertools.combinations(nodes[key], 2):
            x_diff = pair[0][0] - pair[1][0]
            y_diff = pair[0][1] - pair[1][1]
            all_antinodes.append((pair[0][0] + x_diff, pair[0][1] + y_diff))
            all_antinodes.append((pair[1][0] - x_diff, pair[1][1] - y_diff))
    return all_antinodes

def in_range(nodes, lines): 
    max_y = len(lines)
    max_x = len(lines[0]) - 1
    return [x for x in nodes if x[0] >= 0 and x[1] >= 0 and x[0] < max_x and x[1] < max_y]

def print_results(nodes, lines):
    for node in nodes:
        lines[node[1]] = lines[node[1]][:node[0]] + '#' + lines[node[1]][node[0] + 1:]

    for line in lines:
        print(line)
main()