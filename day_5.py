import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def format_map(map_str: str) -> list:
    out = []
    for line in map_str.strip().split('\n')[1:]:
        dest, source, l = line.strip().split()
        out.append((int(source), int(dest), int(l)))
    out.sort()
    return out

def format(raw_input: str):
    split_input = raw_input.strip().split('\n\n')
    seeds = list(map(int, split_input[0].strip().split(': ')[1].split()))
    maps = map(format_map, split_input[1:])
    return seeds, list(maps)

# split_value guarantees that if item_value[0] < map_item[0] then it is outside any map
# and if item_value[0] is inside a map, then the entirety of the source uses that map
def map_range(item_value: (int, int), maps: list[(int, int, int)]) -> (int, int):
    for map_item in maps:
        if item_value[0] < map_item[0]:
            return item_value
        if map_item[0] <= item_value[0] < map_item[0] + map_item[2]:
            return (map_item[1] + item_value[0] - map_item[0], item_value[1])
    return item_value

# Splits a value range into pieces at the boundaries of a list of maps
def split_value(value: (int, int), maps: list[(int, int, int)]) -> list[(int, int)]:
    idxs = sorted(list(set([value[0], value[0] + value[1]] + [m[0] + m[2] for m in maps])))
    new_values = []
    for idx, next_idx in zip(idxs[:-1], idxs[1:]):
        if value[0] <= idx < value[0] + value[1]:
            new_values.append((idx, next_idx - idx))
    return new_values

# Can consider all items at the same time, split by map boundary and map
def get_min_value(item_values: list[(int, int)], all_maps: list[list[(int, int, int)]]) -> int:
    for item_map in all_maps:
        item_values = [map_range(single_value, item_map) for item_value in item_values
                       for single_value in split_value(item_value, item_map)]
    return min([a[0] for a in item_values])

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
        """.strip()

    seeds, all_maps = format(raw_input)

    # part 1
    print(get_min_value([(s, 1) for s in seeds], all_maps))

    # part 2
    print(get_min_value([seeds[i:i+2] for i in range(0, len(seeds), 2)], all_maps))



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
