import re
from typing import Sequence


class Seat:
    
    def __init__(self, seat: int):
        self._seat = seat

    @property
    def seat(self) -> int:
        return self._seat

    @property
    def row(self) -> int:
        return self.seat >> 3

    @property
    def col(self) -> int:
        return self.seat & 0x7

    @classmethod
    def from_string(cls, string: str) -> 'Seat':
        return cls(int(re.sub(r'[FL]', '0', re.sub(r'[BR]', '1', string)), base=2))


def part1(data: Sequence[str]) -> int:
    return max(Seat.from_string(line).seat for line in data)


def part2(data: Sequence[str]) -> int:
    seats = sorted((Seat.from_string(line) for line in data), key=lambda s: s.seat)
    for lower, upper in zip(seats[:-1], seats[1:]):
        if lower.seat + 2 == upper.seat:
            return lower.seat + 1


if __name__ == '__main__':
    with open('05/input.txt', 'r') as in_file:
        data = [line for line in in_file.read().splitlines()]
    
    print(part1(data))
    print(part2(data))