import chess
import chess.svg
import time
import copy
from typing import Dict, List, Any, Callable
import random
from hab_movegeneration import next_move
from evaluate import piece_value
from IPython.display import SVG, display

piece_map = {1: 'Pawn', 2: 'Knight', 3: 'Bishop',
             4: 'Rook', 5: 'Queen', 6: 'King'}


def get_legal_pieces(board: chess.Board) -> List[chess.Piece]:
    return list(set([board.piece_at(x.from_square).piece_type for x in list(board.legal_moves)]))


def can_castle(board: chess.Board) -> bool:
    return list(board.generate_castling_moves())


def is_checkmate(board: chess.Board, move: chess.Move) -> bool:
    board_copy = copy.deepcopy(board)
    board_copy.push(move)
    return board_copy.is_checkmate()


def get_move_piece(board: chess.Board, move: chess.Move) -> chess.Piece:
    return board.piece_at(move.from_square)


def get_checkmate_piece(board: chess.Board) -> bool:
    for move in list(board.legal_moves):
        board_copy = copy.deepcopy(board)
        board_copy.push(move)
        if board_copy.is_checkmate():
            return get_move_piece(board, move).piece_type
    return None


def is_eat(board: chess.Board, move: chess.Move) -> bool:
    to_square = move.to_square
    return board.piece_at(to_square) is not None


def eat_value(board: chess.Board, move: chess.Move, piece_value_map: Dict[chess.Piece, int] = piece_value) -> int:
    to_square = move.to_square
    print("Piece at square is {} of type {}".format(board.piece_at(to_square), board.piece_at(to_square).__class__))
    if board.piece_at(to_square):
        return piece_value_map.get(board.piece_at(to_square).piece_type)
    else:
        return 0


def max_eat_value_move_piece(board: chess.Board) -> chess.Piece:
    moves = list(board.legal_moves)
    current_max_value = eat_value(board, moves[0])
    current_piece = board.piece_at(moves[0].from_square)
    for move in list(board.legal_moves):
        value = eat_value(board, move)
        if value > current_max_value:
           current_max_value = value
           current_piece = board.piece_at(move.from_square)
    return current_piece


def piece_to_string(piece_int: int) -> str:
    return piece_map[piece_int]


def bot_vs_bot(bot1_choose_piece: Callable, bot2_choose_piece: Callable, depth: int = 3, delay_seconds: float = 0.5, debug: bool = False) -> bool:
    # coin flip for which bot is white
    bot1_is_white = random.random() < 0.5
    if bot1_is_white:
        print('Bot 1 is White')
    else:
        print('Bot 1 is Black')

    board = chess.Board()

    print("Board is from Bot 1's perspective")

    if bot1_is_white:
        bot1_constraint = bot1_choose_piece(board)
        print(f'Bot 1 Chose {piece_to_string(bot1_constraint)}')
        board.push(next_move(depth, board, debug=debug,
                   piece_constraint=bot1_constraint))
        display(SVG(chess.svg.board(board, size=250, orientation=bot1_is_white)))
        time.sleep(delay_seconds)

    while not board.is_game_over():
        bot2_constraint = bot2_choose_piece(board)
        print(f'Bot 2 Chose {piece_to_string(bot2_constraint)}')
        board.push(next_move(depth, board,
                   debug=debug, piece_constraint=bot2_constraint))

        display(SVG(chess.svg.board(board, size=250, orientation=bot1_is_white)))
        time.sleep(delay_seconds)

        if board.is_game_over():
            break

        bot1_constraint = bot1_choose_piece(board)
        print(f'Bot 1 Chose {piece_to_string(bot1_constraint)}')
        board.push(next_move(depth, board, debug=debug,
                   piece_constraint=bot1_constraint))
        display(SVG(chess.svg.board(board, size=250, orientation=bot1_is_white)))
        time.sleep(delay_seconds)

    print(f"\nResult: [w] {board.result()} [b]")

    return True
