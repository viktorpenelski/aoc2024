from typing import Counter
from aoc2024.utils import get_input

inp = get_input(1)

inp = inp.split('\n')
inp = filter(None, inp)
inp = (list(map(int, x.split())) for x in inp)
# zip left and right columns to separate lists
left, right = zip(*inp)
left = sorted(left)
right = sorted(right)

def distance(a, b):
    return abs(a - b)


# part one 
distances = list(map(distance, left, right))
print(sum(distances))

# part two
right = Counter(right)
score = sum(v*right.get(v, 0) for v in left)
print(score)