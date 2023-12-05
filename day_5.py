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

def map_item(source: int, maps: list[(int, int, int)]) -> int:
    for map_item in maps:
        if source < map_item[0]:
            return source
        if map_item[0] <= source < map_item[0] + map_item[2]:
            return map_item[1] + (source - map_item[0])
    return source

def get_new_sources(source: (int, int), maps: list[(int, int, int)]) -> list[(int, int)]:
    idxs = sorted(list(set([source[0], source[0] + source[1]] + [m[0] + m[2] for m in maps])))
    new_sources = []
    for idx, next_idx in zip(idxs[:-1], idxs[1:]):
        if source[0] <= idx < source[0] + source[1]:
            new_sources.append((idx, next_idx - idx))
    return new_sources

def map_single_range(source: (int, int), maps: list[(int, int, int)]) -> (int, int):
    for map_item in maps:
        if source[0] < map_item[0]:
            return source
        if map_item[0] <= source[0] < map_item[0] + map_item[2]:
            return (map_item[1] + source[0] - map_item[0], source[1])
    return source

def map_range(source: (int, int), maps: list[(int, int, int)]) -> list[(int, int)]:
    new_sources = get_new_sources(source, maps)
    dests = []
    for source in new_sources:
        dests.append(map_single_range(source, maps))
    return dests

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
    min_value = None
    for seed in seeds:
        value = seed
        for item_map in all_maps:
            value = map_item(value, item_map)
        if min_value is None or value < min_value:
            min_value = value
    print(min_value)

    # part 2
    min_value = None
    for start, l in [seeds[i:i+2] for i in range(0, len(seeds), 2)]:
        values = [(start, l)]
        print(values)
        for item_map in all_maps:
            new_values = []
            for value in values:
                new_values += map_range(value, item_map)
            values = new_values
            print(values)
        print()
        new_min_value = min([a[0] for a in values])
        if min_value is None or new_min_value < min_value:
            min_value = new_min_value
    print(min_value)



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
