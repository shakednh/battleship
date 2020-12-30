import logging

from config.request_conf import ResultCode
from src.communication.communication_manager import CommunicationManager
from src.user_handler.user_handler import UserHandler

logger = logging.getLogger(__name__)


class Game:
    """
    Responsible on the logic of a single Battleships game
    """

    def __init__(self, user_handler: UserHandler, communication_manager: CommunicationManager, is_starting: bool):
        self.user_handler = user_handler
        self.communication_manager = communication_manager
        self.is_starting = is_starting
        self.board = None
        self.is_end = False
        self.is_won = False

    def start_game(self):
        logger.info('Starting game')
        self.board = self.user_handler.get_board()
        self.communication_manager.finish_board_order()
        self.communication_manager.wait_enemy_board_order()

        self.is_end = False
        self.is_won = False
        while not self.is_end:
            self._game_round()
        logger.info('Game ended - is_won=%s', self.is_won)
        if self.is_won:
            self.user_handler.print_win()
        else:
            self.user_handler.print_lose()

    def _game_round(self):
        first, second = self.enemy_turn, self.do_turn
        if self.is_starting:
            first, second = second, first
        first()
        if self.is_end:
            return
        second()

    def do_turn(self):
        x, y = self.user_handler.get_guess()
        self.communication_manager.send_guess(x, y)
        result_code = self.communication_manager.get_result()
        if result_code == ResultCode.FINISH:
            self.is_won = True
            self.is_end = True
            return
        self.user_handler.print_result_code(result_code)

    def enemy_turn(self):
        x, y = self.communication_manager.get_guess()
        result_code = self.board.try_hit(x, y)
        self.communication_manager.send_result(result_code)
        if result_code == ResultCode.FINISH:
            self.is_won = False
            self.is_end = True
            return
        self.user_handler.print_enemy_guess_result(x, y, result_code)
