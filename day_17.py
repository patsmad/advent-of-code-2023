import argparse
from get_input import get_input
import re
import math

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

dxs = {
    'N': (1, 0),
    'E': (0, 1),
    'S': (-1, 0),
    'W': (0, -1)
}

opposite = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E'
}

class Node:
    def __init__(self, x, y, d, w):
        self.x = x
        self.y = y
        self.d = d
        self.three_in_a_row = self.d[0] == self.d[1] and self.d[0] == self.d[2]
        self.w = w
        self.value = math.inf

    def edges(self, m):
        edges = []
        for dir in ['N', 'E', 'S', 'W']:
            if dir != opposite[self.d[2]] and (not self.three_in_a_row or dir != self.d[2]):
                new_x = self.x + dxs[dir][0]
                new_y = self.y + dxs[dir][1]
                if 0 <= new_x < m[0] and 0 <= new_y < m[1]:
                    edges.append((self.d[1], self.d[2], dir, new_x, new_y))
        return edges


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """.strip()

    nodes = [list(map(int, line.strip())) for line in raw_input.strip().split('\n')]
    m = (len(nodes), len(nodes[0]))

    node_dict = {}
    queue = []
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            for d1 in ['N', 'E', 'S', 'W']:
                for d2 in ['N', 'E', 'S', 'W']:
                    for d3 in ['N', 'E', 'S', 'W']:
                        n = Node(i, j, (d1, d2, d3), nodes[i][j])
                        node_dict[(d1, d2, d3, i, j)] = n
                        if i == 0 and j == 0:
                            queue.append(n)
                            n.value = 0

    # part 1
    out = {}
    while 1:
        queue = sorted(queue, key=lambda n: n.value)
        node = queue.pop(0)
        while (node.d[0], node.d[1], node.d[2], node.x, node.y) in out:
            node = queue.pop(0)
        if node.x == m[0] - 1 and node.y == m[1] - 1:
            print(node.x, node.y, node.value)
            break
        for new_edge in node.edges(m):
            new_node = node_dict[new_edge]
            if node.value + new_node.w < new_node.value:
                new_node.value = node.value + new_node.w
            if new_node not in queue:
                queue.append(new_node)
        out[(node.d[0], node.d[1], node.d[2], node.x, node.y)] = True
        print(len(out))


    # part 2

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
