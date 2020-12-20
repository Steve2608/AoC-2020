import re
from typing import Optional, Union


def rotate_flip(data: Union[str, list[list[str]]], *, right_rotations: int = 0, flip: bool = False, 
                to_string: bool = False) -> Union[str, list[list[str]]]:
    # only when data is actually changed
    if right_rotations != 0 or flip:
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
        self._flip = False
        self._facing = 0

        self._data = [list(line[1:-1]) for line in data.splitlines()]
        del self._data[0]
        del self._data[-1]

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

    def _try_set(self, x: int, y: int, value: Tile) -> bool:
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
            if not tiles:
                return True

            for tile in tiles:
                subset = tiles.difference({tile})
                for _ in range(2):
                    for _ in range(4):
                        if self._try_set(x, y, tile) and insert((x + 1) % self.x, y + ((x + 1) // self.x), subset):
                            return True
                        tile.rotate()
                    tile.flip()

            self[x, y] = None
            return False

        insert(0, 0, tiles)
        return self[0, 0].number * self[self.x - 1, 0].number * \
                self[0, self.y - 1].number * self[self.x - 1, self.y - 1].number

    @property
    def image(self) -> str:
        s = ''
        for y in range(self.y):
            cache = { x: self[x, y].data.splitlines() for x in range(self.x) }
            for i in range(max_i := len(cache[0])):
                for x in range(self.x):
                    s += cache[x][max_i - (i + 1)]
                s += '\n'
        return s
    
    def __str__(self):
        return '\n'.join(map(str, self._tiles))


def count_waves_monsters(data: str, sea_monster: str = r"""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """) -> tuple[int, int]:
    monster_one_line = list(map(lambda c: c == '#', sea_monster.replace('\n', '')))
    y_span = sea_monster.count('\n') + 1
    x_span = len(monster_one_line) // y_span

    n_monsters = 0
    for flip in (False, True):
        for rotate in (0, 1, 2, 3):
            rf_lines = rotate_flip(data, right_rotations=rotate, flip=flip, to_string=True).splitlines()
            for y in range(len(rf_lines) - y_span):
                for x in range(len(rf_lines[0]) - x_span):
                    target = rf_lines[y][x:x+x_span] + rf_lines[y+1][x:x+x_span] + rf_lines[y+2][x:x+x_span]
                    if all(t == '#' for t, s in zip(target, monster_one_line) if s):
                        n_monsters += 1
            # monsters only are in ONE orientation
            if n_monsters != 0:
                return data.count('#') - sum(monster_one_line) * n_monsters, n_monsters
    return -1, -1


def count_waves(data: str, sea_monster: str = r"""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """) -> int:
    return count_waves_monsters(data, sea_monster)[0]


def example1():
    with open('20/example1.txt', 'r') as in_file:
        return Grid(x=3, y=3).tile(set(map(Tile.from_string, in_file.read().strip().split('\n\n'))))


def example2():
    gr = Grid(x=3, y=3)
    with open('20/example1.txt', 'r') as in_file:
        gr.tile(set(map(Tile.from_string, in_file.read().strip().split('\n\n'))))

    #with open('20/example2.txt', 'r') as target_file:
    #    expected = target_file.read().strip()
    
    #matched_once = False
    #for flip in (False, True):
    #    for rotate in (0, 1, 2, 3):
    #        if rotate_flip(gr.image, right_rotations=rotate, flip=flip, to_string=True) == expected:
    #            matched_once = True
    #            break
    #    if matched_once:
    #        break
    
    #assert matched_once
    return count_waves_monsters(gr.image)


if __name__ == '__main__':
    assert example1() == 20899048083289
    assert example2() == (273, 2)

    with open('20/input.txt', 'r') as in_file:
        tiles = set(map(Tile.from_string, in_file.read().strip().split('\n\n')))

    g = Grid(x=12, y=12)
    print(g.tile(tiles))
    print(count_waves(g.image))
