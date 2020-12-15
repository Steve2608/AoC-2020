from typing import Sequence
from functools import partial
from collections import defaultdict


def memory_game(data: Sequence[int], target: int):
    last = defaultdict(int)
    for i, number in enumerate(data, 1):
        last[number] = i
    second_to_last = defaultdict(int)

    num = data[-1]
    for i in range(len(data) + 1, target + 1):
        if (stl := second_to_last[num]) == 0:
            second_to_last[(num := 0)] = last[0]
        else:
            second_to_last[num] = last[(num := last[num] - stl)]
        last[num] = i

    return num



part1 = partial(memory_game, target=2020)
part2 = partial(memory_game, target=30_000_000)


if __name__ == '__main__':
    with open('15/input.txt', 'r') as in_file:
        data = list(map(int, in_file.read().strip().split(',')))

    print(part1(data))
    print(part2(data))
