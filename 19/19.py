import re
from typing import Sequence
from functools import partial


def parse_regex(rules: Sequence[str]) -> str:
    def expand(i: int):
        v = pattern[i]
        if (t := type(v)) == str:
            return v
        elif t == list:
            return ''.join(expand(key) for key in v)
        else:
            left, right = v
            return '(?:' + ''.join(expand(key) for key in left) + '|' + ''.join(expand(key) for key in right) + ')'
    
    pattern = {}
    for line in rules:
        k, v = re.search(r'(\d+): ([\d\s\w\|\"]+)', line).groups()
        k, v = int(k), v.strip()

        if '"' in v:
            pattern[k] = v.replace('"', '')
        elif '|' in v:
            left, right = v.split(' | ')
            pattern[k] = list(map(int, left.split(' '))), list(map(int, right.split(' ')))
        else:
            pattern[k] = list(map(int, v.split(' ')))
    
    return expand(0)



def part1(messages: Sequence[str], regex: str) -> int:
    return sum(bool(re.fullmatch(regex, message)) for message in messages)


example1 = partial(part1,
    messages=r"""ababbb
bababa
abbbab
aaabbb
aaaabbb""".splitlines(),
    regex=parse_regex(r"""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
""".strip().splitlines())
)

example2 = partial(part1,
    messages=r"""abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".splitlines(),
    regex=parse_regex(r"""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1""".splitlines())
)


if __name__ == '__main__':
    assert example1() == 2
    assert example2() == 3

    with open('19/input.txt', 'r') as in_file:
        rules, messages = in_file.read().strip().split('\n\n')
    
    messages = messages.splitlines()
    regex = parse_regex(rules.splitlines())

    print(part1(messages, regex))
