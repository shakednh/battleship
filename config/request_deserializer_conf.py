from config.package_packer import MessageType
from src.request.request import GameRequest, GameReplyRequest, OrderRequest, GuessRequest, ErrorRequest

message_type_to_class = {
    MessageType.GAME_REQUEST: GameRequest,
    MessageType.GAME_REPLY: GameReplyRequest,
    MessageType.ORDER: OrderRequest,
    MessageType.GUESS: GuessRequest,
    MessageType.ERROR: ErrorRequest,
}
