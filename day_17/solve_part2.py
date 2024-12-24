import math 

with open("input.txt") as f:
    lines = f.readlines()

initial_register = { 'A': 0, 'B': 0, 'C': 0}

for line in lines:
    if line.startswith("Register A: "):
        initial_register['A'] = int(line.replace('Register A: ', ''))
    elif line.startswith("Register B: "):
        initial_register['B'] = int(line.replace('Register B: ', ''))
    elif line.startswith("Register C: "):
        initial_register['C'] = int(line.replace('Register C: ', ''))
    elif line.startswith("Program:"):
        program = list(map(lambda x: int(x), line.replace("Program: ", '').split(',')))

def solve(a):
    instruction_pointer = 0
    output = []

    register = initial_register.copy()
    register['A'] = a

    while(instruction_pointer < len(program)):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        
        combo_operand = None
        result = None

        if(opcode in [0, 2, 5, 6, 7]):
            if operand < 4:
                combo_operand = operand
            elif operand == 4:
                combo_operand = register['A']
            elif operand == 5:
                combo_operand = register['B']
            elif operand == 6:
                combo_operand = register['C']
            elif operand == 7:
                raise

        skip_increment = False

        match opcode:
            case 0: #adv
                result = register['A'] / (2 ** combo_operand)
                register['A'] = int(math.floor(result))
            case 1: #bxl
                result = register['B'] ^ operand
                register['B'] = result
            case 2: #bst
                result = combo_operand % 8
                register['B'] = result
            case 3: #jnz
                if register['A'] != 0:
                    instruction_pointer = operand
                    skip_increment = True
            case 4: #bxc
                result = register['B'] ^ register['C']
                register['B'] = result
            case 5: #out
                result = combo_operand % 8
                output.append(result)
            case 6: #bdv
                result = register['A'] / (2 ** combo_operand)
                register['B'] = int(math.floor(result))
            case 7: #cdv
                result = register['A'] / (2 ** combo_operand)
                register['C'] = int(math.floor(result))

        if not skip_increment:
            instruction_pointer += 2

    return output

x = 1

for i in range(len(program)):
    for a in range(x, x + (8 ** (i + 1))):
        output = solve(a)
        if output == program[(- (i + 1)) :]:
            x = a
            break
    x = x * 8

result = math.floor(x / 8)
print(result)