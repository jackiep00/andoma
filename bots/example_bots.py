import chess
import helpers
import random


def choose_piece_random(board: chess.Board) -> chess.Piece:
    legal_pieces = helpers.get_legal_pieces(board)
    random.shuffle(legal_pieces)

    return legal_pieces[0]


def choose_piece_in_order(board: chess.Board) -> chess.Piece:
    legal_pieces = helpers.get_legal_pieces(board)

    legal_pieces.sort()

    return legal_pieces[0]


def pure_offense(board: chess.Board) -> chess.Piece:
    checkmate_piece = helpers.get_checkmate_piece(board)
    if checkmate_piece:
        return checkmate_piece
    return helpers.max_eat_value_move_piece(board).piece_type
