from tqdm import tqdm as progress

from game import Board, Move
from constants import *

# https://www.chessprogramming.org/Point_Value_by_Regression_Analysis
INF = float("inf")

PIECE_VALUES = {
    PAWN: 100.0,
    KNIGHT: 288.0,
    BISHOP: 345.0,
    ROOK: 480.0,
    QUEEN: 1077.0,
    KING: INF,
}
SQUARE_VALUES = {
    PAWN:
        [0, 0, 0, 0, 0, 0, 0, 0,
         50, 50, 50, 50, 50, 50, 50, 50,
         10, 10, 20, 30, 30, 20, 10, 10,
         5, 5, 10, 25, 25, 10, 5, 5,
         0, 0, 0, 20, 20, 0, 0, 0,
         5, -5, -10, 0, 0, -10, -5, 5,
         5, 10, 10, -20, -20, 10, 10, 5,
         0, 0, 0, 0, 0, 0, 0, 0],
    KNIGHT:
        [-50, -40, -30, -30, -30, -30, -40, -50,
         -40, -20, 0, 5, 5, 0, -20, -40,
         -30, 5, 10, 15, 15, 10, 5, -30,
         -30, 0, 15, 20, 20, 15, 0, -30,
         -30, 5, 15, 20, 20, 15, 5, -30,
         -30, 0, 10, 15, 15, 10, 0, -30,
         -40, -20, 0, 0, 0, 0, -20, -40,
         -50, -40, -30, -30, -30, -30, -40, -50],
    BISHOP:
        [-20, -10, -10, -10, -10, -10, -10, -20,
         -10, 0, 0, 0, 0, 0, 0, -10,
         -10, 0, 5, 10, 10, 5, 0, -10,
         -10, 5, 5, 10, 10, 5, 5, -10,
         -10, 0, 10, 10, 10, 10, 0, -10,
         -10, 10, 10, 10, 10, 10, 10, -10,
         -10, 5, 0, 0, 0, 0, 5, -10,
         -20, -10, -10, -10, -10, -10, -10, -20],
    ROOK:
        [0, 0, 0, 0, 0, 0, 0, 0,
         5, 10, 10, 10, 10, 10, 10, 5,
         -5, 0, 0, 0, 0, 0, 0, -5,
         -5, 0, 0, 0, 0, 0, 0, -5,
         -5, 0, 0, 0, 0, 0, 0, -5,
         -5, 0, 0, 0, 0, 0, 0, -5,
         -5, 0, 0, 0, 0, 0, 0, -5,
         0, 0, 0, 5, 5, 0, 0, 0],
    QUEEN:
        [-20, -10, -10, -5, -5, -10, -10, -20,
         -10, 0, 0, 0, 0, 5, 0, -10,
         -10, 0, 5, 5, 5, 5, 5, -10,
         -5, 0, 5, 5, 5, 5, 0, 0,
         -5, 0, 5, 5, 5, 5, 0, -5,
         -10, 0, 5, 5, 5, 5, 0, -10,
         -10, 0, 0, 0, 0, 0, 0, -10,
         -20, -10, -10, -5, -5, -10, -10, -20],
    KING:
        [-30, -40, -40, -50, -50, -40, -40, -30,
         -30, -40, -40, -50, -50, -40, -40, -30,
         -30, -40, -40, -50, -50, -40, -40, -30,
         -30, -40, -40, -50, -50, -40, -40, -30,
         -20, -30, -30, -40, -40, -30, -30, 20,
         -10, -20, -20, -20, -20, -20, -20, -10,
         20, 20, 0, 0, 0, 0, 20, 20,
         20, 30, 10, 0, 0, 10, 30, 20],

}
MAX_DEPTH = 4


def heuristic_eval(board: Board) -> float:
    """
    Returns a static evaluation of the current position
    :param board: Board instance
    :return: evaluation
    """
    if (r := board.get_win_state()) != NO_RESULT:
        return r * PIECE_VALUES[KING]

    piece_sum = _sum_pieces(board)
    positional_sum = _sum_square_values(board)

    return (piece_sum + positional_sum) / 100


def _sum_pieces(board: Board) -> float:
    """
    Returns sum of white pieces - sum of black pieces
    :param board: Board instance
    :return: material difference
    """
    res = 0
    for square in board.position:
        if square.has_piece():
            if (t := square.piece.type) != KING:
                colour = square.piece.colour
                value = PIECE_VALUES[t]
                res += colour * value
    return res


def _sum_square_values(board: Board) -> float:
    """
    Returns the positional value of white - positional value of black
    :param board: Board instance
    :return: positional difference
    """
    res = 0
    for square in board.position:
        if square.has_piece():
            t = square.piece.type
            colour = square.piece.colour
            i = square.index if colour == WHITE else 63 - square.index
            value = SQUARE_VALUES[t][i]
            res += colour * value
    return res


SEARCHED_POSITIONS = 0


def minimax(board: Board, depth: int = MAX_DEPTH) -> tuple[Move | None, float]:
    global SEARCHED_POSITIONS

    moves = board.get_legal_moves()
    maximising = board.turn == WHITE

    if depth == 0 or len(moves) == 0:
        return None, heuristic_eval(board)

    best_move_eval_pair = None, -INF if maximising else INF
    func = max if maximising else min

    for move in progress(board.get_legal_moves(), disable=False):
        board.make_move(move)
        ev = _minimax(board, depth - 1, not maximising, -INF, INF)
        board.unmake_move()
        best_move_eval_pair = func(best_move_eval_pair, (move, ev), key=lambda x: x[1])
        SEARCHED_POSITIONS += 1

    return best_move_eval_pair


def _minimax(board: Board, depth: int, maximising: bool, alpha: float, beta: float) -> float:
    global SEARCHED_POSITIONS

    moves = board.get_legal_moves()

    if depth == 0 or len(moves) == 0:
        return heuristic_eval(board)

    if maximising:
        for move in moves:
            board.make_move(move)
            ev = _minimax(board, depth - 1, not maximising, alpha, beta)
            board.unmake_move()
            alpha = max(alpha, ev)
            if beta <= alpha: break
        SEARCHED_POSITIONS += 1
        return alpha
    else:
        for move in moves:
            board.make_move(move)
            ev = _minimax(board, depth - 1, not maximising, alpha, beta)
            board.unmake_move()
            beta = min(beta, ev)
            if beta <= alpha: break
        SEARCHED_POSITIONS += 1
        return beta


if __name__ == "__main__":
    b = Board()
    print(*minimax(b, 2))
    print(f"Searched {SEARCHED_POSITIONS} positions")
