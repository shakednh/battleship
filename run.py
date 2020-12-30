from config import request_conf
from config import connector_conf
from src.communication.request.request import RequestHeader
from src.communication.request.request_deserializer import RequestDeserializer
from src.flow.flow_manager import FlowManager
from src.user_handler.user_handler import UserHandler


def main():
    user_handler = UserHandler()
    request_header = RequestHeader(magic=request_conf.MAGIC)
    request_deserializer = RequestDeserializer(request_header)
    flow_manager = FlowManager(user_handler=user_handler, request_header=request_header,
                               request_deserializer=request_deserializer, port=connector_conf.PROTOCOL_PORT)
    flow_manager.start()


if __name__ == '__main__':
    main()
