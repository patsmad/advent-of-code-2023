import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def to_mb_2(p, v):
    return v[1] / v[0], p[1] - v[1] / v[0] * p[0]

def intersect_2(m1, b1, m2, b2):
    if (m1 - m2) != 0:
        x = - (b1 - b2) / (m1 - m2)
        return x, m1 * x + b1

def get_vec_xy(p1, vel1, p2, vel2):
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    (u1, v1, w1), (u2, v2, w2) = vel1, vel2
    return ([-(v1 - v2), (u1 - u2), (y1 - y2), -(x1 - x2)], -x1 * v1 + x2 * v2 + y1 * u1 - y2 * u2)

def get_vec_xz(p1, vel1, p2, vel2):
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    (u1, v1, w1), (u2, v2, w2) = vel1, vel2
    return ([-(w1 - w2), (u1 - u2), (z1 - z2), -(x1 - x2)], -x1 * w1 + x2 * w2 + z1 * u1 - z2 * u2)

def get_vec(p1, vel1, p2, vel2):
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    (u1, v1, w1), (u2, v2, w2) = vel1, vel2
    return ([
                [-(v1 - v2), (u1 - u2), 0, (y1 - y2), -(x1 - x2), 0],
                [-(w1 - w2), 0, (u1 - u2), (z1 - z2), 0, -(x1 - x2)],
                [0, -(w1 - w2), (v1 - v2), 0, (z1 - z2), -(y1 - y2)]
            ],
            [
                -x1 * v1 + x2 * v2 + y1 * u1 - y2 * u2,
                -x1 * w1 + x2 * w2 + z1 * u1 - z2 * u2,
                -y1 * w1 + y2 * w2 + z1 * v1 - z2 * v2
            ]
    )

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        19, 13, 30 @ -2,  1, -2
        18, 19, 22 @ -1, -1, -2
        20, 25, 34 @ -2, -2, -4
        12, 31, 28 @ -1, -2, -1
        20, 19, 15 @  1, -5, -3
        """.strip()

    pvs = []
    for line in raw_input.strip().split('\n'):
        p, v = map(lambda pv: tuple(map(int, pv.split(', '))), line.strip().split(' @ '))
        pvs.append((p, v))

    if test:
        min_v, max_v = 7, 27
    else:
        min_v, max_v = 200000000000000, 400000000000000

    # part 1
    count = 0
    mb2s = [to_mb_2(*pv) for pv in pvs]
    for i in range(len(mb2s)):
        for j in range(i + 1, len(mb2s)):
            inter_xy = intersect_2(*mb2s[i], *mb2s[j])
            if inter_xy is not None and min_v <= inter_xy[0] <= max_v and min_v <= inter_xy[1] <= max_v:
                t1 = (inter_xy[0] - pvs[i][0][0]) / pvs[i][1][0]
                t2 = (inter_xy[0] - pvs[j][0][0]) / pvs[j][1][0]
                if t1 > 0 and t2 > 0:
                    count += 1
    print(count)

    # part 2
    import numpy as np
    A = []
    b = []
    for i in range(1, 5):
        v, out = get_vec_xy(*pvs[0], *pvs[i])
        A.append(v)
        b.append(out)
    print(list(map(int, np.linalg.inv(A).dot(b))))

    A = []
    b = []
    for i in range(1, 5):
        v, out = get_vec_xz(*pvs[0], *pvs[i])
        A.append(v)
        b.append(out)
    print(list(map(int, np.linalg.inv(A).dot(b))))

    pairs = [(i, j) for i in range(len(pvs)) for j in range(i + 1, len(pvs))]
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            A = []
            b = []
            v, out = get_vec(*pvs[pairs[i][0]], *pvs[pairs[i][1]])
            A += v
            b += out
            v, out = get_vec(*pvs[pairs[j][0]], *pvs[pairs[j][1]])
            A += v
            b += out
            val = list(map(int, np.linalg.inv(A).dot(b)))
            b_app = np.array(A).dot(val)
            if all([b_app[bi] == b[bi] for bi in range(len(b))]):
                print(val)
    # print(xxx)
    #
    # A = []
    # b = []
    # for i in range(2, 4):
    #     v, out = get_vec(*pvs[0], *pvs[i])
    #     A += v
    #     b += out
    # print(list(map(int, np.linalg.inv(A).dot(b))))
    #
    # A = []
    # b = []
    # for i in range(1, len(pvs)):
    #     v, out = get_vec(*pvs[0], *pvs[i])
    #     A += v
    #     b += out
    # print(A, b)
    # print(list(map(int, np.linalg.pinv(A).dot(b))))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
