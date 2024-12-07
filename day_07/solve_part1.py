import itertools
from functools import reduce
from operator import mul

def main():
    with open("input.txt") as f:
        lines = f.readlines()

    expressions = list(map(parse_line, lines))
    print(sum(map(solvable, expressions)))

def parse_line(line):
    split_line = line.split(": ")
    return { "target": int(split_line[0]), "numbers": list(map(int, split_line[1].strip().split(" "))) }

def solvable(x):
    for comb in itertools.product(["+", "*"], repeat = len(x["numbers"]) - 1):
        expression = list([x for x in itertools.chain.from_iterable(itertools.zip_longest(x["numbers"], comb)) if x])
        result = reduce(sequential_eval, itertools.batched(expression[1:], n=2), int(expression[0]))
        if(result == x["target"]):
            return x["target"]

    return 0

def sequential_eval(start, operation):
    if(operation[0] == "+"):
        return start + int(operation[1])
    elif(operation[0] == "*"):
        return start * int(operation[1])

main()