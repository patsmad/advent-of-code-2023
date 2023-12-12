import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

memo = {}

def recurs(curr_num, input_str, input_nums):
    if len(input_str) == 0:
        return 1 * ((curr_num == 0 and len(input_nums) == 0) or (len(input_nums) == 1 and input_nums[0] == curr_num))
    if len(input_nums) == 0:
        return 1 * (curr_num == 0 and all([c != '#' for c in input_str]))
    key = input_str + ';' + ','.join(map(str,input_nums)) + ';' + str(curr_num)
    if key not in memo:
        if input_str[0] == '.':
            if curr_num > 0:
                memo[key] = (input_nums[0] == curr_num and recurs(0, input_str[1:], input_nums[1:])) or 0
            else:
                memo[key] = recurs(0, input_str[1:], input_nums)
        elif input_str[0] == '#':
            memo[key] = recurs(curr_num + 1, input_str[1:], input_nums)
        else:
            memo[key] = recurs(curr_num, '.' + input_str[1:], input_nums) + recurs(curr_num, '#' + input_str[1:], input_nums)
    return memo[key]


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """.strip()

    instructions = []
    for line in raw_input.strip().split('\n'):
        instruction, num_str = line.strip().split()
        instructions.append((instruction, list(map(int, num_str.split(',')))))

    # part 1
    s = 0
    for instruction, nums in instructions:
        s += recurs(0, instruction, nums)
    print(s)

    # part 2
    s = 0
    for instruction, nums in instructions:
        s += recurs(0, instruction + '?' + instruction + '?' + instruction + '?' + instruction + '?' + instruction, nums + nums + nums + nums + nums)
    print(s)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
