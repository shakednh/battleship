import struct
from abc import ABC

from config.request_conf import MessageType


class RequestHeader:
    def __init__(self, magic=''):
        self.magic = magic.encode()

    def get_header(self, message_type):
        return self.magic + struct.pack('B', message_type.value)


class IRequest(ABC):
    def serialize(self):
        raise NotImplementedError()

    @staticmethod
    def deserialize(request_header, data):
        raise NotImplementedError()


class GameRequest(IRequest):
    def __init__(self, request_header: RequestHeader):
        self.request_header = request_header

    def serialize(self):
        return self.request_header.get_header(MessageType.GAME_REQUEST)

    @staticmethod
    def deserialize(request_header, data):
        return GameRequest(request_header)


class GameReplyRequest(IRequest):
    def __init__(self, request_header: RequestHeader, is_accept: bool):
        self.request_header = request_header
        self.is_accept = is_accept

    def serialize(self):
        header = self.request_header.get_header(MessageType.GAME_REPLY)
        return header + struct.pack('B', self.is_accept)

    @staticmethod
    def deserialize(request_header, data):
        is_accept = bool(data[0])
        return GameReplyRequest(request_header, is_accept)


class OrderRequest(IRequest):
    def __init__(self, request_header: RequestHeader):
        self.request_header = request_header

    def serialize(self):
        return self.request_header.get_header(MessageType.ORDER)

    @staticmethod
    def deserialize(request_header, data):
        return OrderRequest(request_header)


class GuessRequest(IRequest):
    def __init__(self, request_header: RequestHeader, x: int, y: int):
        self.request_header = request_header
        self.x = x
        self.y = y

    def serialize(self):
        coordinates_byte = 0xf * self.x + self.y
        header = self.request_header.get_header(MessageType.GUESS)
        return header + struct.pack('B', coordinates_byte)

    @staticmethod
    def deserialize(request_header, data):
        coordinates_byte = int(data[0])
        x = coordinates_byte // 0xf
        y = coordinates_byte % 0xf
        return GuessRequest(request_header, x, y)


class ResultRequest(IRequest):
    def __init__(self, request_header: RequestHeader, result_code):
        self.request_header = request_header
        self.result_code = result_code

    def serialize(self):
        header = self.request_header.get_header(MessageType.RESULT)
        return header + struct.pack('B', self.result_code.value)

    @staticmethod
    def deserialize(request_header, data):
        result_code = int(data[0])
        return ResultRequest(request_header, result_code)


class ErrorRequest(IRequest):
    def __init__(self, request_header: RequestHeader, error_code):
        self.request_header = request_header
        self.error_code = error_code

    def serialize(self):
        header = self.request_header.get_header(MessageType.ERROR)
        return header + struct.pack('B', self.error_code.value)

    @staticmethod
    def deserialize(request_header, data):
        error_code = int(data[1])
        return ResultRequest(request_header, error_code)
