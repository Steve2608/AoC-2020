import re
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


if __name__ == '__main__':
    with open('13/input.txt', 'r') as in_file:
        # first line
        timestamp = int(in_file.readline())
        # second line
        constraints = in_file.readline()
        
        busses = list(map(int, re.findall(r'(\d+)', constraints)))
        busses_constrained = list(map(lambda x: None if x == 'x' else int(x), re.findall(r'((?:\d|x)+)', constraints)))

    print(part1(busses, timestamp))
    print(part2(busses_constrained))
