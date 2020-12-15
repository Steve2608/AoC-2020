import re
from functools import partial
from typing import Sequence, Union

int2 = partial(int, base=2)


def part1(data: Sequence[str]) -> int:
    mem, mask_0, mask_1 = {}, 0, 0
    for instr in data:
        if instr[:4] == 'mask':
            mask = instr[-36:]
            mask_1 = int2(mask.replace('X', '0'))
            mask_0 = int2(mask.replace('X', '1'))
        else:
            address, value = map(int, re.search(r'mem\[(\d+)\] = (\d+)', instr).groups())
            mem[address] = (value & mask_0) | mask_1

    return sum(mem.values())


def floating_masks(mask: str) -> Sequence[int]:
    if 'X' in mask:
        masks = floating_masks(mask.replace('X', '0', 1))
        masks.extend(floating_masks(mask.replace('X', '1', 1)))
        return masks
    else:
        return [int2(mask)]


def mem_adress(address: Union[int, str], mask: str) -> str:
    if type(address) == int:
        address = f'{address:036b}'
    return ''.join('X' if m == 'X' else ('1' if m == '1' or a == '1' else '0') for a, m in zip(address, mask))


def part2(data: Sequence[str]) -> int:
    mem, mask = {}, ''
    for instr in data:
        if instr[:4] == 'mask':
            mask = instr[-36:]
        else:
            address, value = map(int, re.search(r'mem\[(\d+)\] = (\d+)', instr).groups())
            for address in floating_masks(mem_adress(address, mask)):
                mem[address] = value

    return sum(mem.values())


example1 = partial(part1, data=r"""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines())

example2 = partial(part2, data=r"""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines())


if __name__ == '__main__':
    assert example1() == 165
    assert example2() == 208
    
    with open('14/input.txt', 'r') as in_file:
        data = in_file.read().strip().splitlines()

    print(part1(data))
    print(part2(data))
