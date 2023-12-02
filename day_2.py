from __future__ import annotations

import argparse
from get_input import get_input
import re

def day_num() -> int:
    return int(re.search('.*day_([0-9]*)\.py', __file__).group(1))

day: int = day_num()

class Dice:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.blue = blue
        self.green = green

    def possible(self, config: Dice) -> bool:
        return config.red >= self.red and \
            config.blue >= self.blue and \
            config.green >= self.green

    @staticmethod
    def from_str(dice_str: str) -> Dice:
        red_search = re.search('([0-9]*) red', dice_str)
        green_search = re.search('([0-9]*) green', dice_str)
        blue_search = re.search('([0-9]*) blue', dice_str)
        return Dice(
            red=int(red_search.group(1)) if red_search is not None else 0,
            green=int(green_search.group(1)) if green_search is not None else 0,
            blue=int(blue_search.group(1)) if blue_search is not None else 0
        )

    def __str__(self) -> str:
        return f'{self.red} red, {self.green} green, {self.blue} blue'

class Game:
    def __init__(self, id: int, dices: list[Dice]) -> None:
        self.id = id
        self.dices = dices

    def possible(self, config: Dice) -> bool:
        for dice in self.dices:
            if not dice.possible(config):
                return False
        return True

    def power(self) -> int:
        return max([dice.red for dice in self.dices]) * \
            max([dice.green for dice in self.dices]) * \
            max([dice.blue for dice in self.dices])

    @staticmethod
    def from_str(game_str: str) -> Game:
        game_id_str, dices_str = game_str.split(':')
        game_id: int = int(game_id_str.split(' ')[-1])
        dices: list[Dice] = [Dice.from_str(dice_str) for dice_str in dices_str.split(';')]
        return Game(id=game_id, dices=dices)

    def __str__(self) -> str:
        dice_str = '; '.join([dice.__str__() for dice in self.dices])
        return f'Game {self.id}: {dice_str}'

def format(raw_input: str) -> list[Game]:
    return [Game.from_str(game_str) for game_str in raw_input.strip().split('\n')]

def run(test: bool) -> None:
    if not test:
        raw_input: str = get_input(day)
    else:
        raw_input: str = """
            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """.strip()

    games: list[Game] = format(raw_input)

    # part 1
    config: Dice = Dice(red=12, green=13, blue=14)
    print(sum([game.id for game in games if game.possible(config)]))

    # part 2
    print(sum([game.power() for game in games]))

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args: argparse.Namespace = parser.parse_args()
    run(args.test)
