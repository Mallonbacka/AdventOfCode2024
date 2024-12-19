import functools

with open("input.txt") as f:
    lines = f.readlines()

# Available towels
towels = list(sorted(map(lambda x: x.strip(), lines[0].strip().split(","))))
requests = list(map(lambda x: x.strip(), lines[2:]))

# Recursive function:
@functools.cache
def test_towels(prefix, request):
    results = []
    for towel in towels:
        if prefix + towel == request:
            results.append(1)
        elif request.startswith(prefix + towel):
            results.append(test_towels(prefix + towel, request))
    return sum(results)

counter = 0
for pattern in requests:
    counter += test_towels('', pattern)

print(counter)