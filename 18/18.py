import re
from functools import partial
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


def convert_input(line: str) -> str:
    return re.sub(r'(\d+)', r'pint(\1)', line)


def part1(data: Sequence[str]) -> int:
    # + equal to *
    # leave multiplication as is, change addition to modulo (overloaded with addition)
    return sum(int(eval(line.replace('+', '%'))) for line in data)


def part2(data: Sequence[str]) -> int:
    # + before *
    # leave multiplication as is, change addition to power (overloaded with addition)
    return sum(int(eval(line.replace('+', '**'))) for line in data)


example1 = partial(part1, data=[convert_input('1 + 2 * 3 + 4 * 5 + 6')])
example2 = partial(part1, data=[convert_input('1 + (2 * 3) + (4 * (5 + 6))')])
example3 = partial(part1, data=[convert_input('2 * 3 + (4 * 5)')])
example4 = partial(part1, data=[convert_input('5 + (8 * 3 + 9 + 3 * 4 * 3)')])
example5 = partial(part1, data=[convert_input('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')])
example6 = partial(part1, data=[convert_input('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')])

example7 = partial(part2, data=[convert_input('1 + 2 * 3 + 4 * 5 + 6')])
example8 = partial(part2, data=[convert_input('1 + (2 * 3) + (4 * (5 + 6))')])
example9 = partial(part2, data=[convert_input('2 * 3 + (4 * 5)')])
example10 = partial(part2, data=[convert_input('5 + (8 * 3 + 9 + 3 * 4 * 3)')])
example11 = partial(part2, data=[convert_input('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')])
example12 = partial(part2, data=[convert_input('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')])


if __name__ == '__main__':
    assert example1() == 71
    assert example2() == 51
    assert example3() == 26
    assert example4() == 437
    assert example5() == 12240
    assert example6() == 13632

    assert example7() == 231
    assert example8() == 51
    assert example9() == 46
    assert example10() == 1445
    assert example11() == 669060
    assert example12() == 23340

    with open('18/input.txt', 'r') as in_file:
        data = list(map(convert_input, in_file.read().strip().splitlines()))

    print(part1(data))
    print(part2(data))
