import argparse
from collections.abc import Callable
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

card_order: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card_order_joker: list[str] = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

def hand_value(hand: str) -> int:
    count: dict[str, int] = {}
    for card in hand:
        count[card] = count.get(card, 0) + 1
    hand_value: int = sum([count[card] for card in hand])
    return hand_value

def hand_value_joker(hand: str) -> int:
    possible_hand_values = [hand_value(hand.replace('J', possible_card)) for possible_card in card_order_joker]
    return max(possible_hand_values)

def sort_fnc(card_order: list[str], hand_value_fnc: Callable[[str], int]) -> Callable[[str], tuple]:
    card_dict: dict[str, int] = {card: i for i, card in enumerate(card_order)}
    def hand_sort(hand: str) -> tuple:
        return hand_value_fnc(hand), *[card_dict[card] for card in hand]
    return hand_sort

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
    for rank, hand in enumerate(sorted(hands, key=sort_fnc(card_order, hand_value))):
        part_1 += (rank + 1) * bids[hand]
    print(part_1)

    # part 2
    part_2 = 0
    for rank, hand in enumerate(sorted(hands, key=sort_fnc(card_order_joker, hand_value_joker))):
        part_2 += (rank + 1) * bids[hand]
    print(part_2)

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
