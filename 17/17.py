from functools import partial
from itertools import product as carthesian_product


def parse_active(data: str, *, dims: int) -> set[tuple[int, ...]]:
    result, d = set(), [0] * (dims - 2)
    for i_y, x in enumerate(data.splitlines()):
        for i_x, e in enumerate(x):
            if e == '#':
                result.add((i_x, i_y, *d))
    return frozenset(result)


class PocketDimension:

    def __init__(self, active: set[tuple[int, int, int]], dims: int):
        self._active = active
        self._dims = dims
        self._deltas = list(carthesian_product(*([(-1, 0, 1)] * self._dims)))

    def next_gen(self) -> 'PocketDimension':
        candidates = set()
        for elem in self._active:
            for delta in self._deltas:
                candidates.add(tuple(e + d for e, d in zip(elem, delta)))

        return PocketDimension(frozenset(
            e for e in candidates if (n := self._neighbors(e)) == 3 or (n == 2 and e in self._active)
        ), dims=self._dims)

    def _neighbors(self, coord: tuple[int, ...]) -> int:
        return sum(
            tuple(c + d for c, d in zip(coord, delta)) in self._active
            for delta in self._deltas if any(d != 0 for d in delta)
        )


def simulate_cycles(pd: PocketDimension, *, cycles: int) -> int:
    for _ in range(cycles):
        pd = pd.next_gen()
    return len(pd._active)


example1 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=3), dims=3),
    cycles=0
)
example2 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=3), dims=3),
    cycles=1
)
example3 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=3), dims=3),
    cycles=2
)
example4 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=3), dims=3),
    cycles=3
)
example5 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=3), dims=3),
    cycles=6
)

example6 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=4), dims=4),
    cycles=1
)
example7 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=4), dims=4),
    cycles=2
)
example8 = partial(simulate_cycles,
    pd=PocketDimension(parse_active('.#.\n..#\n###', dims=4), dims=4),
    cycles=6
)


part1 = partial(simulate_cycles, cycles=6)
part2 = partial(simulate_cycles, cycles=6)


if __name__ == '__main__':
    assert example1() == 5
    assert example2() == 11
    assert example3() == 21
    assert example4() == 38
    assert example5() == 112

    assert example6() == 29
    assert example7() == 60
    assert example8() == 848

    with open('17/input.txt', 'r') as in_file:
        data = in_file.read().strip()

    print(part1(PocketDimension(parse_active(data, dims=3), dims=3)))
    print(part2(PocketDimension(parse_active(data, dims=4), dims=4)))
