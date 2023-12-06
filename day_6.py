import argparse
from get_input import get_input
import re
import math

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def get_combos(time: int, distance: int) -> (int, int):
    r: int = (time ** 2 - 4 * distance) ** (1 / 2)
    min_time = math.floor((time - r) / 2 + 1)
    max_time = math.ceil((time + r) / 2 - 1)
    return max_time - min_time + 1


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        Time:      7  15   30
        Distance:  9  40  200
        """.strip()

    time_str, distance_str = raw_input.strip().split('\n')

    # part 1
    times = list(map(int, time_str.split(':')[1].strip().split()))
    distances = list(map(int, distance_str.split(':')[1].strip().split()))
    m = 1
    for time, distance in zip(times, distances):
        m *= get_combos(time, distance)
    print(m)

    # part 2
    time = int(''.join(time_str.split(':')[1].strip().split()))
    distance = int(''.join(distance_str.split(':')[1].strip().split()))
    print(get_combos(time, distance))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
