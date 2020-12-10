from collections import defaultdict
from typing import Sequence


def part1(data: Sequence[int]) -> int:
    adapters, last = frozenset(data), max(data)

    jolts = range(1, 4)
    counts = {i: 0 for i in jolts}

    curr = 0    
    while curr < last:
        for i in jolts:
            if curr + i in adapters:
                counts[i] += 1
                curr += i
                # only use shortest path
                break
    
    # implicit +3 adapter
    return counts[1] * (counts[3] + 1)
    

def part2(data: Sequence[int]) -> int:
    adapters = defaultdict(int)
    adapters[0] = 1

    for i in sorted(data):
        adapters[i] = adapters[i - 3] + adapters[i - 2] + adapters[i - 1]

    last = max(data) + 3
    return adapters[last - 3] + adapters[last - 2] + adapters[last - 1]


if __name__ == '__main__':
    with open('10/input.txt', 'r') as in_file:
        data = list(map(int, in_file))

    print(part1(data))
    print(part2(data))
