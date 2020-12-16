import re
from collections import defaultdict
from math import prod
from typing import Sequence
from functools import partial


def parse_inputs(data: str) -> tuple[dict[str, tuple[range, range]], Sequence[Sequence[int]], Sequence[int]]:
    constraints = { name: (range(int(r1), int(r2) + 1), range(int(r3), int(r4) + 1))
        for name, r1, r2, r3, r4 in re.findall(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)', data)
    }
    nearby = [list(map(int, line.split(','))) for line in re.search(r'nearby tickets:\s+([\d+,\s+]+)', data).group(1).splitlines()]
    ticket = list(map(int, re.search(r'your ticket:\s+([\d+,]+)', data).group(1).split(',')))

    return constraints, nearby, ticket


def filter_invalid(constraints: dict[str, tuple[range, range]], nearby: Sequence[Sequence[int]]) -> tuple[int, Sequence[Sequence[int]]]:
    ranges = set()
    for r1, r2 in constraints.values():
        ranges = ranges.union(r1).union(r2)

    return sum(sum(value for value in near if value not in ranges) for near in nearby), \
        [near for near in nearby if all(value in ranges for value in near)]


def set_assignments(constraints: dict[str, tuple[range, range]], nearby: Sequence[Sequence[int]]) -> dict[str, int]:
    def is_possible_column(ranges: tuple[range, range], i: int) -> bool:
        r = set(ranges[0]).union(ranges[1])
        return all(near[i] in r for near in nearby)

    nearby = filter_invalid(constraints, nearby)[1]
    indices = len(constraints)

    # calculating all valid assignments
    valid_assignments = defaultdict(set)
    for key, ranges in constraints.items():
        for i in range(indices):
            if is_possible_column(ranges, i):
                valid_assignments[key].add(i)

    solutions = {}
    # one index is clear at a time
    for _ in range(indices):
        for key, assignments in valid_assignments.items():
            # find obvious solution
            if len(assignments) == 1:
                solutions[key] = assign = assignments.pop()

                # remove obvious solution from dictionary
                del valid_assignments[key]

                # remove assignment from all other keys
                for v in valid_assignments.values():
                    v.remove(assign)

                # obvious index found, next iteration
                break

    return solutions


def part1(constraints: dict[str, tuple[range, range]], nearby: Sequence[Sequence[int]]) -> int:
    return filter_invalid(constraints, nearby)[0]


def part2(constraints: dict[str, tuple[range, range]], nearby: Sequence[Sequence[int]], ticket: Sequence[int]) -> int:
    solutions = set_assignments(constraints, nearby)
    return prod(ticket[i] for k, i in solutions.items() if k.startswith('departure'))


example1 = partial(part1, 
    constraints={
        'class': (range(1, 4), range(5, 8)),
        'row': (range(6, 12), range(33, 45)),
        'seat': (range(13, 41), range(45, 51))
    },
    nearby=[
        [ 7, 3, 47],
        [40, 4, 50],
        [55, 2, 20],
        [38, 6, 12]
    ]
)
example2 = partial(set_assignments,
    constraints={
        'class': (range(0, 2), range(4, 20)),
        'row': (range(0, 6), range(8, 20)),
        'seat': (range(0, 14), range(16, 20))
    },
    nearby=[
        [ 3, 9, 18],
        [15, 1,  5],
        [ 5, 14, 9]
    ]  
)


if __name__ == '__main__':
    assert example1() == 71
    assert example2() == { 'row': 0, 'class': 1, 'seat': 2 }

    with open('16/input.txt', 'r') as in_file:
        constraints, nearby, ticket = parse_inputs(in_file.read().strip())
    
    print(part1(constraints, nearby))
    print(part2(constraints, nearby, ticket))
