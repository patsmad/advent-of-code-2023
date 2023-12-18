import argparse
from get_input import get_input
import re
import math

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

dxs = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

opposite = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E'
}

class Node:
    def __init__(self, x, y, d, num, w):
        self.x = x
        self.y = y
        self.d = d
        self.num = num
        self.w = w
        self.value = math.inf

    def edges(self, m, min_num, max_num):
        edges = []
        for dir in ['N', 'E', 'S', 'W']:
            if dir != opposite[self.d] and (self.num >= min_num or dir == self.d) and (self.num < max_num or dir != self.d):
                new_x = self.x + dxs[dir][0]
                new_y = self.y + dxs[dir][1]
                if 0 <= new_x < m[0] and 0 <= new_y < m[1]:
                    new_num = self.num + 1 if dir == self.d else 1
                    edges.append((dir, new_num, new_x, new_y))
        return edges

def get_ans(raw_input, min_num, max_num):
    nodes = [list(map(int, line.strip())) for line in raw_input.strip().split('\n')]
    m = (len(nodes), len(nodes[0]))

    node_dict = {}
    queue = [Node(0, 0, 'E', 0, nodes[0][0]), Node(0, 0, 'S', 0, nodes[0][0])]
    for q in queue:
        q.value = 0

    out = {}
    while 1:
        queue = sorted(queue, key=lambda n: n.value)
        node = queue.pop(0)
        while (node.d, node.num, node.x, node.y) in out:
            node = queue.pop(0)
        if node.x == m[0] - 1 and node.y == m[1] - 1:
            print(node.x, node.y, node.value, node.d, node.num)
            if node.num >= min_num:
                break
        else:
            for new_edge in node.edges(m, min_num, max_num):
                if new_edge not in node_dict:
                    d, num, i, j = new_edge
                    node_dict[new_edge] = Node(i, j, d, num, nodes[i][j])
                new_node = node_dict[new_edge]
                if node.value + new_node.w < new_node.value:
                    new_node.value = node.value + new_node.w
                if new_node not in queue:
                    queue.append(new_node)
            out[(node.d, node.num, node.x, node.y)] = True
        if len(out) % 20000 == 0:
            print(len(out))


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

    # part 1
    get_ans(raw_input, 0, 3)

    # part 2
    get_ans(raw_input, 4, 10)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
