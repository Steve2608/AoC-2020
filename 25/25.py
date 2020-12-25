from functools import partial


def transform(target: int, /, subect_number: int, mod: int = 20201227):
    n, value = 0, 1
    while value != target:
        n += 1
        value *= subect_number
        value %= mod
    return n


def transform_n(n: int, /, subect_number: int, mod: int = 20201227):
    value = 1
    for _ in range(n):
        value *= subect_number
        value %= mod
    return value


def part1(card: int, door: int):
    n_card = transform(card, subect_number=7)
    n_door = transform(door, subect_number=7)

    key = transform_n(n_door, subect_number=card)
    assert transform_n(n_card, subect_number=door) == key

    return key


example1 = partial(part1, card=5764801, door=17807724)


if __name__ == "__main__":
    assert example1() == 14897079

    with open('25/input.txt', 'r') as in_file:
        card, door = map(int, in_file.read().strip().splitlines())

    print(part1(card, door))
