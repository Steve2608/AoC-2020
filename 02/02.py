from functools import partial
import re
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Password:
    i1: int
    i2: int
    needle: str
    haystack: str

    @classmethod
    def from_string(cls, string: str) -> 'Password':
        match = re.fullmatch(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', string)
        return cls(int(match.group(1)), int(match.group(2)), match.group(3), match.group(4))


def part1(data: Sequence[Password]) -> int:
    return sum(p.i1 <= p.haystack.count(p.needle) <= p.i2 for p in data)


def part2(data: Sequence[Password]) -> int:
    return sum((p.haystack[p.i1 - 1] == p.needle) != (p.needle == p.haystack[p.i2 - 1]) for p in data)


example1 = partial(part1, data=list(map(Password.from_string, r"""1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".splitlines())))

example2 = partial(part2, data=list(map(Password.from_string, r"""1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".splitlines())))


if __name__ == '__main__':
    assert example1() == 2
    assert example2() == 1

    with open('02/input.txt', 'r') as in_file:
        data = list(map(Password.from_string, in_file.read().strip().splitlines()))

    print(part1(data))
    print(part2(data))
