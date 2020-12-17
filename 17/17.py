from typing import Sequence
from functools import cached_property, partial
from copy import deepcopy


ACTIVE = '#'
INACTIVE ='.'

class PocketDimension3:

    def __init__(self, data: Sequence[Sequence[Sequence[int]]]):
        # no copy
        self._data = data

    @cached_property
    def x(self) -> int:
        return len(self._data[0][0])

    @cached_property
    def y(self) -> int:
        return len(self._data[0])

    @cached_property
    def z(self) -> int:
        return len(self._data)

    @cached_property
    def shape(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    def __getitem__(self, xyz: tuple[int, int, int]) -> int:
        x, y, z = xyz
        return self._data[z][y][x]

    def __getslice__(self, xyz: tuple[slice, slice, slice]):
        x, y, z = xyz
        return self._data[z][y][x]

    def __setitem__(self, xyz: tuple[int, int, int], value: int):
        x, y, z = xyz
        self._data[z][y][x] = value

    def next_gen(self) -> 'PocketDimension3':
        d = [[['.'] * (self.x + 2) for y in range(self.y + 2)] for z in range(self.z + 2)]
        next_gen = PocketDimension3(deepcopy(d))
        for z in range(self.z):
            for y in range(self.y):
                for x in range(self.x):
                    next_gen[x + 1, y + 1, z + 1] = self[x, y, z]

        for z in range(next_gen.z):
            for y in range(next_gen.y):
                for x in range(next_gen.x):
                    n = next_gen._neighbors(x, y, z)
                    if n == 3 or (n == 2 and next_gen[x, y, z] == ACTIVE):
                        d[z][y][x] = ACTIVE

        return PocketDimension3(d)

    def _neighbors(self, x: int, y: int, z: int) -> int:
        return sum(
            sum(
                sum(
                    e == ACTIVE for e in _x[max(x-1, 0):min(x+2, self.x)]
                ) 
                for _x in yx[max(y-1, 0):min(y+2, self.y)]
            ) 
            for yx in self._data[max(z-1, 0):min(z+2, self.z)]
        ) - (self[x, y, z] == ACTIVE)

    @property
    def active(self) -> int:
        return sum(sum(sum(e == ACTIVE for e in x) for x in yx) for yx in self._data)

    @property
    def inactive(self) -> int:
        return sum(sum(sum(e == INACTIVE for e in x) for x in yx) for yx in self._data)


class PocketDimension4:

    def __init__(self, data: Sequence[Sequence[Sequence[Sequence[int]]]]):
        # no copy
        self._data = data

    @cached_property
    def x(self) -> int:
        return len(self._data[0][0][0])

    @cached_property
    def y(self) -> int:
        return len(self._data[0][0])

    @cached_property
    def z(self) -> int:
        return len(self._data[0])

    @cached_property
    def w(self) -> int:
        return len(self._data)

    @cached_property
    def shape(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.z, self.w

    def __getitem__(self, xyzw: tuple[int, int, int, int]) -> int:
        x, y, z, w = xyzw
        return self._data[w][z][y][x]

    def __getslice__(self, xyzw: tuple[slice, slice, slice, slice]):
        x, y, z, w = xyzw
        return self._data[w][z][y][x]

    def __setitem__(self, xyzw: tuple[int, int, int, int], value: int):
        x, y, z, w = xyzw
        self._data[w][z][y][x] = value

    def next_gen(self) -> 'PocketDimension4':
        d = [[[['.'] * (self.x + 2) for y in range(self.y + 2)] for z in range(self.z + 2)] for w in range(self.w + 2)]
        next_gen = PocketDimension4(deepcopy(d))
        for w in range(self.w):
            for z in range(self.z):
                for y in range(self.y):
                    for x in range(self.x):
                        next_gen[x + 1, y + 1, z + 1, w + 1] = self[x, y, z, w]

        for w in range(next_gen.w):
            for z in range(next_gen.z):
                for y in range(next_gen.y):
                    for x in range(next_gen.x):
                        n = next_gen._neighbors(x, y, z, w)
                        if n == 3 or (n == 2 and next_gen[x, y, z, w] == ACTIVE):
                            d[w][z][y][x] = ACTIVE

        return PocketDimension4(d)

    def _neighbors(self, x: int, y: int, z: int, w: int) -> int:
        return sum(
            sum(
                sum(
                    sum(
                        e == ACTIVE for e in _x[max(x-1, 0):min(x+2, self.x)]
                    ) 
                    for _x in yx[max(y-1, 0):min(y+2, self.y)]
                ) 
                for yx in zyx[max(z-1, 0):min(z+2, self.z)]
            )
            for zyx in self._data[max(w-1, 0):min(w+2, self.w)]
        ) - (self[x, y, z, w] == ACTIVE)

    @cached_property
    def active(self) -> int:
        return sum(sum(sum(sum(e == ACTIVE for e in x) for x in yx) for yx in zyx) for zyx in self._data)

    @cached_property
    def inactive(self) -> int:
        return sum(sum(sum(sum(e == INACTIVE for e in x) for x in yx) for yx in zyx) for zyx in self._data)


def simulate_cycles(pd: PocketDimension3, cycles: int = 6) -> int:
    for _ in range(cycles):
        pd = pd.next_gen()
    return pd.active


example1 = partial(simulate_cycles, 
    pd=PocketDimension3([[list(line) for line in '.#.\n..#\n###'.splitlines()]]),
    cycles=0
)
example2 = partial(simulate_cycles, 
    pd=PocketDimension3([[list(line) for line in '.#.\n..#\n###'.splitlines()]]),
    cycles=1
)
example3 = partial(simulate_cycles, 
    pd=PocketDimension3([[list(line) for line in '.#.\n..#\n###'.splitlines()]]),
    cycles=2
)
example4 = partial(simulate_cycles, 
    pd=PocketDimension3([[list(line) for line in '.#.\n..#\n###'.splitlines()]]),
    cycles=3
)
example5 = partial(simulate_cycles, 
    pd=PocketDimension3([[list(line) for line in '.#.\n..#\n###'.splitlines()]]),
    cycles=6
)

example6 = partial(simulate_cycles,
    pd=PocketDimension4([[[list(line) for line in '.#.\n..#\n###'.splitlines()]]]),
    cycles=1
)
example7 = partial(simulate_cycles,
    pd=PocketDimension4([[[list(line) for line in '.#.\n..#\n###'.splitlines()]]]),
    cycles=2
)
example8 = partial(simulate_cycles,
    pd=PocketDimension4([[[list(line) for line in '.#.\n..#\n###'.splitlines()]]]),
    cycles=6
)


part1 = partial(simulate_cycles, cycles=6)
part2 = partial(simulate_cycles, cycles=6)


if __name__ == '__main__':
    assert example1() == 5
    assert example2() == 11
    assert example3() == 21
    assert example4() == 38
    assert example5() == 112

    assert example6() == 29
    assert example7() == 60
    assert example8() == 848

    with open('17/input.txt', 'r') as in_file:
        data = [[list(line) for line in in_file.read().strip().splitlines()]]

    print(part1(PocketDimension3(data)))
    print(part2(PocketDimension4([data])))
