from typing import Sequence
from collections import deque
from functools import partial


class Player:

    def __init__(self, number: int, cards: Sequence[int]):
        self._number = number
        self._cards = deque(cards)

    @property
    def number(self) -> int:
        return self._number

    @property
    def cards(self) -> Sequence:
        return self._cards

    def draw(self) -> int:
        return self._cards.popleft()

    def win(self, card1: int, card2: int):
        self._cards.append(card1)
        self._cards.append(card2)

    def copy_cards(self, cards: int) -> 'Player':
        return Player(self.number, list(self._cards)[:cards])

    @classmethod
    def from_string(cls, string: str):
        header, values = string.split('\n', 1)
        return cls(int(header.removeprefix('Player ').removesuffix(':')), deque(map(int, values.splitlines())))

    def __len__(self) -> int:
        return len(self._cards)

    def __bool__(self) -> bool:
        return bool(self._cards)

    def __str__(self) -> str:
        return f'Player {self.number}: {list(self._cards)}'


def points(p1: Player, p2: Player) -> int:
    p = p1 if len(p1) > len(p2) else p2
    return sum(i * elem for i, elem in enumerate(reversed(p.cards), 1))


def part1(p1: Player, p2: Player) -> int:
    while p1 and p2:
        # print(p1, p2)
        if (c1 := p1.draw()) > (c2 := p2.draw()):
            p1.win(c1, c2)
        else:
            p2.win(c2, c1)

    return points(p1, p2)


def part2(p1: Player, p2: Player) -> int:
    def game(p1: Player, p2: Player, depth: int, is_subgame: bool = True) -> bool:
        memory = set()
        while p1 and p2:
            # print("\t"*depth + f'{p1}, {p2}')
            if (state := (tuple(p1.cards), tuple(p2.cards))) in memory and is_subgame:
                return True # p1 won
            memory.add(state)

            c1, c2 = p1.draw(), p2.draw()
            if c1 <= len(p1) and c2 <= len(p2):
                if game(p1.copy_cards(c1), p2.copy_cards(c2), depth=depth + 1):
                    p1.win(c1, c2)
                else:
                    p2.win(c2, c1)
            else:
                if c1 > c2:
                    p1.win(c1, c2)
                else:
                    p2.win(c2, c1)
        
        return len(p1) > len(p2)

    game(p1, p2, depth=0, is_subgame=False)
    return points(p1, p2)


example1 = partial(part1, 
    p1=Player(1, deque([9, 2, 6, 3, 1])),
    p2=Player(2, deque([5, 8, 4, 7, 10]))
)

example2 = partial(part2, 
    p1=Player(1, deque([9, 2, 6, 3, 1])),
    p2=Player(2, deque([5, 8, 4, 7, 10]))
)


if __name__ == '__main__':
    assert example1() == 306
    assert example2() == 291

    with open('22/input.txt', 'r') as in_file:
        player1, player2 = map(Player.from_string, in_file.read().strip().split('\n\n'))
    print(part1(player1, player2))

    with open('22/input.txt', 'r') as in_file:
        player1, player2 = map(Player.from_string, in_file.read().strip().split('\n\n'))
    print(part2(player1, player2))
