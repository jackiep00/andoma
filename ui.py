# inspired by the https://github.com/thomasahle/sunfish user inferface

import chess
import argparse
import chess.svg
from IPython.display import SVG, display
from hab_movegeneration import next_move
from helpers import piece_to_string, get_legal_pieces
from typing import Callable

piece_mapping = {
    'p': 1, 'n': 2, 'b': 3, 'r': 4, 'q': 5, 'k': 6, 'pawn': 1, 'knight': 2, 'bishop': 3, 'rook': 4, 'queen': 5, 'king': 6
}


def get_constraint(board: chess.Board) -> chess.Piece:
    """
    Try (and keep trying) to get a legal bot constraint from the user.
    """
    # in the case where this is a human looking at what move they should do next
    # show them the board to give them a chance
    display(SVG(chess.svg.board(board, size=275, orientation=board.turn)))

    move = input(
        f"\nThe constraint for the bot (Options: {list(set([piece_to_string(x) for x in get_legal_pieces(board)]))}:\n")

    for legal_piece in get_legal_pieces(board):
        if piece_mapping.setdefault(move.lower(), None) == legal_piece:
            return legal_piece

    print('Invalid piece choice')
    return get_constraint(board)


def start(choose_piece: Callable = get_constraint):
    """
    Start the command line user interface.
    """
    board = chess.Board()
    user_side = (
        chess.WHITE if input(
            "Start as [w]hite or [b]lack:\n") == "w" else chess.BLACK
    )

    if user_side == chess.WHITE:
        # print(render(board))
        # chess.svg.board(board, size=300)
        display(SVG(chess.svg.board(board, size=275, orientation=user_side)))

        board.push(get_move(board))

    while not board.is_game_over():
        constraint = choose_piece(board)
        print(f'Bot Chose {piece_to_string(constraint)}')
        board.push(next_move(get_depth(), board,
                   debug=False, piece_constraint=constraint))
        # print(render(board))
        # chess.svg.board(board, size=350)
        display(SVG(chess.svg.board(board, size=275, orientation=user_side)))

        board.push(get_move(board))

    print(f"\nResult: [w] {board.result()} [b]")


def get_move(board: chess.Board) -> chess.Move:
    """
    Try (and keep trying) to get a legal next move from the user.
    Play the move by mutating the game board.
    """
    move = input(f"\nYour move (e.g. {list(board.legal_moves)[0]}):\n")

    for legal_move in board.legal_moves:
        if move == str(legal_move):
            return legal_move

    print('Invalid move')
    return get_move(board)


def get_depth() -> int:
    return 3
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--depth", default=3, help="provide an integer (default: 3)")
    # args = parser.parse_args()
    # return max([1, int(args.depth)])


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        pass
