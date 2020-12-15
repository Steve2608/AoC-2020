from typing import Sequence
from functools import partial


def memory_game(data: Sequence[int], target: int):
    memory = {number: (i, 0) for i, number in enumerate(data, 1)}

    prev = data[-1]
    for i in range(len(data) + 1, target + 1):
        curr1, curr2 = memory[prev]
        
        # first mention
        if curr2 == 0:
            first = memory[(prev := 0)][0]
            memory[prev] = i, first
        # 2nd+ mention
        else:
            second_plus = memory.get(prev := curr1 - curr2, None)
            memory[prev] = (i, second_plus[0]) if second_plus else (i, 0)
    return prev


part1 = partial(memory_game, target=2020)
part2 = partial(memory_game, target=30_000_000)


if __name__ == '__main__':
    with open('15/input.txt', 'r') as in_file:
        data = list(map(int, in_file.read().strip().split(',')))

    print(part1(data))
    print(part2(data))
