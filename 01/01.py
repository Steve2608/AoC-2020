from functools import partial
from typing import Sequence


def part1(data: Sequence[int], *, target: int = 2020) -> int:
    for a in data:
        for b in data:
            if a + b == target:
                return a * b


def part2(data: Sequence[int], *, target: int = 2020) -> int:
    for a in data:
        for b in data:
            if (part1 := a + b) >= target:
                continue
            for c in data:
                if part1 + c == target:
                    return a * b * c


example1 = partial(part1, data=[1721, 979, 366, 299, 675, 1456])
example2 = partial(part2, data=[1721, 979, 366, 299, 675, 1456])


if __name__ == '__main__':
    example1() == 876459
    example2() == 116168640
    
    with open('01/input.txt', 'r') as in_file:
        data = list(map(int, in_file))
    
    print(part1(data))
    print(part2(data))
