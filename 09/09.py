from collections import deque
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
    idx, target = find_weakness(data, preamble_length=preamble_length)

    # sum (can be kept track of on the fly), right index
    s, i = data[0], 1
    curr = deque([s])
    while i < idx:
        # add numbers from the right until >= target or out of numbers
        while s < target and i < idx:
            s += (add := data[i])
            curr.appendleft(add)
            i += 1

        while s > target:
            s -= curr.pop()

        if s == target:
            return min(curr) + max(curr)
    raise ValueError('No contiguous set found')


if __name__ == '__main__':
    with open('09/input.txt', 'r') as in_file:
        data = list(map(int, in_file))

    print(part1(data))
    print(part2(data))
