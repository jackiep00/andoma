from typing import Dict, List, Any
import chess
import sys
import time
from evaluate import evaluate_board, move_value, check_end_game

debug_info: Dict[str, Any] = {}


def next_move(depth: int, board: chess.Board, piece_constraint: int, debug=True) -> chess.Move:
    """
    What is the next best move?
    """
    debug_info.clear()
    debug_info["nodes"] = 0
    t0 = time.time()

    move = minimax_root(depth, board, piece_constraint)

    debug_info["time"] = time.time() - t0
    if debug == True:
        print(f">>> {debug_info}", file=sys.stderr)
    return move


def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    end_game = check_end_game(board)

    def orderer(move):
        return move_value(board, move, end_game)

    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)


def minimax_root(depth: int, board: chess.Board, piece_constraint: int) -> chess.Move:
    # White always wants to maximize (and black to minimize)
    # the board score according to evaluate_board()
    maximize = board.turn == chess.WHITE
    best_move = -float("inf")
    if not maximize:
        best_move = float("inf")

    moves = [move for move in
             get_ordered_moves(board) if board.piece_at(move.from_square).piece_type == piece_constraint]
    best_move_found = moves[0]

    for move in moves:
        board.push(move)
        # Checking if draw can be claimed at this level, because the threefold repetition check
        # can be expensive. This should help the bot avoid a draw if it's not favorable
        # https://python-chess.readthedocs.io/en/latest/core.html#chess.Board.can_claim_draw
        if board.can_claim_draw():
            value = 0.0
        else:
            value = minimax(depth - 1, board, -float("inf"),
                            float("inf"), not maximize)
        board.pop()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    board: chess.Board,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
) -> float:
    debug_info["nodes"] += 1

    if board.is_checkmate():
        # The previous move resulted in checkmate
        return -float("inf") if is_maximising_player else float("inf")
    # When the game is over and it's not a checkmate it's a draw
    # In this case, don't evaluate. Just return a neutral result: zero
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    if is_maximising_player:
        best_move = -float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            best_move = max(
                best_move,
                minimax(depth - 1, board, alpha, beta,
                        not is_maximising_player),
            )
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = float("inf")
        moves = get_ordered_moves(board)
        for move in moves:
            board.push(move)
            best_move = min(
                best_move,
                minimax(depth - 1, board, alpha, beta,
                        not is_maximising_player),
            )
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move
