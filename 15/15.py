from typing import Sequence



def part1(data: Sequence[int], *, target: int = 2020):
    memory = {number: i for i, number in enumerate(data, 1)}

    prev = data[-1]
    for i in range(len(data) + 1, target + 1):
        curr = memory[prev]
        
        # first mention
        if type(curr) == int:
            first = memory[(prev := 0)]
            memory[prev] = (i, first) if type(first) == int else (i, first[0])
        # 2nd+ mention
        else:
            prev = curr[0] - curr[1]
            if prev in memory:
                second_plus = memory[prev]
                memory[prev] = (i, second_plus) if type(second_plus) == int else (i, second_plus[0])
            else:
                memory[prev] = i
    return prev


if __name__ == '__main__':
    with open('15/input.txt', 'r') as in_file:
        data = list(map(int, in_file.read().strip().split(',')))

    print(part1(data))
    print(part1(data, target=30_000_000))
