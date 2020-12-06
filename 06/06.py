from typing import Sequence


def part1(data: Sequence[str]) -> int:
    return sum(len(set(group.replace('\n', ''))) for group in data)


def part2(data: Sequence[str]) -> int:
    s = { chr(c) for c in range(ord('a'), ord('z') + 1) }
    return sum(len(s.intersection(*(map(set, gr.split('\n'))))) for gr in data)


if __name__ == '__main__':
    with open('06/input.txt', 'r') as in_file:
        data = in_file.read().strip().split('\n\n')
    
    print(part1(data))
    print(part2(data))