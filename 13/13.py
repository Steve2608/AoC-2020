import re
from functools import partial
from math import prod
from typing import Optional, Sequence


def part1(busses: Sequence[int], timestamp: int) -> int:
    waiting, best_id = timestamp, -1
    for i, bus in enumerate(busses):
        if (curr := bus - (timestamp % bus)) < waiting:
            waiting = curr
            best_id = i
        
    return busses[best_id] * waiting


def chinese_remainder_theorem(n: Sequence[int], a: Sequence[int], *, verbose: bool = False) -> int:
    m = prod(n)
    if verbose:
        print(f'm={m}')

    x = 0
    for i, (n_i, a_i) in enumerate(zip(n, a), 1):
        z_i = m // n_i
        y_i = pow(z_i % n_i, -1, mod=n_i)
        w_i = (y_i * z_i) % m
        x += a_i * w_i

        if verbose:
            print(f'z_{i} = {z_i}, y_{i} = {y_i}, w_{i} = {w_i}')
         
    return x % m

def part2(busses: Sequence[Optional[int]]) -> int:
    n = [bus for bus in busses if bus is not None]
    a = [bus - i for i, bus in enumerate(busses) if bus is not None]
    return chinese_remainder_theorem(n, a)


example1 = partial(part1, busses=[7, 13, 59, 31, 19], timestamp=939)
example2 = partial(part2, busses=[7, 13, None, None, 59, None, 31, 19])
example3 = partial(part2, busses=[17, None, 13, 19])
example4 = partial(part2, busses=[67, 7, 59, 61])
example5 = partial(part2, busses=[67, None, 7, 59, 61])
example6 = partial(part2, busses=[67, 7, None, 59, 61])
example7 = partial(part2, busses=[1789, 37, 47, 1889])


if __name__ == '__main__':
    assert example1() == 295
    assert example2() == 1068781
    assert example3() == 3417
    assert example4() == 754018
    assert example5() == 779210
    assert example6() == 1261476
    assert example7() == 1202161486

    with open('13/input.txt', 'r') as in_file:
        # first line
        timestamp = int(in_file.readline())
        # second line
        constraints = in_file.readline()
        
        busses = list(map(int, re.findall(r'(\d+)', constraints)))
        busses_constrained = list(map(lambda x: None if x == 'x' else int(x), re.findall(r'((?:\d|x)+)', constraints)))

    print(part1(busses, timestamp))
    print(part2(busses_constrained))
