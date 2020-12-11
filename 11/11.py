from functools import cached_property
from typing import Literal, Sequence, Union


class Seats:
    FLOOR = '.'
    EMPTY = 'L'
    OCCUP = '#'

    def __init__(self, data: Sequence[Sequence[int]]):
        self._data = data.copy()

    @property
    def data(self) -> Sequence[Sequence[int]]:
        return self._data.copy()

    def _sum(self, target: Literal['#', '.', 'L']) -> int:
        return sum(sum(target == y for y in x) for x in self._data)

    @cached_property
    def seats(self) -> int:
        return self._sum(Seats.OCCUP)

    @cached_property
    def floors(self) -> int:
        return self._sum(Seats.FLOOR)

    @cached_property
    def empty(self) -> int:
        return self._sum(Seats.EMPTY)

    def count_neighbors(self, i: int, j: int) -> int:
        max_len = len(self._data)
        neighbors = 0
        for x in range(i - 1, i + 2):
            if 0 <= x < max_len:
                for y in range(j - 1, j + 2):
                    if 0 <= y < len(self._data[x]):
                        if (x != i or y != j) and self._data[x][y] == Seats.OCCUP:
                            neighbors += 1
        return neighbors

    def next_gen_seat(self, i: int, j: int) -> str:
        if (seat := self._data[i][j]) == Seats.FLOOR:
            return Seats.FLOOR
    
        n = self.count_neighbors(i, j)
        if seat == Seats.EMPTY and n == 0:
            return Seats.OCCUP
        if seat == Seats.OCCUP and n >= 4:
            return Seats.EMPTY
        return seat

    def next_gen(self) -> 'Seats':
        return Seats([
            [self.next_gen_seat(i, j) for j in range(len(self._data[i]))] for i in range(len(self._data))
        ])

    def __eq__(self, o: object) -> bool:
        return self._data == o._data

    def __str__(self) -> str:
        return '\n'.join(''.join(e for e in line) for line in self._data)


class VisibleSeats(Seats):

    def __init__(self, data: Sequence[Sequence[int]]):
        self._data = data.copy()

    def seat_in_direction(self, i: int, j: int, *, x: Literal[-1, 0, 1], y: Literal[-1, 0, 1]) -> str:
        if x == y == 0:
            raise ValueError(f'No direction was given! ({x}, {y})')

        curr_x, curr_y = i + x, j + y
        while 0 <= curr_x < len(self._data) and 0 <= curr_y < len(self._data[curr_x]):
            if (pos := self._data[curr_x][curr_y]) != Seats.FLOOR:
                return pos
            curr_x += x
            curr_y += y
        # out of range ~ saw floor
        return Seats.FLOOR

    def count_neighbors(self, i: int, j: int) -> int:
        neighbors = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x != 0 or y != 0) and self.seat_in_direction(i, j, x=x, y=y) == Seats.OCCUP:
                    neighbors += 1
        return neighbors

    def next_gen_seat(self, i: int, j: int) -> str:
        if (seat := self._data[i][j]) == Seats.FLOOR:
            return Seats.FLOOR
    
        n = self.count_neighbors(i, j)
        if seat == Seats.EMPTY and n == 0:
            return Seats.OCCUP
        if seat == Seats.OCCUP and n >= 5:
            return Seats.EMPTY
        return seat

    def next_gen(self) -> 'VisibleSeats':
        return VisibleSeats([
            [self.next_gen_seat(i, j) for j in range(len(self._data[i]))] for i in range(len(self._data))
        ])


def convergence_seats(prev: Union[Seats, VisibleSeats]):
    curr = prev.next_gen()
    while prev != curr:
        prev, curr = curr, curr.next_gen()

    return curr.seats

def part1(data: Sequence[Sequence[int]]) -> int:
    return convergence_seats(Seats(data))


def part2(data: Sequence[Sequence[int]]) -> int:
    return convergence_seats(VisibleSeats(data))
    

if __name__ == '__main__':
    with open('11/input.txt', 'r') as in_file:
        data = [list(line) for line in in_file.read().strip().splitlines()]

    print(part1(data))
    print(part2(data))
