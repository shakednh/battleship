from config.game_conf import Orientation
import logging

from config.request_conf import ResultCode

logger = logging.getLogger(__name__)


class Battleship:
    def __init__(self, x, y, orientation, length):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.hits = []

    def try_hit(self, x, y):
        """
        A method for getting a coordinate and returning if hitting this battleship
        (and add it to hits if so)
        :param x: int - the x coordinate
        :param y: int - the y coordinate
        :return: if the coordinate is hitting an unhitted spot of this battleship
        """
        if self.x == x and self.y == y:
            return self._hit_battleship(x, y)
        if self.x == x:
            if self.y < y <= self.y + self.length and self.orientation == Orientation.up:
                return self._hit_battleship(x, y)
            if self.y > y >= self.y - self.length and self.orientation == Orientation.down:
                return self._hit_battleship(x, y)
            return ResultCode.MISS
        if self.y == y:
            if self.x < x <= self.x + self.length and self.orientation == Orientation.right:
                return self._hit_battleship(x, y)
            if self.x > x >= self.x - self.length and self.orientation == Orientation.left:
                return self._hit_battleship(x, y)
            return ResultCode.MISS
        return ResultCode.MISS

    def _hit_battleship(self, x, y):
        """
        Add an hit to this battleship in the given coordinates
        :param x: int - the x coordinate
        :param y: int - the y coordinate
        :return: the appropriate result code
        """
        if (x, y) in self.hits:
            return ResultCode.MISS
        self.hits.append((x, y))
        if len(self.hits) == self.length:
            return ResultCode.HIT_FINAL
        return ResultCode.HIT
