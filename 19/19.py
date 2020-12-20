import re
from typing import Sequence, Union
from functools import partial


class Parser:

    def __init__(self, rules: dict[int, Union[str, list[int], tuple[list[int], list[int]]]]):
        self.rules = rules

    def parse(self, sentence: str) -> bool:
        def match(rule: Union[str, list[int], tuple[list[int], ...]], sentence: str) -> set[str]:
            # string already consumed
            if not sentence:
                return set()
            
            if (typ := type(rule)) == str:
                return {sentence.removeprefix(rule)} if sentence.startswith(rule) else set()
            elif typ == list:
                possibs = {sentence}
                for r in rule:
                    possibs = set().union(*[match(self.rules[r], p) for p in possibs])
                return possibs                        
            else:
                return set().union(*[match(branch, sentence) for branch in rule])

        # one of the possibilities eventually leads to match             
        return '' in match(self.rules[0], sentence)

    @classmethod
    def from_string(cls, rules: str) -> 'Parser':
        return cls.from_strings(rules.splitlines())

    @classmethod
    def from_strings(cls, rules: Sequence[str]) -> 'Parser':
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
        return cls(pattern)


def count_matches(parser: Parser, sentences: Sequence[str]) -> int:
    return sum(parser.parse(sentence) for sentence in sentences)


example1 = partial(count_matches,
    sentences=r"""ababbb
bababa
abbbab
aaabbb
aaaabbb""".splitlines(),
    parser=Parser.from_string(r"""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
""".strip()))

example2 = partial(count_matches,
    sentences=r"""abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
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
    parser=Parser.from_string(r"""42: 9 14 | 10 1
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
24: 14 1"""))

example3 = partial(count_matches,
    sentences=r"""abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
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
    parser=Parser.from_string(r"""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31 | 42 11 31
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
8: 42 | 42 8
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1"""))


if __name__ == '__main__':
    assert example1() == 2
    assert example2() == 3

    assert example3() == 12

    with open('19/input.txt', 'r') as in_file:
        rules, messages = in_file.read().strip().split('\n\n')
    
    messages = messages.splitlines()
    parser = Parser.from_string(rules)
    parser2 = Parser.from_string(rules.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31'))

    print(count_matches(parser, messages))
    print(count_matches(parser2, messages))
