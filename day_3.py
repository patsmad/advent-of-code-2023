from __future__ import annotations

import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Symbol:
    def __init__(self, value, x, y) -> None:
        self.value: str = value
        self.x: int = x
        self.y: int = y

    def numbers(self, numbers: list[Number]) -> list[Number]:
        return [n for n in numbers if abs(self.x - n.x) < 2 and self.y + 1 >= n.y_start and self.y - 1 <= n.y_end]

    def gear_ratio(self, numbers: list[Number]) -> int:
        filtered_numbers: list[Number] = self.numbers(numbers)
        return (self.value == '*' and len(filtered_numbers) == 2 and filtered_numbers[0].value * filtered_numbers[1].value) or 0

class Number:
    def __init__(self, value, x, y_start, y_end) -> None:
        self.value: int = value
        self.x: int = x
        self.y_start: int = y_start
        self.y_end: int = y_end

    def symbols(self, symbols: list[Symbol]) -> list[Symbol]:
        return [s for s in symbols if abs(self.x - s.x) < 2 and self.y_start <= s.y + 1 and self.y_end >= s.y - 1]

    def engine(self, symbols: list[Symbol]) -> int:
        return (len(self.symbols(symbols)) > 0 and self.value) or 0

class Grid:
    def __init__(self, raw_input):
        lines = [line.strip() for line in raw_input.strip().split('\n')]
        self.numbers: list[Number] = []
        self.symbols: list[Symbol] = []
        for i, line in enumerate(lines):
            curr_num: list[str] = []
            for j, c in enumerate(line):
                if re.match('[0-9]', c):
                    curr_num.append(c)
                else:
                    if c != '.':
                        self.symbols.append(Symbol(c, i, j))
                    if len(curr_num) > 0:
                        self.numbers.append(Number(int(''.join(curr_num)), i, j - len(curr_num), j - 1))
                        curr_num = []
            if len(curr_num) > 0:
                self.numbers.append(Number(int(''.join(curr_num)), i, len(line) - len(curr_num), len(line) - 1))

    def engines(self) -> int:
        return sum([number.engine(self.symbols) for number in self.numbers])

    def gear_ratio(self) -> int:
        return sum([symbol.gear_ratio(self.numbers) for symbol in self.symbols])

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
            467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598..
        """.strip()

    g: Grid = Grid(raw_input)

    # part 1
    print(g.engines())

    # part 2
    print(g.gear_ratio())

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
