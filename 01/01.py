from typing import List

def part1(data: List[int]) -> int:
    for a in data:
        for b in data:
            if a + b == 2020:
                return a * b


def part2(data: List[int]) -> int:
    for a in data:
        for b in data:
            if (part1 := a + b) >= 2020:
                continue
            for c in data:
                if part1 + c == 2020:
                    return a * b * c


if __name__ == '__main__':
    with open('01/input.txt', 'r') as in_file:
        data = list(map(int, in_file))
    
    print(part1(data))
    print(part2(data))
