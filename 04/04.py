from dataclasses import dataclass
import re
from typing import Optional, Sequence


@dataclass
class Passport:
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str] = None

    @classmethod
    def from_string(cls, string: str) -> 'Password':
        def search(pattern: str, optional: bool = False) -> Optional[str]:
            try:
                return re.search(pattern, string).group(1)
            except AttributeError as e:
                if optional:
                    return None
                else:
                    raise e

        try:
            byr = search(r'byr:(\S+)')
            iyr = search(r'iyr:(\S+)')
            eyr = search(r'eyr:(\S+)')
            hgt = search(r'hgt:(\S+)')
            hcl = search(r'hcl:(\S+)')
            ecl = search(r'ecl:(\S+)')
            pid = search(r'pid:(\S+)')
        except AttributeError:
            # one of the fields was not present
            return None

        cid = search(r'cid:(\S+)', optional=True)
        try:
            return cls(byr, iyr, eyr, hgt, hcl, ecl, pid, cid)
        except ValueError as e:
            # print(e, string, sep='\n', end='\n\n')
            return None


class VerifiedPassport(Passport):

    def __init__(self, byr: str, iyr: str, eyr: str, hgt: str, hcl: str, ecl: str, pid: str, cid: Optional[str] = None):
        if not re.fullmatch(r'\d{4}', byr) or not (1920 <= int(byr) <= 2002):
            raise ValueError(f'Invalid byr: {byr}')
        self.byr = int(byr)
        
        if not re.fullmatch(r'\d{4}', iyr) or not (2010 <= int(iyr) <= 2020):
            raise ValueError(f'Invalid iyr: {iyr}')
        self.iyr = int(iyr)

        if not re.fullmatch(r'\d{4}', eyr) or not (2020 <= int(eyr) <= 2030):
            raise ValueError(f'Invalid eyr: {eyr}')
        self.eyr = int(eyr)

        if not re.fullmatch(r'\d+(?:cm|in)', hgt):
            raise ValueError(f'Invalid height: {hgt}')
        if hgt.endswith('in') and not (59 <= int(hgt[:-2]) <= 76):
            raise ValueError(f'Invalid height in inches: {hgt}')
        if hgt.endswith('cm') and not (150 <= int(hgt[:-2]) <= 193):
            raise ValueError(f'Invalid height in cm: {hgt}')
        self.hgt = hgt

        if not re.fullmatch(r'#[a-f0-9]{6}', hcl):
            raise ValueError(f'Invalid hcl: {hcl}')
        self.hcl = hcl

        if ecl not in { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' }:
            raise ValueError(f'Invalid ecl: {ecl}')
        self.ecl = ecl

        if not re.fullmatch(r'\d{9}', pid):
            raise ValueError(f'Invalid pid: {pid}')
        self.pid = int(pid)

        self.cid = cid


def part1(data: Sequence[str]) -> int:
    return sum(bool(Passport.from_string(elem)) for elem in data)


def part2(data: Sequence[str]) -> int:
    return sum(bool(VerifiedPassport.from_string(elem)) for elem in data)


if __name__ == '__main__':
    with open('04/input.txt', 'r') as in_file:
        data = [line.replace('\n', ' ') for line in in_file.read().strip().split('\n\n')]

    print(part1(data))
    print(part2(data))
