import logging

from src.request.request import RequestHeader, OrderRequest, GuessRequest, ResultRequest
from src.connector.connector import IStream
from src.request.request_deserializer import RequestDeserializer

logger = logging.getLogger(__name__)


class CommunicationManager:
    def __init__(self, connector: IStream, request_header: RequestHeader, request_deserializer: RequestDeserializer):
        self.connector = connector
        self.request_header = request_header
        self.request_deserializer = request_deserializer

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
        if type(request) is not OrderRequest:
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
        return request.result_code
