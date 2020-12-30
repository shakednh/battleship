import logging

from config.game_conf import string_to_orientation
from config.request_conf import ResultCode
from src.game.battleship import Battleship
from src.game.board import Board

logger = logging.getLogger(__name__)


class UserHandler:
    def get_board(self):
        battleships = [
            self.get_ship(1, 5),
            self.get_ship(2, 4),
            self.get_ship(3, 3),
            self.get_ship(4, 3),
            self.get_ship(5, 2),
        ]
        return Board(battleships)

    def get_ship(self, index, length):
        print(f'Ship {index}, of length {length}:')
        x = input('enter x coordinate: ')
        y = input('enter y coordinate: ')
        raw_orientation = input('enter orientation(up, down, left, right): ')
        orientation = string_to_orientation[raw_orientation.lower()]
        return Battleship(x, y, orientation, length)

    def get_guess(self):
        print('Where you want to hit?')
        x = input('enter x coordinate: ')
        y = input('enter y coordinate: ')
        return x, y

    def print_result_code(self, result_code: ResultCode):
        print(f'Result is {result_code.name}')
