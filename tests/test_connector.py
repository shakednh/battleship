from config import connector_conf
from src.communication.connector.connector import TCPServerConnector, TCPClientConnector
import threading


def test_client_and_server_connection():
    message = 'hello world!'.encode()

    # run server
    server = TCPServerConnector(connector_conf.PROTOCOL_PORT)
    threading.Thread(target=run_server_connector, args=(server, message)).start()

    # run client
    client = TCPClientConnector()
    client.connect(connector_conf.HOST_IP, connector_conf.PROTOCOL_PORT)

    client.write(message)


def run_server_connector(server: TCPServerConnector, message: bytes):
    server.connect()
    message_received = server.read()
    assert message_received == message
