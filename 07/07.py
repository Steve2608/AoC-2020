import re
from typing import Dict, Sequence


def build_bags(data: Sequence[str]) -> Dict[str, Dict[str, int]]:
    container = r'(\w+ \w+) bags contain'
    containees = r'(?:(\d+) (\w+ \w+) bags?)+'
    return {
        re.match(container, s).group(1):
        dict() if s.endswith('no other bags.') else { bag: int(n) for n, bag in re.findall(containees, s) }
        for s in data
    }


def part1(data: Sequence[str], target: str ='shiny gold') -> int:
    bags = build_bags(data)
    containers, size = { target }, 0

    # as long as no new solutions were found
    while size != (size := len(containers)):
        containers = containers.union({k for k, v in bags.items() if containers.intersection(v)})
    # target does not contain itself
    return len(containers) - 1


def part2(data: Sequence[str], target: str ='shiny gold') -> int:
    def count(bag: Dict[str, int]) -> int:
        return sum(n * (1 + count(bags[color])) for color, n in bag.items())

    bags = build_bags(data)
    return count(bags[target])


if __name__ == '__main__':
    with open('07/input.txt', 'r') as in_file:
        data = in_file.read().strip().splitlines()

    print(part1(data))
    print(part2(data))
