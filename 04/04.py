from dataclasses import dataclass
import re
from typing import Any, Optional, Sequence


@dataclass
class Passport:
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[Any] = None

    @classmethod
    def from_string(cls, string: str) -> 'Password':
        def search(pattern: str, optional: bool = False) -> Any:
            try:
                return re.search(pattern, string).group(1)
            except AttributeError as e:
                if optional:
                    return None
                else:
                    raise e

        try:
            byr = search(r'byr:([^\s]+)')
            iyr = search(r'iyr:([^\s]+)')
            eyr = search(r'eyr:([^\s]+)')
            hgt = search(r'hgt:([^\s]+)')
            hcl = search(r'hcl:([^\s]+)')
            ecl = search(r'ecl:([^\s]+)')
            pid = search(r'pid:([^\s]+)')
        except AttributeError:
            # one of the fields was not present
            return None

        cid = search(r'cid:([^\s]+)', optional=True)
        try:
            return cls(byr, iyr, eyr, hgt, hcl, ecl, pid, cid)
        except ValueError as e:
            # print(e, string, sep='\n', end='\n\n')
            return None


class VerifiedPassport(Passport):

    def __init__(self, byr: str, iyr: str, eyr: str, hgt: str, hcl: str, ecl: str, pid: str, cid: Optional[Any] = None):
        byr = int(byr)
        if not (1920 <= byr <= 2002):
            raise ValueError(f'Invalid byr: {byr}')
        self.byr = byr
        
        iyr = int(iyr)
        if not (2010 <= iyr <= 2020):
            raise ValueError(f'Invalid iyr: {iyr}')
        self.iyr = iyr

        eyr = int(eyr)
        if not (2020 <= eyr <= 2030):
            raise ValueError(f'Invalid eyr: {eyr}')
        self.eyr = eyr

        if (end1 := hgt.endswith('in')) and not (59 <= int(hgt[:-2]) <= 76):
            raise ValueError(f'Invalid height in inches: {hgt}')
        if (end2 := hgt.endswith('cm')) and not (150 <= int(hgt[:-2]) <= 193):
            raise ValueError(f'Invalid height in cm: {hgt}')
        if not (end1 or end2):
            raise ValueError(f'Invalid unit for height: {hgt}')
        self.hgt = hgt

        if not hcl.startswith('#') or len(hcl) != 7:
            raise ValueError(f'Invalid hcl: {hcl}')
        self.hcl = hcl

        if ecl not in { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' }:
            raise ValueError(f'Invalid ecl: {ecl}')
        self.ecl = ecl

        if not re.search(r'^\d{9}$', pid):
            raise ValueError(f'Invalid pid: {pid}')
        self.pid = int(pid)

        self.cid = cid


def part1(data: Sequence[str]) -> int:
    return sum(bool(Passport.from_string(elem)) for elem in data)


def part2(data: Sequence[str]) -> int:
    return sum(bool(VerifiedPassport.from_string(elem)) for elem in data)


if __name__ == '__main__':
    with open('04/input.txt', 'r') as in_file:
        data = [line.replace('\n', ' ') for line in in_file.read().split('\n\n')]

    print(part1(data))
    print(part2(data))
