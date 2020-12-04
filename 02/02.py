from dataclasses import dataclass
import re
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


if __name__ == '__main__':
    with open('02/input.txt', 'r') as in_file:
        data = [Password.from_string(line.replace('\n', '')) for line in in_file]

    print(part1(data))
    print(part2(data))