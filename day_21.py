import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def dirs_bounded(y, x, my, mx):
    dirs = []
    for d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if 0 <= y + d[0] < my and 0 <= x + d[1] < mx:
            dirs.append((y + d[0], x + d[1]))
    return dirs

def dirs_unbounded(tile, y, x, my, mx):
    dirs = []
    for d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        ny = (y + d[0]) % my
        nx = (x + d[1]) % mx
        n_tile = (tile[0] + (y + d[0]) // my, tile[1] + (x + d[1]) // mx)
        dirs.append((n_tile, (ny, nx)))
    return dirs

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """.strip()

    nodes = [[c for c in line.strip()] for line in raw_input.strip().split('\n')]
    my = len(nodes)
    mx = len(nodes[0])
    start = [(i, j) for i, line in enumerate(nodes) for j, c in enumerate(line) if c == 'S'][0]
    nodes[start[0]][start[1]] = '.'

    # part 1
    node_set = {start}
    for _ in range(64):
        node_set = set([n for node in node_set for n in dirs_bounded(node[0], node[1], my, mx) if nodes[n[0]][n[1]] == '.'])
    print(len(node_set))

    # part 2
    even_set = {((0, 0), start)}
    odd_set = set()
    even_count = 0
    odd_count = 0
    counts = [0]
    for i in range(1, 500):
        new_set = set([(t, n) for tile, node in (odd_set if i % 2 == 0 else even_set)
                       for t, n in dirs_unbounded(tile, node[0], node[1], my, mx)
                        if nodes[n[0]][n[1]] != '#'])
        if i % 2 == 0:
            even_count += len(even_set)
            even_set = new_set - even_set
        else:
            odd_count += len(odd_set)
            odd_set = new_set - odd_set
        counts.append(len(even_set) + even_count if i % 2 == 0 else len(odd_set) + odd_count)

    N = 26501365 + 1
    x = counts
    d = [counts[i] - counts[i - 1] for i in range(1, len(counts))]
    cycle = 131
    while len(x) < N:
        d.append(d[-cycle] + d[-cycle] - d[-2*cycle])
        x.append(x[-1] + d[-1])
    print(x[-1])


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
