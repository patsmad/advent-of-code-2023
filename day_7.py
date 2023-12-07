import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

def format(raw_input: str) -> (list, dict[str, int]):
    bids = {}
    hands = []
    for line in raw_input.strip().split('\n'):
        hand, bid = line.strip().split()
        hands.append(hand)
        bids[hand] = int(bid)
    return hands, bids

card_value: dict[str, int] = {card: i + 1 for i, card in enumerate(
    ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
)}
card_value_joker: dict[str, int] = {card: i + 1 for i, card in enumerate(
    ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
)}

def hand_value(hand: str):
    count: dict[str, int] = {}
    for card in hand:
        count[card] = count.get(card, 0) + 1
    hand_value: int = sum([count[card] for card in hand])
    return hand_value, *[card_value.get(card, 0) for card in hand]

def joker_hand_value(hand: str):
    possible_hand_values = [hand_value(hand.replace('J', possible_card))[0] for possible_card in card_value_joker.keys()]
    return max(possible_hand_values), *[card_value_joker.get(card, 0) for card in hand]

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """.strip()

    hands, bids = format(raw_input)

    # part 1
    part_1 = 0
    for rank, hand in enumerate(sorted(hands, key=hand_value)):
        part_1 += (rank + 1) * bids[hand]
    print(part_1)

    # part 2
    part_2 = 0
    for rank, hand in enumerate(sorted(hands, key=joker_hand_value)):
        part_2 += (rank + 1) * bids[hand]
    print(part_2)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
