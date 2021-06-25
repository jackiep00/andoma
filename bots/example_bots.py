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


def two_knights_opening(board: chess.Board) -> chess.Piece:
    # first two moves, move the knight
    if (board.fullmove_number <= 2):
        return chess.KNIGHT
    if (board.fullmove_number <= 4):
        return chess.PAWN


def count_attackers_and_defenders(board: chess.Board) -> chess.Piece:
    my_color = board.turn
    candidate_moves = []

    for move in list(board.legal_moves):
        num_attackers = len(board.attackers(my_color, move.to_square))
        num_defenders = len(board.attackers(not my_color, move.to_square))
        if num_attackers > num_defenders:
            candidate_moves.append(move)

    # if there are no candidate moves just return a piece from a random legal move
    if not candidate_moves:
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        return helpers.get_move_piece(board, legal_moves[0]).piece_type

    random.shuffle(candidate_moves)

    return helpers.get_move_piece(board, candidate_moves[0]).piece_type
