import chess
from typing import Dict, List, Any


def get_legal_pieces(board: chess.Board) -> List[int]:
    list(set([board.piece_at(x.from_square).piece_type for x in list(board.legal_moves)]))
