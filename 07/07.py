import re
from functools import partial
from typing import Dict, Sequence


def build_bags(data: Sequence[str]) -> Dict[str, Dict[str, int]]:
    container = r'(\w+ \w+) bags contain'
    containees = r'(?:(\d+) (\w+ \w+) bags?)+'
    return {re.match(container, s).group(1): { bag: int(n) for n, bag in re.findall(containees, s) } for s in data}


def part1(data: Sequence[str], *, target: str ='shiny gold') -> int:
    bags = build_bags(data)
    containers, size = { target }, 0

    # as long as no new solutions were found
    while size != (size := len(containers)):
        containers = containers.union({k for k, v in bags.items() if containers.intersection(v)})
    # target does not contain itself
    return len(containers) - 1


def part2(data: Sequence[str], *, target: str ='shiny gold') -> int:
    def count(bag: Dict[str, int]) -> int:
        return sum(n * (1 + count(bags[color])) for color, n in bag.items())

    bags = build_bags(data)
    return count(bags[target])


example1 = partial(part1,
    data=r"""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".splitlines(),
    target='shiny gold'
)

example2 = partial(part2,
    data=r"""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".splitlines(),
    target='shiny gold'
)


if __name__ == '__main__':
    assert example1() == 4
    assert example2() == 126
    
    with open('07/input.txt', 'r') as in_file:
        data = in_file.read().strip().splitlines()

    print(part1(data))
    print(part2(data))
