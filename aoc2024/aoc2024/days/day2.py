from aoc2024.utils import get_input


inp = get_input(2)

def parse_input(input: str) -> list[list[int]]:
    inp = input.split('\n')
    inp = filter(None, inp)
    inp = (list(map(int, x.split())) for x in inp)
    return list(inp)


input = parse_input(inp)


def is_safe(x: list[int]) -> bool:
    fn_increasing = lambda a, b: a < b and b - a <= 3
    fn_decreasing = lambda a, b: a > b and a - b <= 3
    return all(map(fn_increasing, x[:-1], x[1:])) or all(map(fn_decreasing, x[:-1], x[1:]))

def part1(input: list[list[int]]) -> int:
    return sum(
        is_safe(x)
        for x in input
    )

print(part1(input))

def part2(input: list[list[int]]) -> int:
    safe = 0
    for x in input:
        for i in range(len((x))):
            if is_safe(x[:i] + x[i+1:]):
                safe += 1
                break
    return safe
            


print(part2(input))