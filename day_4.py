import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Card:
    def __init__(self, line):
        id_str, num_str = line.strip().split(':')
        win_num, my_num = num_str.strip().split(' | ')
        self.id = int(id_str.split()[-1])
        self.win_set = set(map(int, win_num.strip().split()))
        self.my_set = set(map(int, my_num.strip().split()))
        self.nums = len(self.my_set & self.win_set)

    def score(self):
        return (self.nums > 0 and 2**(self.nums - 1)) or 0

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        """.strip()

    # part 1
    cards: list[Card] = [Card(line) for line in raw_input.strip().split('\n')]
    print(sum([card.score() for card in cards]))

    # part 2
    card_dict = {card.id: 1 for card in cards}
    for i, card in enumerate(cards):
        for j in range(card.nums):
            card_dict[card.id + j + 1] += card_dict[card.id]
    print(sum(card_dict.values()))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
