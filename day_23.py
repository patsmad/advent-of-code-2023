import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

match_symbol = {'>': (0, 1), 'v': (1, 0), '^': (-1, 0), '<': (0, -1)}

class Node:
    def __init__(self, yx):
        self.yx = yx

def get_next(grid, s, last_s):
    steps = []
    for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        symbol = grid[s[0] + d[0]][s[1] + d[1]]
        if symbol != '#' and (s[0] + d[0], s[1] + d[1]) != last_s:
            steps.append((s[0] + d[0], s[1] + d[1]))
    return steps

def advance(grid, s, last_s):
    steps = get_next(grid, s, last_s)
    n = 1
    while len(steps) == 1:
        last_s = s
        s = steps[0]
        n += 1
        if s == (len(grid) - 1, len(grid[-1]) - 2):
            break
        steps = get_next(grid, s, last_s)
    return s, steps, n

def get_max(edges, start_point, end_point):
    out = []
    for n1, n2, n in edges:
        if n2.yx == end_point:
            if n1.yx == start_point:
                out.append(n)
            else:
                out.append(n + get_max(edges, start_point, n1.yx))
    return max(out)

def get_double_max(edges, start_point, end_point, path):
    global overall_max
    max_value = 0
    for n1, n2, n in edges:
        if n2.yx == end_point and n1.yx not in path:
            if n1.yx == start_point:
                if n > max_value:
                    max_value = n
            else:
                new_n = get_double_max(edges, start_point, n1.yx, path + [n1.yx])
                if new_n > 0 and n + new_n > max_value:
                    max_value = new_n + n
    return max_value

def all_paths(edges, start_point, end_point, path):
    out = []
    for n1, n2, n in edges:
        new_path = path + [n1.yx]
        if n2.yx == end_point and n1.yx not in path:
            if n1.yx == start_point:
                out.append(new_path)
            else:
                out += all_paths(edges, start_point, n1.yx, new_path)
    print(len(out))
    return out

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
        """.strip()

    grid = [[c for c in line.strip()] for line in raw_input.strip().split('\n')]
    start_point = (0, 1)
    end_point = (len(grid) - 1, len(grid[-1]) - 2)

    # part 1
    last_s = (0, 1)
    s = (1, 1)
    nodes = {last_s: Node(last_s)}
    queue = [(s, last_s)]
    edges = {}
    while len(queue) > 0:
        s, last_s = queue.pop(0)
        start_node = nodes[last_s]
        new_s, steps, n = advance(grid, s, last_s)
        if new_s not in nodes:
            nodes[new_s] = Node(new_s)
        edges[(s, last_s)] = (start_node, nodes[new_s], n)
        for step in steps:
            if new_s != end_point and \
                    (step[0] - new_s[0], step[1] - new_s[1]) == match_symbol[grid[step[0]][step[1]]] and \
                    (step, new_s) not in edges and \
                    (step, new_s) not in queue:
                queue.append((step, new_s))

    print(get_max(edges.values(), start_point, end_point))

    # part 2
    double_edges = []
    for n1, n2, n in edges.values():
        double_edges += [(n1, n2, n), (n2, n1, n)]
    print(get_double_max(double_edges, start_point, end_point, [end_point]))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
