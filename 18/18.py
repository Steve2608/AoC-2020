import re
from typing import Sequence


class pint:
    """
    p(recedent)int
    precedence 2: __pow__ is overloaded with '+' (addition)
    precedence 1: __mul__ is overloaded with '*' (multiplication)
    precedence 1: __mod__ is overloaded with '+' (addition)
    """

    def __init__(self, value: int) -> 'pint':
        self.value = value

    def __pow__(self, other: 'pint') -> 'pint':
        return pint(self.value + other.value)

    def __mod__(self, other: 'pint') -> 'pint':
        return pint(self.value + other.value)

    def __mul__(self, other: 'pint') -> 'pint':
        return pint(self.value * other.value)

    def __int__(self) -> int:
        return self.value


def part1(data: Sequence[str]) -> int:
    # + equal to *
    # leave multiplication as is, change addition to modulo (overloaded with addition)
    return sum(int(eval(line.replace('+', '%'))) for line in data)


def part2(data: Sequence[str]) -> int:
    # + before *
    # leave multiplication as is, change addition to power (overloaded with addition)
    return sum(int(eval(line.replace('+', '**'))) for line in data)


if __name__ == '__main__':
    with open('18/input.txt', 'r') as in_file:
        data = [re.sub(r'(\d+)', r'pint(\1)', line) for line in in_file.read().strip().splitlines()]

    print(part1(data))
    print(part2(data))
