import chess
import helpers
import random


def choose_piece(board: chess.Board) -> chess.Piece:
    legal_pieces = helpers.get_legal_pieces(board)
    random.shuffle(legal_pieces)[0]
