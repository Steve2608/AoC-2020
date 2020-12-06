from dataclasses import dataclass
import re
from typing import Sequence


@dataclass
class Seat:
    seat: int
    row: int
    col: int

    def __init__(self, seat: int):
        self.seat = seat
        self.row = seat >> 3
        self.col = seat & 0x7

    @classmethod
    def from_string(cls, string: str) -> 'Seat':
        return cls(int(re.sub(r'[FL]', '0', re.sub(r'[BR]', '1', string)), base=2))


def part1(data: Sequence[str]) -> int:
    return max(Seat.from_string(line).seat for line in data)


def part2(data: Sequence[str]) -> int:
    seats = sorted(Seat.from_string(line).seat for line in data)
    for lower, upper in zip(seats[:-1], seats[1:]):
        if lower + 2 == upper:
            return lower + 1


if __name__ == '__main__':
    with open('05/input.txt', 'r') as in_file:
        data = in_file.read().strip().splitlines()
    
    print(part1(data))
    print(part2(data))
