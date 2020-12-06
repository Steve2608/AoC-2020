from typing import Sequence


def part1(data: Sequence[str]) -> int:
    return sum(len(set(group.replace('\n', ''))) for group in data)


def part2(data: Sequence[str]) -> int:
    return sum(len(
        set((g := gr.split('\n'))[0]).intersection(*g[1:]) if '\n' in gr else set(gr)
    ) for gr in data)


if __name__ == '__main__':
    with open('06/input.txt', 'r') as in_file:
        data = in_file.read().strip().split('\n\n')
    
    print(part1(data))
    print(part2(data))
