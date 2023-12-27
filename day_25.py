import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def min_cut_phase(v, e, a):
    if len(v) == 2:
        return e[v[0]][v[1]]

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        jqt: rhn xhk nvd
        rsh: frs pzl lsr
        xhk: hfx
        cmg: qnr nvd lhk bvb
        rhn: xhk bvb hfx
        bvb: xhk hfx
        pzl: lsr hfx nvd
        qnr: nvd
        ntq: jqt hfx bvb xhk
        nvd: lhk
        lsr: lhk
        rzs: qnr cmg lsr rsh
        frs: qnr lhk lsr
        """.strip()

    data = []
    for line in raw_input.strip().split('\n'):
        key, connections = line.strip().split(': ')
        for connection in connections.strip().split():
            data.append(tuple(sorted((key, connection))))
    data = list(set(data))

    v = list(set([b for a in data for b in a]))
    e = {}
    for d in data:
        if d[0] not in e:
            e[d[0]] = {}
        if d[1] not in e:
            e[d[1]] = {}
        e[d[0]][d[1]] = 1
        e[d[1]][d[0]] = 1

    # part 1
    e['A'] = {a: 0 for a in v}

    A = [v]
    while len(v) > 0:
        v = sorted(v, key=lambda k: e['A'][k])
        A.append(v.pop())
        for edge in e[A[-1]]:
            if edge not in e['A']:
                e['A'][edge] = 0
            e['A'][edge] += e[A[-1]][edge]
        e.pop(A[-1])
        if sum([e['A'][a] for a in v]) == 3:
            print(len(v) * (len(list(set([b for a in data for b in a]))) - len(v)))

    # part 2
    # Press a button

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
