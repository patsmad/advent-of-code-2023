import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def intersect_dim(d1, d2):
    return (d1[0] <= d2[0] and d1[1] >= d2[0]) or \
        (d1[1] >= d2[1] and d1[0] <= d2[1]) or \
        (d1[0] >= d2[0] and d1[1] <= d2[1])

def intersect_seg(seg1, seg2):
    return intersect_dim([a[0] for a in seg1], [a[0] for a in seg2]) and \
        intersect_dim([a[1] for a in seg1], [a[1] for a in seg2])


def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        """.strip()

    segments = []
    for line in raw_input.strip().split('\n'):
        d1, d2 = [tuple(map(int, s.split(','))) for s in line.strip().split('~')]
        segments.append((d1, d2))
    segments = sorted(segments, key=lambda s: s[0][2])

    # part 1
    collapsed_segs = []
    while len(segments) > 0:
        segment = segments.pop(0)
        intersected_segs = [seg for seg in collapsed_segs if intersect_seg(segment, seg)] + [((0, 0, 0), (0, 0, 0))]
        new_z = max([d[2] for seg in intersected_segs for d in seg]) + 1
        l = abs(segment[0][2] - segment[1][2])
        collapsed_segs.append(((segment[0][0], segment[0][1], new_z), (segment[1][0], segment[1][1], new_z + l)))

    sitting_on = {seg: set() for seg in collapsed_segs}
    holding_up = {seg: set() for seg in collapsed_segs}
    for segment in collapsed_segs:
        max_z = max([a[2] for a in segment])
        for seg in collapsed_segs:
            if min([a[2] for a in seg]) == max_z + 1 and intersect_seg(segment, seg):
                sitting_on[seg] |= {segment}
                holding_up[segment] |= {seg}

    keep = set()
    for seg, sits_on in sitting_on.items():
        if len(sits_on) == 1:
            keep |= sits_on
    print(len(sitting_on) - len(keep))

    # part 2
    s = 0
    for seg in holding_up:
        falling = {seg}
        new_falling = set([s for s in holding_up[seg] if len(sitting_on[s] - falling) == 0])
        while len(new_falling) > 0:
            falling |= new_falling
            new_falling = set([s for falling_seg in new_falling for s in holding_up[falling_seg] if len(sitting_on[s] - falling) == 0])
        s += len(falling) - 1
    print(s)



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
