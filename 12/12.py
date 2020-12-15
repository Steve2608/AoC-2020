import re
from functools import partial
from typing import Sequence, Tuple


class Vec2:

    def __init__(self, x: int, y: int) -> 'Vec2':
        self.x = x
        self.y = y

    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, times: int) -> 'Vec2':
        return Vec2(self.x * times, self.y * times)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __lshift__(self, amount: int) -> 'Vec2':
        return self.__rshift__(-amount)

    def __rshift__(self, amount: int) -> 'Vec2':
        rotation = (amount % 360) // 90
        if not (1 <= rotation <= 3):
            raise ValueError(f'Invalid rotation {amount}')

        if rotation == 1:
            return Vec2(self.y, -self.x)
        elif rotation == 2:
            return Vec2(-self.x, -self.y)
        else:
            return Vec2(-self.y, self.x)

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)


def part1(data: Sequence[Tuple[str, int]]) -> int:
    def move(direction: str, facing: str, length: int) -> Vec2:
        if direction == 'F':
            direction = facing
            
        if direction == 'E':
            return Vec2(length, 0)
        elif direction == 'S':
            return Vec2(0, -length)
        elif direction == 'W':
            return Vec2(-length, 0)
        elif direction == 'N':
            return Vec2(0, length)
        else: 
            raise ValueError(f'Invalid direction: {d}')

    movement_options = frozenset('ESWNF')
    directions, facing = 'ESWN', 'E'
    len_dir = len(directions)
    position = Vec2(0, 0)
    
    for d, l in data:
        if d in movement_options:
            position += move(d, facing, l)
        else:
            # only account for right rotations
            if d == 'R':
                rotation = l // 90
            elif d == 'L':
                rotation = -l // 90
            else:
                raise ValueError(f'Invalid rotation: {d}')
        
            facing = directions[(directions.index(facing) + rotation) % len_dir]

    return position.manhattan()


def part2(data: Sequence[Tuple[str, int]], *, waypoint: Vec2 = Vec2(10, 1)) -> int:
    def move(direction: str, length: int) -> Vec2:
        if direction == 'E':
            return Vec2(length, 0)
        elif direction == 'S':
            return Vec2(0, -length)
        elif direction == 'W':
            return Vec2(-length, 0)
        elif direction == 'N':
            return Vec2(0, length)
        else: 
            raise ValueError(f'Invalid direction: {d}')

    allowed_directions = frozenset('ESWN')    
    ship = Vec2(0, 0)
    for d, l in data:
        if d == 'F':
            ship += waypoint * l
        elif d in allowed_directions:
            waypoint += move(d, l)
        elif d == 'R':
            waypoint >>= l
        elif d == 'L':
            waypoint <<= l
        else:
            raise ValueError(f'Invalid rotation: {d}')

    return ship.manhattan()


example1 = partial(part1,
    data=[(d, int(l)) for d, l in re.findall(r'(F|E|S|W|N|R|L)(\d+)', 'F10\nN3\nF7\nR90\nF11')]
)
example2 = partial(part2,
    data=[(d, int(l)) for d, l in re.findall(r'(F|E|S|W|N|R|L)(\d+)', 'F10\nN3\nF7\nR90\nF11')],
    waypoint=Vec2(10, 1)
)


if __name__ == '__main__':
    assert example1() == 25
    assert example2() == 286

    with open('12/input.txt', 'r') as in_file:
        data = [(d, int(l)) for d, l in re.findall(r'(F|E|S|W|N|R|L)(\d+)', in_file.read())]

    print(part1(data))
    print(part2(data))
