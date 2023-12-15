import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def hash_it(s: str) -> int:
    out = 0
    for c in s:
        out += ord(c)
        out *= 17
        out %= 256
    return out

def power(box, slot, focus):
    return (1 + box) * (1 + slot) * focus

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """.strip()

    # part 1
    t = 0
    for s in raw_input.strip().split(','):
        t += hash_it(s)
    print(t)

    # part 2
    labels = {i: [] for i in range(256)}
    lenses = {i: [] for i in range(256)}
    for s in raw_input.strip().split(','):
        label, op, num = re.search('([a-zA-Z]*)([=-])([0-9]*)', s).groups()
        box = hash_it(label)
        if op == '-':
            if label in labels[box]:
                idx = labels[box].index(label)
                labels[box].pop(idx)
                lenses[box].pop(idx)
        else:
            if label in labels[box]:
                idx = labels[box].index(label)
                lenses[box][idx] = int(num)
            else:
                labels[box].append(label)
                lenses[box].append(int(num))

    t = 0
    for box, lenses in lenses.items():
        for slot, focus in enumerate(lenses):
            t += power(box, slot, focus)
    print(t)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
