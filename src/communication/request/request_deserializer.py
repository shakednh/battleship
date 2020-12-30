import src.exceptions.battleship_exception as bship_exception

from config.request_deserializer_conf import message_type_to_class
from src.communication.request import RequestHeader


class RequestDeserializer:
    def __init__(self, request_header:RequestHeader):
        self.request_header = request_header

    def deserialize_request(self, data):
        # extract magic and message type
        magic_len = len(self.request_header.magic)
        header_len = magic_len + 1

        header = data[:header_len]
        request_data = data[header_len:]

        magic = header[:magic_len]
        message_type = header[magic_len]
        if self.request_header.magic != magic:
            raise bship_exception.InvalidMagicException

        request_cls = message_type_to_class.get(message_type)
        if not request_cls:
            raise bship_exception.InvalidMessageTypeException

        return request_cls.deserialize(self.request_header, request_data)
