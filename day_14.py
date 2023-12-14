import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.neighbors = {'N': None, 'S': None, 'E': None, 'W': None}

    def add_neighbor(self, neighbor, dir):
        self.neighbors[dir] = neighbor

    def roll(self, dir):
        if self.symbol == 'O' and self.neighbors[dir] is not None and self.neighbors[dir].symbol == '.':
            self.symbol = '.'
            self.neighbors[dir].symbol = 'O'
            return 1
        return 0

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

    def to_str(self):
        return '\n'.join([''.join([n.symbol for n in node_line]) for node_line in self.nodes])

    def roll(self, dir):
        moves = 0
        for i in (dir == 'S' and range(len(self.nodes) - 1, -1, -1)) or range(len(self.nodes)):
            for j in (dir == 'E' and range(len(self.nodes[0]) - 1, -1, -1)) or range(len(self.nodes[0])):
                moves += self.nodes[i][j].roll(dir)
        return moves

    def cycle(self):
        for dir in ['N', 'W', 'S', 'E']:
            while self.roll(dir) > 0:
                self.roll(dir)

    def score(self):
        score = 0
        for i, node_line in enumerate(self.nodes):
            for node in node_line:
                if node.symbol == 'O':
                    score += len(self.nodes) - i
        return score

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """.strip()


    # part 1
    grid = Grid(raw_input)
    while grid.roll('N') > 0:
        pass
    print(grid.score())

    # part 2
    grid = Grid(raw_input)
    cycle_strs = []
    while grid.to_str() not in cycle_strs:
        cycle_strs.append(grid.to_str())
        grid.cycle()
    cycle_strs.append(grid.to_str())
    idx = cycle_strs.index(cycle_strs[-1])
    final_grid = Grid(cycle_strs[(1000000000 - idx) % (len(cycle_strs) - idx - 1) + idx])
    print(final_grid.score())


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
