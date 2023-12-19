import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def format(raw_input):
    commands = []
    for line in raw_input.strip().split('\n'):
        d, n, c = re.fullmatch('([RUDL]) ([0-9]*) \((.*)\)', line.strip()).groups()
        commands.append((d, int(n), c))
    return commands

dir = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

dir_from_num = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

num_from_hex = {
    str(i): i for i in range(10)
}
num_from_hex['a'] = 10
num_from_hex['b'] = 11
num_from_hex['c'] = 12
num_from_hex['d'] = 13
num_from_hex['e'] = 14
num_from_hex['f'] = 15

def from_hex(h):
    n = 0
    for i, c in enumerate(h[1:6]):
        n += 16**(4 - i) * num_from_hex[c]
    return dir_from_num[h[-1]], n, h

def get_points(commands):
    points = [(0, 0)]
    for command in commands:
        d = dir[command[0]]
        new_point = (points[-1][0] + d[0] * command[1], points[-1][1] + d[1] * command[1])
        points.append(new_point)
    return points[:-1]

def get_s_points(points):
    s_points = {}
    for p in points:
        if p[0] not in s_points:
            s_points[p[0]] = set()
        s_points[p[0]] |= {p[1]}
    return s_points

def combine(curr, new):
    return curr ^ new

def segment_in(segment_in_question, segments):
    for segment in segments:
        if segment_in_question[0] >= segment[0] and segment_in_question[1] <= segment[1]:
            return True
    return False

def to_segment(s_points):
    sorted_list = sorted(s_points)
    return [(sorted_list[i], sorted_list[i + 1]) for i in range(0, len(sorted_list), 2)]

def get_added_segments(s_points, line_segments):
    added_segments = []
    for segment in to_segment(s_points):
        if not segment_in(segment, line_segments):
            added_segments.append(segment)
    return added_segments

def get_num(points):
    num = 0
    s_points = get_s_points(points)
    line_points = set()
    last_y = min(s_points)
    for y in sorted(s_points):
        combined_points = combine(line_points, s_points[y])
        line_segments = to_segment(line_points)
        added_segments = get_added_segments(s_points[y], line_segments)
        added_num = sum([s[1] - s[0] - 1 + len(set(s) - line_points) for s in added_segments])
        last_width = sum([s[1] - s[0] + 1 for s in line_segments])
        height = y - last_y
        num += added_num + last_width * height
        line_points = combined_points
        last_y = y
    return num


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """.strip()

    commands = format(raw_input)

    # part 1
    points = get_points(commands)
    print(get_num(points))

    # part 2
    new_commands = [from_hex(command[2]) for command in commands]
    new_points = get_points(new_commands)
    print(get_num(new_points))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
