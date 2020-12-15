from dataclasses import dataclass
from functools import partial
from math import prod
from typing import Sequence


@dataclass
class Vector:
    x: int
    y: int

    def __mod__(self, x: int) -> 'Vector':
        return Vector(self.x % x, self.y)

    def __mul__(self, mul: int) -> 'Vector':
        return Vector(self.x * mul, self.y * mul)


def part1(data: Sequence[Sequence[bool]], *, direction: Vector) -> int:
    return sum(data[p.y][p.x] for p in [(direction * i) % len(data[0]) for i in range(len(data) // direction.y)])


def part2(data: Sequence[Sequence[bool]], *, directions: Sequence[Vector]) -> int:
    return prod(part1(data, direction=di) for di in directions)


example1 = partial(part1, 
    data=[[ch == '#' for ch in line] for line in r"""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".splitlines()],
    direction=Vector(3, 1)
)
example2 = partial(part2, 
    data=[[ch == '#' for ch in line] for line in r"""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".splitlines()],
    directions=[Vector(1, 1), Vector(3, 1), Vector(5, 1), Vector(7, 1), Vector(1, 2)]
)


if __name__ == '__main__':
    assert example1() == 7
    assert example2() == 336

    with open('03/input.txt', 'r') as in_file:
        data = [[ch == '#' for ch in line] for line in in_file.read().strip().splitlines()]

    print(part1(data, direction=Vector(3, 1)))
    print(part2(data, directions=[Vector(1, 1), Vector(3, 1), Vector(5, 1), Vector(7, 1), Vector(1, 2)]))
