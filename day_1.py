import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()
map_digit_str = {
    'zero': 'zero0zero',
    'one': 'one1one',
    'two': 'two2two',
    'three': 'three3three',
    'four': 'four4four',
    'five': 'five5five',
    'six': 'six6six',
    'seven': 'seven7seven',
    'eight': 'eight8eight',
    'nine': 'nine9nine'
}

def to_num(nums: str) -> int:
    return 10 * int(nums[0]) + int(nums[-1])

def replace_word_digits(input: str) -> str:
    for k, v in map_digit_str.items():
        input: str = input.replace(k, v)
    return input

def part_1_format(raw_input: str) -> list[str]:
    return re.sub('[^0-9\n]', '', raw_input).split('\n')

def part_2_format(raw_input: str) -> list[str]:
    return part_1_format(replace_word_digits(raw_input))

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day, strip=True)
    else:
        raw_input: str = """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
        """.strip()
    print(len(raw_input.split('\n')))
    print(sum([len(a) for a in raw_input.split('\n')]) / len(raw_input.split('\n')))

    # part 1
    print(sum(map(to_num, part_1_format(raw_input))))

    # part 2
    if test:
        raw_input: str = """
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
        """.strip()

    print(sum(map(to_num, part_2_format(raw_input))))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
