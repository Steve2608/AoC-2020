import re
from functools import partial
from typing import Literal, Sequence


class HexCoordinate:

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self._x = x
        self._y = y
        self._z = z

    @property
    def xyz(self) -> tuple[int, int, int]:
        return self._x, self._y, self._z

    def move(self, direction: Literal['e', 'se', 'sw', 'w', 'nw', 'ne']) -> None:
        if direction == 'e':
            self._x += 1
            self._y -= 1
        elif direction == 'w':
            self._x -= 1
            self._y += 1
        elif direction == 'sw':
            self._x -= 1
            self._z += 1
        elif direction == 'ne':
            self._x += 1
            self._z -= 1
        elif direction == 'se':
            self._y -= 1
            self._z += 1
        else:
            self._y += 1
            self._z -= 1

    def neighbor_coords(self) -> tuple[tuple[int, int, int], ...]:
        return (self._x + 1, self._y - 1, self._z), \
            (self._x - 1, self._y + 1, self._z), \
            (self._x - 1, self._y, self._z + 1), \
            (self._x + 1, self._y, self._z - 1), \
            (self._x, self._y - 1, self._z + 1), \
            (self._x, self._y + 1, self._z - 1)


def fill_floor(lines: Sequence[tuple[str]]) -> dict[tuple[int, int, int], bool]:
    # true equals black side up
    grid = {}

    for line in lines:
        curr = HexCoordinate()
        for direction in line:
            curr.move(direction)
        
        # flip tile
        coords = curr.xyz
        grid[coords] = not grid.get(coords, False)

    return grid


def part1(lines: Sequence[tuple[str]]) -> int:
    return sum(fill_floor(lines).values())


def part2(lines: Sequence[tuple[str]], days: int) -> int:
    def expand_floor(grid: dict[tuple[int, int, int], bool]) -> dict[tuple[int, int, int], bool]:
        expanded = grid.copy()
        for coords, is_black in grid.items():
            if is_black:
                for dest in HexCoordinate(*coords).neighbor_coords():
                    expanded[dest] = grid.get(dest, False)

        return expanded

    prev_gen = fill_floor(lines)
    for _ in range(days):
        prev_gen = expand_floor(prev_gen)
        next_gen = prev_gen.copy()
        for coords, is_black in prev_gen.items():
            neighbors = sum(prev_gen.get(neighbor, False) for neighbor in HexCoordinate(*coords).neighbor_coords())
            if is_black:
                if neighbors == 0 or neighbors > 2:
                    next_gen[coords] = False
            else:
                if neighbors == 2:
                    next_gen[coords] = True
        
        prev_gen = next_gen

    return sum(prev_gen.values())


example1 = partial(part1, lines=[tuple(re.findall(r'e|se|sw|w|nw|ne', line)) for line in r"""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines()])

example2 = partial(part2, lines=[tuple(re.findall(r'e|se|sw|w|nw|ne', line)) for line in r"""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines()])


if __name__ == '__main__':
    assert example1() == 10

    assert example2(days=1) == 15
    assert example2(days=2) == 12
    assert example2(days=3) == 25
    assert example2(days=4) == 14
    assert example2(days=5) == 23
    assert example2(days=6) == 28
    assert example2(days=7) == 41
    assert example2(days=8) == 37
    assert example2(days=9) == 49
    assert example2(days=10) == 37
    assert example2(days=20) == 132
    assert example2(days=30) == 259
    assert example2(days=40) == 406
    assert example2(days=50) == 566
    assert example2(days=60) == 788
    assert example2(days=70) == 1106
    assert example2(days=80) == 1373
    assert example2(days=90) == 1844
    assert example2(days=100) == 2208

    with open('24/input.txt', 'r') as in_file:
        lines = [tuple(re.findall(r'e|se|sw|w|nw|ne', line)) for line in in_file.read().strip().splitlines()]

    print(part1(lines))
    print(part2(lines, days=100))
