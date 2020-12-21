
from collections import defaultdict
from typing import NamedTuple, Sequence
from functools import partial

class Food(NamedTuple):
    ingredients: Sequence[str]
    allergents: Sequence[str]

    @classmethod
    def from_string(cls, string: str):
        ingredients, allergenes = map(lambda l: l.strip(), string.strip().split('('))
        return cls(ingredients.split(' '), allergenes.removeprefix('contains ').removesuffix(')').split(', '))


def assign(data: Sequence[Food]):
    # count occurrences of ingredients
    counter = defaultdict(int)
    for food in data:
        for ing in food.ingredients:
            counter[ing] += 1

    # find possibly dangerous ingredients 
    danger = {}
    for food in data:
        ing = food.ingredients
        for allergent in food.allergents:
            danger[allergent] = danger[allergent].intersection(ing) if allergent in danger else set(ing)

    # as long as possibly dangerous ingredients do not have single value everywhere
    while sum(map(len, danger.values())) != len(danger):
        for allergent, possibs in danger.items():
            if len(possibs) == 1:
                # spread set
                to_discard, = possibs
                for k in danger:
                    if allergent != k:
                        danger[k].discard(to_discard)
    # take single remaining element out of set for convenience
    danger = { k: v.pop() for k, v in danger.items() }

    # delete entries in counter for dangerous ingredients
    for possibs in danger.values():
        del counter[possibs]
    
    # count non-allergenes, dangerous ingredients sorted by allergents 
    return sum(counter.values()), ','.join(danger[key] for key in sorted(danger))


example1 = partial(assign, data=list(map(Food.from_string, r"""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines())))


if __name__ == '__main__':
    assert example1() == (5, 'mxmxvkd,sqjhc,fvjkl')

    with open('21/input.txt', 'r') as in_file:
        data = list(map(Food.from_string, in_file.read().strip().splitlines()))
    
    print(*assign(data), sep='\n')
