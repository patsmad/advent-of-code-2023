import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

exchangers = {
    '.': {'N': ['N'], 'E': ['E'], 'S': ['S'], 'W': ['W']},
    '/': {'N': ['E'], 'E': ['N'], 'S': ['W'], 'W': ['S']},
    '\\': {'N': ['W'], 'E': ['S'], 'S': ['E'], 'W': ['N']},
    '|': {'N': ['N'], 'E': ['N', 'S'], 'S': ['S'], 'W': ['N', 'S']},
    '-': {'N': ['E', 'W'], 'E': ['E'], 'S': ['E', 'W'], 'W': ['W']}
}

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.exchanger = exchangers[symbol]
        self.directions_used = []
        self.neighbors = {}
        self.energized = False

    def add_neighbor(self, neighbor, dir):
        self.neighbors[dir] = neighbor

    def move_into(self, dir):
        if dir not in self.directions_used:
            self.energized = True
            self.directions_used.append(dir)
            return [(dir, self.neighbors[dir]) for dir in self.exchanger[dir] if dir in self.neighbors]
        else:
            return []

    def reset(self):
        self.energized = False
        self.directions_used = []

class Grid:
    def __init__(self, raw_input):
        self.nodes = self.get_nodes(raw_input)

    def get_nodes(self, raw_input):
        nodes = []
        for line in raw_input.strip().split('\n'):
            nodes.append([])
            for c in line.strip():
                nodes[-1].append(Node(c))
        for i in range(1, len(nodes)):
            nodes[i][0].add_neighbor(nodes[i-1][0], 'N')
            nodes[i-1][0].add_neighbor(nodes[i][0], 'S')
        for i in range(1, len(nodes[0])):
            nodes[0][i].add_neighbor(nodes[0][i-1], 'W')
            nodes[0][i-1].add_neighbor(nodes[0][i], 'E')
        for i in range(1, len(nodes)):
            for j in range(1, len(nodes[i])):
                nodes[i][j].add_neighbor(nodes[i-1][j], 'N')
                nodes[i-1][j].add_neighbor(nodes[i][j], 'S')
                nodes[i][j].add_neighbor(nodes[i][j-1], 'W')
                nodes[i][j-1].add_neighbor(nodes[i][j], 'E')
        return nodes

    def run_beams(self, beams):
        while len(beams) > 0:
            new_beams = []
            for beam in beams:
                new_beams += beam[1].move_into(beam[0])
            beams = new_beams

    def reset(self):
        for node_line in self.nodes:
            for n in node_line:
                n.reset()

    def energized(self):
        return sum([n.energized for node_line in self.nodes for n in node_line])

    def to_str(self):
        return '\n'.join([''.join([n.symbol for n in node_line]) for node_line in self.nodes])

    def to_energized(self):
        return '\n'.join([''.join(['#' if n.energized else '.' for n in node_line]) for node_line in self.nodes])


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\\
        ..../.\\\\..
        .-.-/..|..
        .|....-|.\\
        ..//.|....
        """.strip()
    g = Grid(raw_input)

    # part 1
    g.run_beams([('E', g.nodes[0][0])])
    print(g.energized())

    # part 2
    max_value = 0
    for i in range(len(g.nodes)):
        g.reset()
        g.run_beams([('E', g.nodes[i][0])])
        if g.energized() > max_value:
            max_value = g.energized()
        g.reset()
        g.run_beams([('W', g.nodes[i][-1])])
        if g.energized() > max_value:
            max_value = g.energized()
    for i in range(len(g.nodes[0])):
        g.reset()
        g.run_beams([('S', g.nodes[0][i])])
        if g.energized() > max_value:
            max_value = g.energized()
        g.reset()
        g.run_beams([('N', g.nodes[-1][i])])
        if g.energized() > max_value:
            max_value = g.energized()
    print(max_value)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
