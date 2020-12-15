from functools import partial
from typing import Sequence


def part1(data: Sequence[str]) -> int:
    return sum(len(set(group.replace('\n', ''))) for group in data)


def part2(data: Sequence[str]) -> int:
    return sum(len(
        set((g := gr.split('\n'))[0]).intersection(*g[1:]) if '\n' in gr else set(gr)
    ) for gr in data)


example1 = partial(part1, data=['abcx\nabcy\nabcz'])
example2 = partial(part1, data=r"""abc

a
b
c

ab
ac

a
a
a
a

b""".split('\n\n'))

example3 = partial(part2, data=r"""abc

a
b
c

ab
ac

a
a
a
a

b""".split('\n\n'))


if __name__ == '__main__':
    assert example1() == 6
    assert example2() == 11
    assert example3() == 6

    with open('06/input.txt', 'r') as in_file:
        data = in_file.read().strip().split('\n\n')
    
    print(part1(data))
    print(part2(data))
