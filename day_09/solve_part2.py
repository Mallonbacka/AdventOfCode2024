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
    expanded_length = len(expanded)
    expanded_rev = list(reversed(expanded))
    file_id = expanded[-1]
    while(file_id > 0):
        file_start = expanded.index(file_id)
        file_end = expanded_length - expanded_rev.index(file_id)
        file_length = file_end - file_start
        # Search from the start for file_length consecutive Nones
        block_start = 0
        block_end = 1
        while(block_end < file_end):
            if(expanded[block_end - 1] != None):
                block_start = block_end
            if(block_end - block_start == file_length):
                # Write the values
                for i in range(block_start, block_end):
                    expanded[i] = file_id
                # Write the empty space
                for i in range(file_start, file_end):
                    expanded[i] = None
                break
            block_end += 1
        file_id -= 1
    return expanded


def fragmented_p1(expanded):
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