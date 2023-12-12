import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_sum(coords, cols, rows, N):
    sum_value = 0
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            min1, max1 = (coords[i][0], coords[j][0]) if coords[i][0] < coords[j][0] else (coords[j][0], coords[i][0])
            min2, max2 = (coords[i][1], coords[j][1]) if coords[i][1] < coords[j][1] else (coords[j][1], coords[i][1])
            for c1 in range(min1 + 1, max1 + 1):
                sum_value += (c1 not in cols and N) or 1
            for c2 in range(min2 + 1, max2 + 1):
                sum_value += (c2 not in rows and N) or 1
    return sum_value


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """.strip()

    coords = [(i, j) for j, line in enumerate(raw_input.split('\n')) for i, node in enumerate(line.strip()) if node == '#']
    cols = {a[0] for a in coords}
    rows = {a[1] for a in coords}

    # part 1
    print(get_sum(coords, cols, rows, 2))

    # part 2
    print(get_sum(coords, cols, rows, 1000000))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
