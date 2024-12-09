import itertools

def main():
    with open("input.txt") as f:
        lines = f.readlines()
    print(checksum(fragmented(expanded_layout(lines[0]))))
    
def expanded_layout(input):
    data = []
    file_id = 0
    for i, char in enumerate(input):
        if(i % 2 == 1):
            # Even number, write blank space
            for i in range(int(char)):
                data.append(None)
        else:
            # Odd number, write values
            for i in range(int(char)):
                data.append(file_id)
            file_id += 1
    return data

def fragmented(expanded):
    end_index = len(expanded) - 1
    for i in range(len(expanded)):
        if expanded[i] == None:
            expanded[i] = expanded[end_index]
            expanded[end_index] = None
            while(expanded[end_index] == None):
                end_index -= 1
        if(i >= end_index):
            break
    return expanded

def checksum(expanded):
    return sum([x * i for i, x in enumerate(expanded) if x != None])

main()