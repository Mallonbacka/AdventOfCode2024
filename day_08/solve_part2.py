import itertools


def main():
    with open("input.txt") as f:
        lines = f.readlines()
    x_lim = len(lines[0]) - 1
    y_lim = len(lines)
    all_nodes = collate_nodes(lines)
    antinodes = in_range(get_antinodes(all_nodes, x_lim, y_lim), lines)
    # print_results(antinodes, lines)
    print(len(set(antinodes)))

def collate_nodes(lines):
    nodes = {}
    for y in range(len(lines)):
        for x in range(len(lines[0]) - 1):
            if(lines[y][x] != '.'):
                nodes.setdefault(str(lines[y][x]), []).append((x, y))
    return nodes

def get_antinodes(nodes, x_lim, y_lim):
    all_antinodes = []
    for key in nodes:
        for pair in itertools.combinations(nodes[key], 2):
            x_diff = pair[0][0] - pair[1][0]
            y_diff = pair[0][1] - pair[1][1]
            new_node_start = (pair[0][0], pair[0][1])
            while(new_node_start[0] >= 0 and new_node_start[0] < x_lim and new_node_start[1] >= 0 and new_node_start[1] < y_lim):
                all_antinodes.append((new_node_start[0], new_node_start[1]))
                new_node_start = (new_node_start[0] + x_diff, new_node_start[1] + y_diff)
            new_node_end = (pair[1][0], pair[1][1])
            while(new_node_end[0] >= 0 and new_node_end[0] < x_lim and new_node_end[1] >= 0 and new_node_end[1] < y_lim):
                all_antinodes.append((new_node_end[0], new_node_end[1]))
                new_node_end = (new_node_end[0] - x_diff, new_node_end[1] - y_diff)
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