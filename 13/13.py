import re
from typing import Optional, Sequence


def part1(busses: Sequence[int], timestamp: int) -> int:
    waiting, best_id = timestamp, -1
    for i, bus in enumerate(busses):
        if (curr := bus - (timestamp % bus)) < waiting:
            waiting = curr
            best_id = i
        
    return busses[best_id] * waiting


def part2(busses: Sequence[Optional[int]]) -> int:
    # TODO
    pass


if __name__ == '__main__':
    with open('13/input.txt', 'r') as in_file:
        # first line
        timestamp = int(in_file.readline())
        # second line
        constraints = in_file.readline()
        
        busses = list(map(int, re.findall(r'(\d+)', constraints)))
        # busses_constrained = list(map(lambda x: None if x == 'x' else int(x), re.findall(r'((?:\d|x)+)', constraints)))

    print(part1(busses, timestamp))
    # print(part2(busses_constrained))
