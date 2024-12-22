import math 
import sys

initial_a = int(sys.argv[1], 8)
a = initial_a
print("a (decimal):", a)

print("Target: 16")
result = []
target = [2,4,1,7,7,5,0,3,4,4,1,7,5,5,3,0]
print("Result: ", end="")
while a > 0:
    #print("  a =", a)
    # 2,4: b = a mod 8 
    b = a % 8
    #print(" ", b)
    #print("  b =", b)
    # 1,7: b = b ^ 7
    b = b ^ 7
    #print("  b =", b)
    # 7,5: c = floor(a / (2 ** b))
    c = math.floor(a / (2 ** b))
    #print("  c =", c)
    # 0,3: a = floor(a / 8)
    a = math.floor(a / 8)
    #print("  a =", a)
    # 4,4: b = b ^ c
    b = b ^ c
    #print("  b =", b)
    # 1,7: b = b ^ 7
    b = b ^ 7
    #print("  b =", b)
    # 5,5: out(b % 8)
    result.append(b % 8)
print(result)
