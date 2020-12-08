import re
from typing import NamedTuple, Sequence, Set, Tuple


class Instruction(NamedTuple):
    op: str
    arg: int

    def change(self) -> 'Instruction':
        if self.op == 'jmp':
            return Instruction('nop', self.arg)
        if self.op == 'nop':
            return Instruction('jmp', self.arg)
        return Instruction(self.op, self.arg)


def parse_instructions(data: str) -> Sequence[Instruction]:
    return [Instruction(op, int(arg)) for op, arg in re.findall(r'(?:(acc|jmp|nop) ((?:\+|-)\d+))+', data)]


def execute(instructions: Sequence[Instruction]) -> Tuple[int, int, Set[int]]:
    val, i, visited, max_idx = 0, 0, set(), len(instructions)

    while i not in visited and i < max_idx:
        visited.add(i)
        instr = instructions[i]

        i += instr.arg if instr.op == 'jmp' else 1
        if instr.op == 'acc':
            val += instr.arg
    
    return val, i, visited


def part1(data: Sequence[Instruction]) -> int:
    return execute(data)[0]


def part2(data: Sequence[Instruction]) -> int:
    max_idx = len(data)

    # only test for jmp/nop
    for i in filter(lambda i: data[i].op != 'acc', execute(data)[2]):
        changed = data[:i] + [data[i].change()] + data[i + 1:]
        
        val, j, _ = execute(changed)
        if j >= max_idx:
            return val


if __name__ == '__main__':
    with open('08/input.txt', 'r') as in_file:
        data = parse_instructions(in_file.read())
    
    print(part1(data))
    print(part2(data))
