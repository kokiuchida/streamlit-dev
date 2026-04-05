"""
Shogi AI Engine using minimax with alpha-beta pruning.

Difficulty levels and their parameters:
  1級: depth 1 + 40% random moves
  初段: depth 2 + 20% random
  二段〜三段: depth 2
  四段〜五段: depth 3
  六段〜七段: depth 4
  八段〜九段: depth 5
  棋士: depth 6
"""

import shogi
import random
import time

# Material values for each piece type
MATERIAL_VALUES = {
    shogi.PAWN:             100,
    shogi.LANCE:            400,
    shogi.KNIGHT:           450,
    shogi.SILVER:           640,
    shogi.GOLD:             690,
    shogi.BISHOP:           890,
    shogi.ROOK:            1040,
    shogi.KING:           10000,
    shogi.PROM_PAWN:    300,
    shogi.PROM_LANCE:   500,
    shogi.PROM_KNIGHT:  530,
    shogi.PROM_SILVER:  680,
    shogi.PROM_BISHOP: 1150,
    shogi.PROM_ROOK:   1300,
}

DIFFICULTY_PARAMS = {
    "1級":  {"depth": 1, "random_rate": 0.40},
    "初段":  {"depth": 2, "random_rate": 0.20},
    "二段":  {"depth": 2, "random_rate": 0.00},
    "三段":  {"depth": 2, "random_rate": 0.00},
    "四段":  {"depth": 3, "random_rate": 0.00},
    "五段":  {"depth": 3, "random_rate": 0.00},
    "六段":  {"depth": 4, "random_rate": 0.00},
    "七段":  {"depth": 4, "random_rate": 0.00},
    "八段":  {"depth": 5, "random_rate": 0.00},
    "九段":  {"depth": 5, "random_rate": 0.00},
    "棋士":  {"depth": 6, "random_rate": 0.00},
}

# Time limits per difficulty (seconds)
DIFFICULTY_TIME_LIMITS = {
    "1級":  1.0,
    "初段":  1.0,
    "二段":  1.5,
    "三段":  2.0,
    "四段":  2.5,
    "五段":  3.0,
    "六段":  4.0,
    "七段":  5.0,
    "八段":  7.0,
    "九段":  8.0,
    "棋士": 10.0,
}


def _material_score(board: shogi.Board) -> int:
    """Compute material balance from BLACK's perspective."""
    score = 0
    for sq in range(81):
        piece = board.piece_at(sq)
        if piece is None:
            continue
        val = MATERIAL_VALUES.get(piece.piece_type, 0)
        if piece.color == shogi.BLACK:
            score += val
        else:
            score -= val
    # Pieces in hand
    for pt, val in MATERIAL_VALUES.items():
        if pt == shogi.KING:
            continue
        score += board.pieces_in_hand[shogi.BLACK].get(pt, 0) * val
        score -= board.pieces_in_hand[shogi.WHITE].get(pt, 0) * val
    return score


def _mobility_score(board: shogi.Board) -> int:
    """Number of legal moves difference as a proxy for mobility."""
    current_turn = board.turn
    black_mob = 0
    white_mob = 0
    # Count for current player
    mob_current = len(list(board.legal_moves))
    if current_turn == shogi.BLACK:
        black_mob = mob_current
    else:
        white_mob = mob_current
    return (black_mob - white_mob) * 5


def _king_safety(board: shogi.Board) -> int:
    """Bonus for having pieces near own king."""
    score = 0
    # Find king positions
    black_king_sq = None
    white_king_sq = None
    for sq in range(81):
        piece = board.piece_at(sq)
        if piece and piece.piece_type == shogi.KING:
            if piece.color == shogi.BLACK:
                black_king_sq = sq
            else:
                white_king_sq = sq

    # Reward gold/silver near king
    def _proximity_bonus(king_sq, color):
        if king_sq is None:
            return 0
        bonus = 0
        kr = king_sq // 9
        kf = king_sq % 9
        for sq in range(81):
            piece = board.piece_at(sq)
            if piece is None or piece.color != color:
                continue
            if piece.piece_type in (shogi.GOLD, shogi.SILVER, shogi.PROM_SILVER):
                r = sq // 9
                f = sq % 9
                dist = abs(r - kr) + abs(f - kf)
                if dist <= 2:
                    bonus += 30
        return bonus

    score += _proximity_bonus(black_king_sq, shogi.BLACK)
    score -= _proximity_bonus(white_king_sq, shogi.WHITE)
    return score


