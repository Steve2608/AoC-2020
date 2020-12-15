from collections import defaultdict
from functools import partial
from typing import Sequence


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


example1 = partial(memory_game, data=[0, 3, 6], target=10)
example2 = partial(memory_game, data=[1, 3, 2], target=2020)
example3 = partial(memory_game, data=[2, 1, 3], target=2020)
example4 = partial(memory_game, data=[1, 2, 3], target=2020)
example5 = partial(memory_game, data=[2, 3, 1], target=2020)
example6 = partial(memory_game, data=[3, 2, 1], target=2020)
example7 = partial(memory_game, data=[3, 1, 2], target=2020)

part1 = partial(memory_game, target=2020)
part2 = partial(memory_game, target=30_000_000)


if __name__ == '__main__':
    assert example2() == 1
    assert example3() == 10
    assert example4() == 27
    assert example5() == 78
    assert example6() == 438
    assert example7() == 1836

    with open('15/input.txt', 'r') as in_file:
        data = list(map(int, in_file.read().strip().split(',')))

    print(part1(data))
    print(part2(data))
