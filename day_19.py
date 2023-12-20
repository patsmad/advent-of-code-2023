import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Func:
    def __init__(self, trait, op, num, to_if, to_else):
        self.trait = trait
        if op == '>':
            self.num = int(num) + 1
            self.to_if = to_else
            self.to_else = to_if
        else:
            self.num = int(num)
            self.to_if = to_if
            self.to_else = to_else

    def run_scalar(self, item):
        if item[self.trait] < self.num:
            return self.to_if
        else:
            return self.to_else

    def run_ranges(self, item):
        if item[self.trait][1] < self.num:
            return [(self.to_if, item)]
        elif item[self.trait][0] >= self.num:
            return [(self.to_else, item)]
        else:
            if_range = (item[self.trait][0], self.num - 1)
            else_range = (self.num, item[self.trait][1])
            return [(self.to_if, {k: if_range if k == self.trait else item[k] for k,v in item.items()}),
                    (self.to_else, {k: else_range if k == self.trait else item[k] for k,v in item.items()})]

class DefaultFunc:
    def __init__(self, result):
        self.result = result

    def run_scalar(self, item):
        return self.result

    def run_ranges(self, item):
        return [(self.result, item)]

def get_func(condition, next_func):
    trait, op, num, result = re.fullmatch('(.*)([<>])([0-9]*):(.*)', condition).groups()
    return Func(trait, op, num, result, next_func)

def parse_workflow(line):
    base_name, conditions = re.fullmatch('(.*){(.*)}', line).groups()
    condition_list = conditions.split(',')
    funcs = {}
    name = base_name
    for idx, condition in enumerate(condition_list[:-1]):
        funcs[name] = get_func(condition, f'{base_name}_{idx+1}')
        name = f'{base_name}_{idx+1}'
    funcs[f'{base_name}_{len(funcs)}'] = DefaultFunc(condition_list[-1])
    return funcs

def parse_item(line):
    x, m, a, s = re.fullmatch('{x=([0-9]*),m=([0-9]*),a=([0-9]*),s=([0-9]*)}', line).groups()
    return {'x': int(x), 'm': int(m), 'a': int(a), 's': int(s)}

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}
        
        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """.strip()

    lines = [line.strip() for line in raw_input.strip().split('\n')]

    funcs = {}
    for line in lines[:lines.index('')]:
        new_funcs = parse_workflow(line)
        funcs.update(new_funcs)

    items = []
    for line in lines[lines.index('')+1:]:
        items.append(parse_item(line))

    # part 1
    s = 0
    for item in items:
        out = funcs['in'].run_scalar(item)
        while out not in ['R', 'A']:
            out = funcs[out].run_scalar(item)
        if out == 'A':
            s += item['x'] + item['m'] + item['a'] + item['s']
    print(s)

    # part 2
    items = [('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})]
    A_items = []
    while len(items) > 0:
        new_items = []
        for item in items:
            new_items += funcs[item[0]].run_ranges(item[1])
        A_items += [item for item in new_items if item[0] == 'A']
        items = [item for item in new_items if item[0] not in ['A', 'R']]
    s = 0
    for item in A_items:
        m = 1
        for k, v in item[1].items():
            m *= v[1] - v[0] + 1
        s += m
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
