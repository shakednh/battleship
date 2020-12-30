import logging

from config.game_conf import string_to_orientation, battleship_sizes
from config.request_conf import ResultCode
from config.user_handler_conf import ActionType
from src.game.battleship import Battleship
from src.game.board import Board

logger = logging.getLogger(__name__)


class UserHandler:
    def get_board(self):
        # TODO add board positioning validation and retry logic
        battleships = [self.get_ship(i, length) for i, length in enumerate(battleship_sizes, 1)]
        return Board(battleships)

    def get_ship(self, index, length):
        # TODO add coordinates validations and retry logic
        print(f'Ship {index}, of length {length}:')
        x, y = self.get_coordinates()
        raw_orientation = input('enter orientation(up, down, left, right): ')
        # TODO add retry mechanisms
        orientation = string_to_orientation[raw_orientation.lower()]
        return Battleship(x, y, orientation, length)

    def get_guess(self):
        print('Where you want to hit?')
        x, y = self.get_coordinates()
        return x, y

    def get_coordinates(self):
        x = int(input('enter x coordinate: '))
        y = int(input('enter y coordinate: '))
        return x, y

    def print_result_code(self, result_code: ResultCode):
        print(f'Result is {result_code.name}')

    def print_enemy_guess_result(self, x, y, result_code: ResultCode):
        print(f'Enemy tryed to hit {x},{y} - result is {result_code.name}')

    def get_wanted_action(self):
        answer = input(f'You want to wait for connection or try to connect someone(wait/connect): ')
        # TODO add retry mechanism
        return ActionType[answer.upper()]

    def get_ip(self):
        ip = input('Enter ip: ')
        # TODO - add ip format validation and retry mechanism
        return ip

    def print_win(self):
        print("WooooWeeee you won this match!!!")

    def print_lose(self):
        print("You lost this one...")
