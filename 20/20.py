import re
from typing import Optional, Union
from math import prod


def rotate_flip(data: Union[str, list[list[str]]], *, right_rotations: int = 0, flip: bool = False, 
                to_string: bool = False) -> Union[str, list[list[str]]]:
    if type(data) == str:
        data = [list(line) for line in data.splitlines()]
    for _ in range(right_rotations % 4):
        data = list(zip(*data[::-1]))
    if to_string:
        return '\n'.join(''.join(char for char in (line if not flip else reversed(line))) for line in data)
    else:
        return [list(line if not flip else reversed(line)) for line in data]


class Tile:

    def __init__(self, number: int, data: str, size: int):
        self._number = number
        self._data = [list(line[1:-1]) for line in data.splitlines()]
        del self._data[0]
        del self._data[-1]
        self._flip = False
        self._facing = 0

        self._edges = [
            data[:size],
            ''.join(data[(i * (size + 1)) + size - 1] for i in range(size)),
            data[-size:],
            ''.join(data[i * (size + 1)] for i in range(size)),
        ]

    @property
    def number(self) -> int:
        return self._number

    @property
    def data(self) -> str:
        return '\n'.join(''.join(char for char in line) for line in self._data)

    def rotate(self):
        self._facing = (self._facing + 1) % 4
        self._data = rotate_flip(self._data, right_rotations=1)
        self._edges = [
            self._edges[3][::-1],
            self._edges[0],
            self._edges[1][::-1],
            self._edges[2]
        ]


    def flip(self):
        self._flip = ~self._flip
        self._data = rotate_flip(self._data, flip=True)
        self._edges = [
            self._edges[0][::-1],
            self._edges[3],
            self._edges[2][::-1],
            self._edges[1]
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
            # print(f'x={x}, y={y}, tiles={tiles}\n{self}\n')
            if not tiles:
                return True

            for tile in tiles:
                subset = tiles.difference({tile})
                for _ in range(2):
                    for _ in range(4):
                        if self.try_set(x, y, tile) and insert((x + 1) % self.x, y + ((x + 1) // self.x), subset):
                            return True
                        tile.rotate()
                    tile.flip()

            self[x, y] = None
            return False

        insert(0, 0, tiles)
        # print(self)
        return prod(target.number for target in [self[0, 0], self[self.x - 1, 0], self[0, self.y - 1], self[self.x - 1, self.y - 1]])

    def image(self) -> str:
        s = ''
        for y in range(self.y):
            for i in range(len(self[0, y].data.splitlines())):
                for x in range(self.x):
                    s += self[x, y].data.splitlines()[i]
                s += '\n'
        return s
    
    def __str__(self):
        return '\n'.join(map(str, reversed(self._tiles)))


def find_seamonsters(data: str, sea_monster: str = r"""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """) -> int:
    mapper = lambda char: char == '#'

    lines = sea_monster.count('\n') + 1
    sea_monster_one = list(map(mapper, sea_monster.replace('\n', '')))
    smol = len(sea_monster_one) // lines

    count = 0
    for flip in (False, True):
        for rotate in (0, 1, 2, 3):
            rf_data = rotate_flip([list(line) for line in data.splitlines()], right_rotations=rotate, flip=flip, to_string=True)
            rf_lines = rf_data.splitlines()
            max_j, max_i = len(rf_lines) - lines, len(rf_lines[0]) - smol
            for j in range(max_j):
                for i in range(max_i):
                    target = list(map(mapper, rf_lines[j][i:i+smol] + rf_lines[j+1][i:i+smol] + rf_lines[j+2][i:i+smol]))
                    if target == sea_monster_one:
                        count += 1
    return count


def example1():
    with open('20/example1.txt', 'r') as in_file:
        return Grid(x=3, y=3).tile(set(map(Tile.from_string, in_file.read().strip().split('\n\n'))))


def example2():
    g = Grid(x=3, y=3)
    with open('20/example1.txt', 'r') as in_file, open('20/example2.txt', 'r') as target_file:
        g.tile(set(map(Tile.from_string, in_file.read().strip().split('\n\n'))))
        target = target_file.read()
    
    print(g)
    print(g[0, 0].data, g[1, 0].data, g[2, 0].data, sep='\n\n', end='\n\n')
    for flip in (False, True):
        for rotate in (0, 1, 2, 3):
            actual = rotate_flip(g.image(), right_rotations=rotate, flip=flip, to_string=True)
            print(actual, end='\n\n')
            if actual == target:
                print('True')
    return find_seamonsters(g.image())


if __name__ == '__main__':
    assert example1() == 20899048083289
    assert example2() == 2

    with open('20/input.txt', 'r') as in_file:
        tiles = set(map(Tile.from_string, in_file.read().strip().split('\n\n')))

    g = Grid(x=12, y=12)
    print(g.tile(tiles))
    image = g.image()
    print(find_seamonsters(image))