def evaluate(board: shogi.Board) -> int:
    """
    Full position evaluation from BLACK's perspective.
    Higher = better for BLACK.
    """
    if board.is_game_over():
        # The side whose turn it is has lost (or drawn)
        winner = board.turn  # the player to move is in checkmate
        if winner == shogi.BLACK:
            return -50000
        else:
            return 50000

    score = _material_score(board)
    score += _king_safety(board)
    return score


def _alpha_beta(board: shogi.Board, depth: int, alpha: int, beta: int,
                maximizing: bool, deadline: float) -> int:
    """Alpha-beta pruning minimax search."""
    if time.time() > deadline:
        return evaluate(board)

    if depth == 0 or board.is_game_over():
        return evaluate(board)

    moves = list(board.legal_moves)
    if not moves:
        return evaluate(board)

    # Move ordering: captures first
    def move_priority(m):
        if board.piece_at(m.to_square) is not None:
            return -1
        return 0

    moves.sort(key=move_priority)

    if maximizing:  # BLACK's turn
        value = -999999
        for move in moves:
            board.push(move)
            value = max(value, _alpha_beta(board, depth - 1, alpha, beta, False, deadline))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:  # WHITE's turn
        value = 999999
        for move in moves:
            board.push(move)
            value = min(value, _alpha_beta(board, depth - 1, alpha, beta, True, deadline))
            board.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def get_best_move(board: shogi.Board, difficulty: str,
                  time_limit: float = 5.0) -> shogi.Move:
    """
    Return the best move for the current player given difficulty.
    """
    params = DIFFICULTY_PARAMS.get(difficulty, DIFFICULTY_PARAMS["初段"])
    depth = params["depth"]
    random_rate = params["random_rate"]

    moves = list(board.legal_moves)
    if not moves:
        return None

    # Random move for lower difficulties
    if random.random() < random_rate:
        return random.choice(moves)

    deadline = time.time() + time_limit
    maximizing_is_black = (board.turn == shogi.BLACK)

    best_move = None
    best_val = -999999 if maximizing_is_black else 999999

    # Shuffle for variety
    random.shuffle(moves)

    for move in moves:
        if time.time() > deadline:
            break
        board.push(move)
        val = _alpha_beta(board, depth - 1, -999999, 999999,
                          not maximizing_is_black, deadline)
        board.pop()
        if maximizing_is_black:
            if val > best_val:
                best_val = val
                best_move = move
        else:
            if val < best_val:
                best_val = val
                best_move = move

    return best_move if best_move is not None else moves[0]


def get_move_evaluation(board: shogi.Board, move: shogi.Move,
                        depth: int = 3) -> int:
    """Return evaluation score after making a move (for analysis)."""
    board.push(move)
    score = evaluate(board)
    board.pop()
    return score


def analyze_game(moves_usi: list) -> list:
    """
    Analyze a complete game given as list of USI move strings.
    Returns list of dicts with keys: move_num, move, score, best_move, best_score, comment
    """
    board = shogi.Board()
    analysis = []
    prev_score = evaluate(board)

    for i, move_usi in enumerate(moves_usi):
        try:
            move = shogi.Move.from_usi(move_usi)
        except Exception:
            continue

        # Find best move at depth 3
        best = get_best_move(board, "三段", time_limit=2.0)
        best_score = get_move_evaluation(board, best, depth=3) if best else prev_score

        # Score after actual move
        actual_score = get_move_evaluation(board, move, depth=3)

        # Determine quality
        score_diff = abs(actual_score - best_score)
        if score_diff < 50:
            comment = "好手"
        elif score_diff < 200:
            comment = "普通"
        elif score_diff < 500:
            comment = "疑問手"
        else:
            comment = "悪手"

        analysis.append({
            "move_num": i + 1,
            "move_usi": move_usi,
            "score": actual_score,
            "best_move_usi": best.usi() if best else move_usi,
            "best_score": best_score,
            "score_diff": score_diff,
            "comment": comment,
        })

        board.push(move)
        prev_score = actual_score

    return analysis
