import copy
from dataclasses import dataclass
from multiprocessing import Pool

from aoc2024.utils import get_input


_inp = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

_inp = get_input(6)

@dataclass(frozen=True)
class Pos:
    row: int
    col: int
    
    def plus(self, pos: 'Pos') -> 'Pos':
        return Pos(self.row + pos.row, self.col + pos.col)        

def parse_input(input_str: str) -> list[list[str]]:
    return [list(c) for c in input_str.split('\n')]

def find_start(inp: list[list[str]]) ->Pos:
    for row in range(len(inp)):
        for col in  range(len(inp[row])):
            if inp[row][col] == '^':
                return Pos(row, col)

def is_in_bounds(pos: Pos, inp: list[list[str]]) -> bool:
    return pos.row >= 0 and pos.row < len(inp) and pos.col >= 0 and pos.col < len(inp[pos.row])

def is_solid(pos: Pos, inp: list[list[str]]) -> bool:
    return inp[pos.row][pos.col] == '#'

def get_direction(guard: Pos) -> Pos:
    if guard == '^':
        direction = Pos(-1, 0)
    elif guard == 'v':
        direction = Pos(1, 0)
    elif guard == '>':
        direction = Pos(0, 1)
    else:
        direction = Pos(0, -1)
    return direction

def rotate_right(guard_str: str) -> str:
    if guard_str == '^':
        return '>'
    elif guard_str == '>':
        return 'v'
    elif guard_str == 'v':
        return '<'
    else:
        return '^'
    
def move(guard_pos: Pos, inp: list[list[str]]) -> set[Pos]:
    visited = set()
    while(True):
        guard_symbol = inp[guard_pos.row][guard_pos.col]
        direction = get_direction(guard_symbol)
        next = guard_pos.plus(direction)

        if not is_in_bounds(next, inp):
            visited.add(guard_pos)
            return visited
        if is_solid(next, inp):
            inp[guard_pos.row][guard_pos.col] = rotate_right(guard_symbol)
        else:
            inp[guard_pos.row][guard_pos.col] = '.'
            inp[next.row][next.col] = guard_symbol
            visited.add(guard_pos)
            guard_pos = next
            
            
def try_loop(guard_pos: Pos, inp: list[list[str]]) -> bool:
    visited = set()
    while(True):
        guard_symbol = inp[guard_pos.row][guard_pos.col]

        if (guard_pos, guard_symbol) in visited:
            return True

        direction = get_direction(guard_symbol)
        next = guard_pos.plus(direction)

        visited.add((guard_pos, guard_symbol))
        if not is_in_bounds(next, inp):
            return False
        if is_solid(next, inp):
            inp[guard_pos.row][guard_pos.col] = rotate_right(guard_symbol)
        else:
            inp[guard_pos.row][guard_pos.col] = '.'
            inp[next.row][next.col] = guard_symbol
            guard_pos = next


def print_grid(inp: list[list[str]]) -> None:
    for row in range(len(inp)):
        print(inp[row])
    print('\n\n')


# part 1
parsed_input = parse_input(_inp)
start = find_start(parsed_input)
print(start)
visited = move(start, copy.deepcopy(parsed_input))
print(len(visited))

# part 2
def paradoxify(pos: Pos, inp: list[list[str]]) -> list[list[str]] | None:
    if parsed_input[pos.row][pos.col] == '.':
        paradox_obstruction = copy.deepcopy(parsed_input)
        paradox_obstruction[pos.row][pos.col] = '#'
        return paradox_obstruction
    return None

tasks = [(Pos(row, col), parsed_input) for row in range(len(parsed_input)) for col in range(len(parsed_input[row]))]
with Pool(16) as p:
    grids = p.starmap(paradoxify, tasks)
    all_grids = [x for x in grids if x is not None]

print(len(all_grids))

tasks =  [(start, grid) for grid in all_grids]
with Pool(16) as p:
    loops = p.starmap(try_loop, tasks)
    print(loops.count(True))