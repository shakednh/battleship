import logging

from config.request_conf import ResultCode
from src.communication.request.request import RequestHeader, OrderRequest, GuessRequest, ResultRequest, GameRequest, \
    GameReplyRequest
from src.communication.connector.connector import IStream
from src.communication.request.request_deserializer import RequestDeserializer

logger = logging.getLogger(__name__)


class CommunicationManager:
    def __init__(self, connector: IStream, request_header: RequestHeader, request_deserializer: RequestDeserializer):
        self.connector = connector
        self.request_header = request_header
        self.request_deserializer = request_deserializer

    def send_game_request(self):
        logging.info('Sending game request')
        return self.connector.write(GameRequest(self.request_header).serialize())

    def get_game_request(self):
        request_data = self.connector.read()
        request = self.request_deserializer.deserialize_request(request_data)
        if type(request) is not GameRequest:
            raise TypeError(f'Should have got an GameRequest instead got: {type(request)}')
        logger.info('Got a game request from %s', self.connector)

    def send_game_reply(self, is_accept):
        logging.info('Sending game reply')
        return self.connector.write(GameReplyRequest(self.request_header, is_accept).serialize())

    def get_game_reply(self):
        request_data = self.connector.read()
        request = self.request_deserializer.deserialize_request(request_data)
        if type(request) is not GameReplyRequest:
            raise TypeError(f'Should have got an GameReplyRequest instead got: {type(request)}')
        logger.info('Got a game reply with value %s from %s', (request.is_accept, self.connector))
        return request.is_accept

    def finish_board_order(self):
        logging.info('Finished board ordering')
        return self.connector.write(OrderRequest(self.request_header).serialize())

    def wait_enemy_board_order(self):
        request_data = self.connector.read()
        request = self.request_deserializer.deserialize_request(request_data)
        if type(request) is not OrderRequest:
            raise TypeError(f'Should have got an OrderRequest instead got: {type(request)}')
        logger.info('Enemy finished board ordering')

    def send_guess(self, x, y):
        logger.info('Sending guess - %s', ((x, y),))
        request = GuessRequest(self.request_header, x, y)
        return self.connector.write(request.serialize())

    def get_guess(self):
        request_data = self.connector.read()
        request = self.request_deserializer.deserialize_request(request_data)
        if type(request) is not GuessRequest:
            raise TypeError(f'Should have got an GuessRequest instead got: {type(request)}')
        return request.x, request.y

    def send_result(self, result_code):
        request = ResultRequest(self.request_header, result_code)
        return self.connector.write(request.serialize())

    def get_result(self):
        request_data = self.connector.read()
        request = self.request_deserializer.deserialize_request(request_data)
        if type(request) is not ResultRequest:
            raise TypeError(f'Should have got an ResultRequest instead got: {type(request)}')
        return ResultCode(request.result_code)
