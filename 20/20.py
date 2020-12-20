import re
from typing import Optional
from functools import partial
from math import prod


class Tile:

    def __init__(self, number: int, data: str, size: int):
        self._number = number
        self._data = data
        self._facing = 0
        self._format = f'{{:0{size}b}}'

        self._edges = [
            self._string_to_int(data[:size]),
            self._string_to_int(''.join(data[(i * (size + 1)) + size - 1] for i in range(size))),
            self._string_to_int(data[-size:]),
            self._string_to_int(''.join(data[i * (size + 1)] for i in range(size))),
        ]

    def _string_to_int(self, string: str) -> int:
        return sum(2**i for i, e in enumerate(reversed(string)) if e == '#')

    @property
    def number(self) -> int:
        return self._number

    @property
    def data(self) -> str:
        return self._data

    def rotate_right(self):
        self._facing = (self._facing + 1) % 4
        self._edges = [self._edges[3]] + self._edges[:3]

    def flip_x(self):
        self._edges = [
            int(self._format.format(self._edges[0])[::-1], base=2),
            self._edges[3],
            int(self._format.format(self._edges[2])[::-1], base=2),
            self._edges[1]
        ]

    def flip_y(self):
        self._edges = [
            self._edges[2],
            int(self._format.format(self._edges[1])[::-1], base=2),
            self._edges[0],
            int(self._format.format(self._edges[3])[::-1], base=2)
        ]

    @property
    def top(self) -> int:
        return self._edges[0]

    @property
    def right(self) -> int:
        return self._edges[1]

    @property
    def bottom(self) -> int:
        return self._edges[2]

    @property
    def left(self) -> int:
        return self._edges[3]

    @classmethod
    def from_string(cls, string: str, size: int = 10):
        tile, field = string.split('\n', 1)
        return cls(int(re.match('Tile (\d+):', tile).group(1)), field.strip(), size)
    
    def __str__(self) -> str:
        return f'{self.number:04d}'

    __repr__ = __str__


class Grid:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._tiles = [[None for _ in range(self.x)] for _ in range(self.y)]

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __getitem__(self, coord: tuple[int, int]) -> Optional[Tile]:
        x, y = coord
        return self._tiles[y][x] if (0 <= x < self.x and 0 <= y < self.y) else None

    def __setitem__(self, coord: tuple[int, int], value: Optional[Tile]):
        x, y = coord
        if 0 <= x < self.x and 0 <= y < self.y:
            self._tiles[y][x] = value
        else: 
            raise IndexError(f'{x, y} out of bounds for {self.x, self.y}')

    def try_set(self, x: int, y: int, value: Tile) -> bool:
        if 0 <= x < self.x and 0 <= y < self.y:
            #if (up := self[x, y + 1]) is not None and up.bottom != value.top:
            #    return False
            #if (right := self[x + 1, y]) is not None and right.left != value.right:
            #    return False
            if (down := self[x, y - 1]) is not None and down.top != value.bottom:
                return False
            if (left := self[x - 1, y]) is not None and left.right != value.left:
                return False

            self[x, y] = value
            return True
        return False

    def tile(self, tiles: set[Tile]) -> int:
        def insert(x: int, y: int, tiles: set[Tile]) -> bool:
            print(f'x={x}, y={y}, tiles={tiles}\n{self}\n')
            if not tiles:
                return True

            for tile in tiles:
                subset = tiles.difference({tile})
                for _ in range(2):
                    for _ in range(2):
                        for _ in range(4):
                            if self.try_set(x, y, tile) and insert((x + 1) % self.x, y + ((x + 1) // self.x), subset):
                                return True
                            tile.rotate_right()
                        tile.flip_x()
                    tile.flip_y()

            self[x, y] = None
            return False

        insert(0, 0, tiles)
        print(self)
        return prod(target.number for target in [self[0, 0], self[self.x - 1, 0], self[0, self.y - 1], self[self.x - 1, self.y - 1]])
    
    def __str__(self):
        return '\n'.join(map(str, reversed(self._tiles)))


def example1():
    return Grid(x=3, y=3).tile(
        set(map(Tile.from_string, r"""Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".strip().split('\n\n'))))


if __name__ == '__main__':
    assert example1() == 20899048083289

    with open('20/input.txt', 'r') as in_file:
        tiles = set(map(Tile.from_string, in_file.read().strip().split('\n\n')))

    g = Grid(x=12, y=12)
    g.tile(tiles)
