import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_nodes(raw_input):
    nodes = {}
    for line in raw_input.strip().split('\n'):
        node_type, name, to_node_list = re.fullmatch('([%&]{,1})([a-z]*) -> ([a-z, ]*)', line.strip()).groups()
        to_nodes = to_node_list.split(', ')
        if node_type == '':
            nodes[name] = Broadcaster(name, to_nodes)
        elif node_type == '%':
            nodes[name] = FlipFlip(name, to_nodes)
        else:
            nodes[name] = Conjunction(name, to_nodes)
        for node in to_nodes:
            if node not in nodes:
                nodes[node] = NullNode(node)
    from_nodes = {}
    for name, node in nodes.items():
        for to_node in node.to_nodes:
            if nodes[to_node].conjunction:
                if to_node not in from_nodes:
                    from_nodes[to_node] = []
                from_nodes[to_node].append(name)
    for name, from_list in from_nodes.items():
        nodes[name].add_from_nodes(from_list)
    return nodes

class FlipFlip:
    def __init__(self, name, to_nodes):
        self.conjunction = False
        self.name = name
        self.is_on = False
        self.to_nodes = to_nodes

    def pulse(self, from_node, is_high):
        if not is_high:
            self.is_on = not self.is_on
            return [(self.name, to_node, self.is_on) for to_node in self.to_nodes]
        else:
            self.last = None
            return []

    def to_state(self):
        return '#' if self.is_on else '.'

class Conjunction:
    def __init__(self, name, to_nodes):
        self.conjunction = True
        self.name = name
        self.to_nodes = to_nodes
        self.is_on = True

    def add_from_nodes(self, from_nodes):
        self.is_high = {node: False for node in from_nodes}

    def pulse(self, from_node, is_high):
        self.is_high[from_node] = is_high
        self.is_on = not all(self.is_high.values())
        return [(self.name, to_node, self.is_on) for to_node in self.to_nodes]

    def to_state(self):
        return '#' if self.is_on else '.'

class Broadcaster:
    def __init__(self, name, to_nodes):
        self.conjunction = False
        self.name = name
        self.to_nodes = to_nodes

    def pulse(self, from_node, is_high):
        return [(self.name, to_node, is_high) for to_node in self.to_nodes]

    def to_state(self):
        return ''

class NullNode:
    def __init__(self, name):
        self.conjunction = False
        self.name = name
        self.to_nodes = []

    def pulse(self, from_node, is_high):
        return []

    def to_state(self):
        return ''

def to_state(nodes):
    return ';'.join([f'{name}{nodes[name].to_state()}' for name in sorted(nodes)])


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
        """.strip()

        raw_input: str = """
        broadcaster -> a, b
        %a -> c
        %b -> c
        &c -> d
        """

    # part 1
    nodes = get_nodes(raw_input)
    high = 0
    low = 0
    for press in range(1000):
        to_nodes = [('button', 'broadcaster', False)]
        while len(to_nodes) > 0:
            curr_node = to_nodes.pop(0)
            if curr_node[2]:
                high += 1
            else:
                low += 1
            to_nodes += nodes[curr_node[1]].pulse(curr_node[0], curr_node[2])
    print(high, low, high * low)

    # part 2
    # nodes = get_nodes(raw_input)
    # for node in ['a', 'b']:
    #     for i in range(10):
    #         initial_state = nodes[node].is_on
    #         first_flip = None
    #         length = 0
    #         press = 0
    #         while first_flip is None or nodes[node].is_on != initial_state:
    #             if nodes[node].is_on != initial_state:
    #                 if first_flip is None:
    #                     first_flip = press
    #                 length += 1
    #             press += 1
    #             if press > 100000 * (i + 1):
    #                 break
    #             to_nodes = [('button', 'broadcaster', False)]
    #             while len(to_nodes) > 0:
    #                 curr_node = to_nodes.pop(0)
    #                 if curr_node[2]:
    #                     high += 1
    #                 else:
    #                     low += 1
    #                 to_nodes += nodes[curr_node[1]].pulse(curr_node[0], curr_node[2])
    #         print(node, first_flip, length, press)
    nodes = get_nodes(raw_input)
    for press in range(100000):
        press_pulses = {n: [] for n in nodes}
        to_nodes = [('button', 'broadcaster', False)]
        while len(to_nodes) > 0:
            curr_node = to_nodes.pop(0)
            new_nodes = nodes[curr_node[1]].pulse(curr_node[0], curr_node[2])
            to_nodes += new_nodes
            for node in new_nodes[:1]:
                press_pulses[node[0]].append('H' if node[2] else 'L')
        if len(press_pulses['gk']) > 7:
            print(240914003753370 / 3947, press_pulses['gk'])
        # print(','.join(f'{name}:{"".join(press_pulses[name])}' for name in sorted(press_pulses) if len(press_pulses[name]) > 0))





if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
