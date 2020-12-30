from config.request_conf import MessageType
from src.communication.request.request import GameRequest, GameReplyRequest, OrderRequest, GuessRequest, ErrorRequest, \
    ResultRequest

message_type_to_class = {
    MessageType.GAME_REQUEST: GameRequest,
    MessageType.GAME_REPLY: GameReplyRequest,
    MessageType.ORDER: OrderRequest,
    MessageType.GUESS: GuessRequest,
    MessageType.RESULT: ResultRequest,
    MessageType.ERROR: ErrorRequest,
}
