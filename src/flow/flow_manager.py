from config.user_handler_conf import ActionType
from src.communication.communication_manager import CommunicationManager
from src.communication.connector.connector import TCPServerConnector, TCPClientConnector
from src.communication.request.request import RequestHeader
from src.communication.request.request_deserializer import RequestDeserializer
from src.game.game import Game
from src.user_handler.user_handler import UserHandler


class FlowManager:
    def __init__(self, user_handler: UserHandler, request_header: RequestHeader,
                 request_deserializer: RequestDeserializer, port: int):
        self.user_handler = user_handler
        self.request_header = request_header
        self.request_deserializer = request_deserializer
        self.port = port

    def start(self):
        action = self.user_handler.get_wanted_action()
        action_to_flow = {
            ActionType.WAIT: self.wait_for_connection,
            ActionType.CONNECT: self.connect,
        }
        action_to_flow[action]()

    def wait_for_connection(self):
        with TCPServerConnector(self.port) as connector:
            comm_manager = CommunicationManager(connector, self.request_header, self.request_deserializer)
            comm_manager.get_game_request()
            comm_manager.send_game_reply(is_accept=True)

            game = Game(self.user_handler, comm_manager, is_starting=False)
            game.start_game()

    def connect(self):
        connector = TCPClientConnector()
        ip = self.user_handler.get_ip()
        connector.connect(ip, self.port)
        with connector:
            comm_manager = CommunicationManager(connector, self.request_header, self.request_deserializer)
            comm_manager.send_game_request()
            is_accept = comm_manager.get_game_reply()
            if not is_accept:
                return

            game = Game(self.user_handler, comm_manager, is_starting=True)
            game.start_game()
