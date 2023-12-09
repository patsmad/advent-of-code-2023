import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def format(raw_input: str) -> list[list[int]]:
    return [list(map(int, line.strip().split())) for line in raw_input.strip().split('\n')]

def diff(history: list[int]) -> list[int]:
    return [history[i] - history[i-1] for i in range(1, len(history))]

def get_next(history: list[int]) -> int:
    next: int = history[-1]
    while len(history) > 1:
        history: list[int] = diff(history)
        next += history[-1]
    return next

def get_first(history: list[int]) -> int:
    first: int = history[0]
    count = 0
    while len(history) > 1:
        count += 1
        history: list[int] = diff(history)
        first += history[0] * (-1)**count
    return first


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """.strip()

    histories = format(raw_input)

    # part 1
    print(sum([get_next(history) for history in histories]))

    # part 2
    print(sum([get_first(history) for history in histories]))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
