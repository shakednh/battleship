from abc import ABC
from contextlib import AbstractContextManager

from config.connector_conf import HOST_IP
from src.exceptions.connector_exception import ConnectorNotConnectedException
import socket
import logging

logger = logging.getLogger(__name__)


class IStream(ABC):
    def read(self):
        raise NotImplementedError()

    def write(self, data):
        raise NotImplementedError()


class TCPServerConnector(IStream):
    def __init__(self, port: int):
        self.port = port
        self.socket = None
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST_IP, self.port))
        self.socket.listen(1)
        self.conn, address = self.socket.accept()
        logger.info('Connected by %s', address)

    def disconnect(self):
        logger.info("Closing connection of socket: %s", self.socket)
        self.conn.close()
        self.conn = None
        self.socket.close()
        self.socket = None

    def read(self):
        return self.conn.recv(1024)

    def write(self, data):
        if not self.conn:
            raise ConnectorNotConnectedException()
        return self.conn.sendall(data)


class TCPClientConnector(IStream, AbstractContextManager):
    def __init__(self):
        self.socket = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        logger.info('Connected to %s:%s', (ip, port))

    def disconnect(self):
        logger.info("Closing connection of socket: %s", self.socket)
        self.socket.close()
        self.socket = None

    def read(self):
        return self.socket.recv(1024)

    def write(self, data):
        if not self.socket:
            raise ConnectorNotConnectedException()
        return self.socket.sendall(data)
