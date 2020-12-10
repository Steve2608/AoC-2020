from collections import defaultdict
from typing import Iterable, Sequence


def part1(data: Sequence[int], *, jolts: Iterable[int] = range(1, 4)) -> int:
    adapters, last = frozenset(data), max(data)
    counts = {i: 0 for i in jolts}

    # implicit 0 adapter
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
    

def part2(data: Sequence[int], *, jolts: Iterable[int] = range(1, 4)) -> int:
    adapters = defaultdict(int)
    # implicit 0 adapter
    adapters[0] = 1

    for i in sorted(data):
        adapters[i] = sum(adapters[i - j] for j in jolts)

    # implicit +3 adapter
    last = max(data) + 3
    return sum(adapters[last - j] for j in jolts)


if __name__ == '__main__':
    with open('10/input.txt', 'r') as in_file:
        data = list(map(int, in_file))

    print(part1(data))
    print(part2(data))
