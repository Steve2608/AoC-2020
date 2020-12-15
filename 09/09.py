from collections import deque
from functools import partial
from typing import Sequence


def sums_to(preamble: Sequence[int], *, target: int) -> bool:
    for i, pi in enumerate(preamble):
        for j, pj in enumerate(preamble):
            if i != j and pi + pj == target:
                return True
    else:
        return False


def find_weakness(data: Sequence[int], *, preamble_length: int):
    preamble = deque(data[:preamble_length], maxlen=preamble_length)

    for i, s in enumerate(data[preamble_length:], preamble_length):
        if not sums_to(preamble, target=s):
            return i, s
        preamble.append(s)


def part1(data: Sequence[int], *, preamble_length: int = 25) -> int:
    return find_weakness(data, preamble_length=preamble_length)[1]


def part2(data: Sequence[int], *, preamble_length: int = 25) -> int:
    target = find_weakness(data, preamble_length=preamble_length)[1]

    # sum (can be kept track of on the fly), left index, right index
    s, left, right, max_idx = data[0], 0, 1, len(data)
    while right < max_idx:
        # add numbers from the right until >= target or out of numbers
        while s < target and right < max_idx:
            s += data[right]
            right += 1

        while s > target:
            s -= data[left]
            left += 1

        if s == target:
            window = data[left:right]
            return min(window) + max(window)
    raise ValueError('No contiguous set found')


example1 = partial(part1,
    data=[35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
    preamble_length=5
)
example2 = partial(part2,
    data=[35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
    preamble_length=5
)


if __name__ == '__main__':
    assert example1() == 127
    assert example2() == 62

    with open('09/input.txt', 'r') as in_file:
        data = list(map(int, in_file))

    print(part1(data))
    print(part2(data))
