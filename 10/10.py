from collections import defaultdict
from functools import partial
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


example1 = partial(part1, data=[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], jolts=range(1, 4))
example2 = partial(part1, 
    data=[28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3],
    jolts=range(1, 4)
)
example3 = partial(part2, data=[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], jolts=range(1, 4))
example4 = partial(part2, 
    data=[28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3],
    jolts=range(1, 4)
)

if __name__ == '__main__':
    assert example1() == 35
    assert example2() == 220
    assert example3() == 8
    assert example4() == 19208

    with open('10/input.txt', 'r') as in_file:
        data = list(map(int, in_file))

    print(part1(data))
    print(part2(data))
