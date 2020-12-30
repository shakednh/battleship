from collections import defaultdict
from typing import List

from config.game_conf import orientation_to_vector
from config.request_conf import ResultCode
from src.game.battleship import Battleship


class Board:
    def __init__(self, battleships: List[Battleship]):
        self.battleships = battleships
        self.num_alive = len(battleships)

    def try_hit(self, x, y):
        for ship in self.battleships:
            result = ship.try_hit(x, y)
            if result != ResultCode.MISS:
                if result == ResultCode.HIT_FINAL:
                    self.num_alive -= 1
                if self.num_alive == 0:
                    return ResultCode.FINISH
                return result
        return ResultCode.MISS

    def is_valid_board(self):
        used_points = defaultdict(list)
        for ship in self.battleships:
            x, y = orientation_to_vector[ship.orientation]
            for i in ship.length:
                x_coord, y_coord = ship.x + i * x, ship.y + i * y
                self._check_and_append(used_points, (x_coord - 1, y_coord - 1), ship)
                self._check_and_append(used_points, (x_coord - 1, y_coord), ship)
                self._check_and_append(used_points, (x_coord - 1, y_coord + 1), ship)
                self._check_and_append(used_points, (x_coord, y_coord - 1), ship)
                self._check_and_append(used_points, (x_coord, y_coord), ship)
                self._check_and_append(used_points, (x_coord, y_coord + 1), ship)
                self._check_and_append(used_points, (x_coord + 1, y_coord - 1), ship)
                self._check_and_append(used_points, (x_coord + 1, y_coord), ship)
                self._check_and_append(used_points, (x_coord + 1, y_coord + 1), ship)

    def _check_and_append(self, dictionary, key, group):
        """
        An helper method for checking if the dictionary key already occupied by another group,
        and adding it only if not
        :param dictionary: dict
        :param key: hashable object
        :param group: object
        :return: True if added successfully
        """
        if dictionary[key]:
            for element in dictionary[key]:
                if element != group:
                    return False
        dictionary[key].append(group)
        return True
