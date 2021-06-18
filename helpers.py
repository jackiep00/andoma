import chess
import copy
from typing import Dict, List, Any


def get_legal_pieces(board: chess.Board) -> List[chess.Piece]:
    return list(set([board.piece_at(x.from_square).piece_type for x in list(board.legal_moves)]))


def can_castle(board: chess.Board) -> bool:
    return list(board.generate_castling_moves())


def is_checkmate(board: chess.Board, move: chess.Move) -> bool:
    board_copy = copy.deepcopy(board)
    board_copy.push(move)
    return board_copy.is_checkmate()
