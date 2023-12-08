import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Node:
    def __init__(self, name: str, left: str, right: str) -> None:
        self.name: str = name
        self.left: str = left
        self.right: str = right

    def __str__(self):
        return f'{self.name} {self.left} {self.right}'

def format(raw_input: str) -> (str, dict[str, Node]):
    instructions, node_strs = raw_input.strip().split('\n\n')
    nodes: dict[str, Node] = {}
    for node_str in node_strs.split('\n'):
        name, lr = node_str.strip().split(' = ')
        left, right = re.search('\(([A-Z]{3}), ([A-Z]{3})\)', lr.strip()).groups()
        nodes[name] = Node(name, left, right)
    return instructions, nodes

def get_steps(curr_node: str, instructions: str, nodes: dict[str, Node]) -> (int, str):
    steps = 0
    idx = 0
    while curr_node[2] != 'Z':
        curr_node = nodes[curr_node].right if instructions[idx] == 'R' else nodes[curr_node].left
        steps += 1
        idx = (idx + 1) % len(instructions)
    return steps


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """.strip()

    instructions, nodes = format(raw_input)

    # part 1
    print(get_steps('AAA', instructions, nodes))

    # part 2
    m = len(instructions)
    for name in nodes:
        if name[2] == 'A':
            steps = get_steps(name, instructions, nodes)
            m *= steps // len(instructions)
    print(m)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
