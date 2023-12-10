from __future__ import annotations

import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()
shifts: dict[str, list[(int, int)]] = {
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, -1), (1, 0)],
    'F': [(0, 1), (1, 0)],
    '7': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '.': [],
    'S': [(-1, 0), (0, -1), (0, 1), (1, 0)]
}

class Node:
    def __init__(self, x: int, y: int, symbol: str):
        self.xy = (x, y)
        self.symbol = symbol
        self.neighbors = []
        self.connected_xy = [(self.xy[0] + shift[0], self.xy[1] + shift[1]) for shift in shifts[self.symbol]]

    def add_neighbor(self, other: Node) -> None:
        self.neighbors.append(other)
        other.neighbors.append(self)

    def connected(self, neighbor):
        for shift in shifts[self.symbol]:
            if neighbor.xy == (self.xy[0] + shift[0], self.xy[1] + shift[1]):
                return True

    def connections(self):
        return [neighbor for neighbor in self.neighbors if self.connected(neighbor) and neighbor.connected(self)]

class NodeMap:
    def __init__(self, raw_input):
        self.nodes, self.start_node = self.to_nodes(raw_input)
        self.node_traversal = self.get_traversal()

    def to_nodes(self, raw_input: str) -> (list[list[Node]], Node):
        nodes = []
        start_node = None
        for y, line in enumerate(raw_input.strip().split('\n')):
            nodes.append([])
            for x, symbol in enumerate(line.strip()):
                n = Node(x, y, symbol)
                nodes[y].append(n)
                if n.symbol == 'S':
                    start_node = n
        for node_line in nodes:
            for node in node_line:
                if node.xy[0] + 1 < len(nodes[node.xy[1]]):
                    node.add_neighbor(nodes[node.xy[1]][node.xy[0] + 1])
                if node.xy[1] + 1 < len(nodes):
                    node.add_neighbor(nodes[node.xy[1] + 1][node.xy[0]])
        return nodes, start_node

    def get_traversal(self) -> list[Node]:
        node_traversal = [self.start_node]
        next_node = self.start_node.connections()[0]
        while next_node != self.start_node:
            node_traversal.append(next_node)
            next_node = [conn for conn in node_traversal[-1].connections() if conn != node_traversal[-2]][0]
        return node_traversal

    def get_in_nodes(self):
        # Need to substitute '.' for unused pipes and the actual start node type for 'S'
        for node_line in self.nodes:
            for node in node_line:
                if node not in self.node_traversal:
                    node.symbol = '.'
        start_conns = sorted(
            [(self.node_traversal[1].xy[0] - self.node_traversal[0].xy[0], self.node_traversal[1].xy[1] - self.node_traversal[0].xy[1]),
             (self.node_traversal[-1].xy[0] - self.node_traversal[0].xy[0], self.node_traversal[-1].xy[1] - self.node_traversal[0].xy[1])])
        self.start_node.symbol = [symbol for symbol, all_shifts in shifts.items() if
                        all([shift in start_conns for shift in all_shifts]) and symbol not in ['.', 'S']][0]

        # An in-node crosses an odd number of "up" (or "down") nodes when moving to the right or left edge.
        # See: Ray casting algorithm
        in_nodes = []
        for node_line in self.nodes:
            for node in node_line:
                if node.symbol == '.':
                    count = 0
                    x = node.xy[0] + 1
                    while x < len(node_line):
                        if node_line[x].symbol in ['|', 'J', 'L']:
                            count += 1
                        x += 1
                    if count % 2 == 1:
                        in_nodes.append(node)
        return in_nodes



def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
        """.strip()

    nodes = NodeMap(raw_input)

    # part 1
    print(len(nodes.node_traversal) // 2)

    # part 2
    print(len([n.xy for n in nodes.get_in_nodes()]))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
