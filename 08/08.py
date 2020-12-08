import re
import dataclasses
from typing import List, Sequence, Set, Tuple


@dataclasses.dataclass
class Instruction:
    op: str
    arg: int

    def change(self) -> 'Instruction':
        if self.op == 'jmp':
            return Instruction('nop', self.arg)
        if self.op == 'nop':
            return Instruction('jmp', self.arg)
        return Instruction(self.op, self.arg)

    @classmethod
    def _from_parts(cls, parts: Tuple[str, str]) -> 'Instruction':
        return cls(parts[0], int(parts[1]))

    @classmethod
    def parse_instructions(cls, data: str) -> List['Instruction']:
        return list(map(cls._from_parts, re.findall(r'(?:(acc|jmp|nop) ((?:\+|-)\d+))+', data)))


def execute(instructions: Sequence[Instruction]) -> Tuple[int, int, Set[int]]:
    val, i, visited, max_idx = 0, 0, set(), len(instructions)

    while i not in visited and i < max_idx:
        visited.add(i)
        instr = instructions[i]

        i += instr.arg if instr.op == 'jmp' else 1
        if instr.op == 'acc':
            val += instr.arg
    
    return val, i, visited


def execute_interruptable(instructions: Sequence[Instruction], *, idx: int, dead_code: Set[int]) -> Tuple[int, int, Set[int]]:
    val, i, visited, max_idx = 0, 0, set(), len(instructions)

    while (j := i) not in visited and i < max_idx:
        instr = instructions[i]

        i += instr.arg if instr.op == 'jmp' else 1
        if j == idx and i in dead_code:
            # after change i still points to code known to be dead -> abort
            break

        if instr.op == 'acc':
            val += instr.arg
        visited.add(j)
    
    return val, i, visited


def part1(data: Sequence[Instruction]) -> int:
    return execute(data)[0]


def part2(data: Sequence[Instruction]) -> int:
    max_idx = len(data)

    # only test for jmp/nop
    for i in filter(lambda i: data[i].op != 'acc', visited := execute(data)[2]):
        changed = data[:i] + [data[i].change()] + data[i + 1:]
        
        # val, j, _ = execute(changed)
        val, j, _ = execute_interruptable(changed, idx=i, dead_code=visited)
        if j >= max_idx:
            return val


if __name__ == '__main__':
    with open('08/input.txt', 'r') as in_file:
        data = Instruction.parse_instructions(in_file.read())
    
    print(part1(data))
    print(part2(data))
