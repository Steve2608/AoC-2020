import re
from dataclasses import dataclass
from functools import partial
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

    def __init__(self, byr: str, iyr: str, eyr: str, hgt: str, hcl: str, ecl: str, pid: str, cid: Optional[str] = None, /):
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


example1 = partial(part1, data=[line.replace('\n', ' ') for line in r"""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split('\n\n')])

example2 = partial(part2, data=[line.replace('\n', ' ') for line in r"""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".split('\n\n')])

example3 = partial(part2, data=[line.replace('\n', ' ') for line in r"""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""".split('\n\n')])


if __name__ == '__main__':
    assert example1() == 2
    assert example2() == 0
    assert example3() == 4

    with open('04/input.txt', 'r') as in_file:
        data = [line.replace('\n', ' ') for line in in_file.read().strip().split('\n\n')]

    print(part1(data))
    print(part2(data))
