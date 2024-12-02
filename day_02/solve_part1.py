def main():
    with open("input.txt") as f:
        lines = f.readlines()

    lines = list(map(lambda t: t.strip(), lines))
    lines = list(map(lambda t: list(map(lambda n: int(n), t.split(" "))), lines))

    increasing_or_decreasing = [x for x in lines if all_increasing(x) or all_decreasing(x)]
    with_max_change = [x for x in increasing_or_decreasing if max_change(x) < 4]
    
    print(len(with_max_change))

def all_increasing(l):
    for i in (range(len(l) - 1)):
        if(l[i] >= l[i + 1]):
            return False
    
    return True

def all_decreasing(l):
    for i in (range(len(l) - 1)):
        if(l[i] <= l[i + 1]):
            return False
    
    return True

def max_change(l):
    biggest_max = 0
    for i in (range(len(l) - 1)):
        biggest_max = max(abs(l[i] - l[i+1]), biggest_max)
    
    return biggest_max 


main()
