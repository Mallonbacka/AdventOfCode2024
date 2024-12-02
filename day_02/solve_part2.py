def main():
    with open("input.txt") as f:
        lines = f.readlines()

    lines = list(map(lambda t: t.strip(), lines))
    lines = list(map(lambda t: list(map(lambda n: int(n), t.split(" "))), lines))

    increasing_or_decreasing = [x for x in lines if all_increasing(x) or all_decreasing(x)]
    totally_safe = [x for x in increasing_or_decreasing if max_change(x) < 4]
    
    unsafe = [x for x in lines if x not in totally_safe]

    can_be_made_safe = [x for x in unsafe if can_be_safe(x)]

    print(len(totally_safe) + len(can_be_made_safe))

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

def can_be_safe(l):
    for i in (range(len(l))):
        new_l = [x for j,x in enumerate(l) if j!=i]
        if((all_increasing(new_l) or all_decreasing(new_l)) and max_change(new_l) < 4):
            return True
    return False 

main()
