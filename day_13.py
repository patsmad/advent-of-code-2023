import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_reflections(maze):
    rows = []
    for i in range(len(maze) - 1):
        if all([maze[i - j] == maze[i + j + 1] for j in range(len(maze) - 1) if i - j >= 0 and i + j + 1 < len(maze)]):
            rows.append(i + 1)
    return rows

def line_of_reflection(maze):
    rows = get_reflections(maze)
    transpose_maze = [''.join([maze[i][j] for i in range(len(maze))]) for j in range(len(maze[0]))]
    cols = get_reflections(transpose_maze)
    return [100 * row for row in rows] + cols

def test_all(maze):
    orig = set(line_of_reflection(maze))
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            test_maze = maze[:i] + [maze[i][:j] + ('.' if maze[i][j] == '#' else '#') + maze[i][j+1:]] + maze[i+1:]
            new_set = set(line_of_reflection(test_maze)) - orig
            if len(new_set) > 0:
                return list(new_set)

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.
        
        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """.strip()

    lines = [[line.strip() for line in block.strip().split('\n')] for block in raw_input.strip().split('\n')]
    mazes = []
    curr_maze = []
    for line in lines:
        if line == ['']:
            mazes.append(curr_maze)
            curr_maze = []
        else:
            curr_maze.append(line[0])
    mazes.append(curr_maze)

    # part 1
    s = 0
    for maze in mazes:
        s += line_of_reflection(maze)[0]
    print(s)

    # part 2
    s = 0
    for maze in mazes:
        s += test_all(maze)[0]
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
