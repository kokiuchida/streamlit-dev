"""
対局ページ - Play against AI
"""

import streamlit as st
import shogi
import datetime
import os
import sys
import io

# Add parent to path for shogi_engine imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shogi_engine.board_renderer import (
    render_board, pixel_to_square, shogi_sq_to_display, display_to_shogi_sq,
    BOARD_OFFSET_X, BOARD_OFFSET_Y, SQUARE_SIZE, STAND_W, IMG_W
)
from shogi_engine.ai_engine import get_best_move, DIFFICULTY_PARAMS, DIFFICULTY_TIME_LIMITS

try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    HAS_SIC = True
except ImportError:
    HAS_SIC = False

st.set_page_config(page_title="対局", layout="wide")
st.title("🎮 対局")

DIFFICULTIES = list(DIFFICULTY_PARAMS.keys())

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ── Piece stand click detection ──────────────────────────────────────────
STAND_PIECE_ORDER = [shogi.ROOK, shogi.BISHOP, shogi.GOLD, shogi.SILVER,
                     shogi.KNIGHT, shogi.LANCE, shogi.PAWN]

def pixel_in_stand(px, py, board, turn):
    """Return (piece_type, color) if click is on a piece in hand, else None."""
    # Black stand: right side
    if turn == shogi.BLACK:
        sx = BOARD_OFFSET_X + SQUARE_SIZE * 9 + 5
        sy = BOARD_OFFSET_Y
    else:
        # White stand: left side
        sx = 2
        sy = BOARD_OFFSET_Y

    if not (sx <= px <= sx + STAND_W - 5):
        return None

    pieces_in_hand = board.pieces_in_hand[turn]
    y_offset = sy + 30
    for pt in STAND_PIECE_ORDER:
        count = pieces_in_hand.get(pt, 0)
        if count == 0:
            continue
        if y_offset <= py <= y_offset + 34:
            return (pt, turn)
        y_offset += 36
    return None


# ── KIF helpers ──────────────────────────────────────────────────────────
PIECE_NAME_JA = {
    shogi.PAWN: "歩", shogi.LANCE: "香", shogi.KNIGHT: "桂",
    shogi.SILVER: "銀", shogi.GOLD: "金", shogi.BISHOP: "角",
    shogi.ROOK: "飛", shogi.KING: "玉",
    shogi.PROM_PAWN: "と", shogi.PROM_LANCE: "成香",
    shogi.PROM_KNIGHT: "成桂", shogi.PROM_SILVER: "成銀",
    shogi.PROM_BISHOP: "馬", shogi.PROM_ROOK: "龍",
}
FILE_NUM_JA = ["", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
RANK_JA = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九"]


def move_to_kif(board_before: shogi.Board, move: shogi.Move, move_num: int) -> str:
    """Format a move in KIF notation."""
    to_sq = move.to_square
    to_file = shogi.SQUARE_NAMES[to_sq][0]
    to_rank = ord(shogi.SQUARE_NAMES[to_sq][1]) - ord('a') + 1

    to_str = f"{to_file}{RANK_JA[to_rank]}"

    if move.from_square is None:
        # Drop
        pt = move.drop_piece_type
        piece_str = PIECE_NAME_JA.get(pt, "?")
        from_str = "打"
    else:
        from_sq = move.from_square
        from_file = shogi.SQUARE_NAMES[from_sq][0]
        from_rank = ord(shogi.SQUARE_NAMES[from_sq][1]) - ord('a') + 1
        piece = board_before.piece_at(from_sq)
        piece_str = PIECE_NAME_JA.get(piece.piece_type if piece else shogi.PAWN, "?")
        if move.promotion:
            piece_str += "成"
        from_str = f"({from_file}{from_rank})"

    return f"   {move_num:3d} {to_str}{piece_str}{from_str}"


def save_kif(game_log: list, difficulty: str, player_color: str):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d %H:%M:%S")
    file_str = now.strftime("%Y%m%d_%H%M%S")

    if player_color == "black":
        sente, gote = "あなた", f"AI（{difficulty}）"
    else:
        sente, gote = f"AI（{difficulty}）", "あなた"

    lines = [
        f"開始日時：{date_str}",
        "手合割：平手",
        f"先手：{sente}",
        f"後手：{gote}",
        "手数----指手---------消費時間--",
    ]
    lines.extend(game_log)
    lines.append(f"まで{len(game_log)}手で{'先手' if len(game_log) % 2 == 1 else '後手'}の勝ち")

    kif_text = "\n".join(lines)
    filename = os.path.join(LOG_DIR, f"game_{file_str}.kif")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(kif_text)
    return filename, kif_text


# ── Session state initialisation ────────────────────────────────────────
def init_game():
    st.session_state.board = shogi.Board()
    st.session_state.selected_sq = None        # board square index
    st.session_state.selected_drop = None      # (piece_type, color) from hand
    st.session_state.legal_sqs = []
    st.session_state.game_log = []
    st.session_state.move_count = 0
    st.session_state.last_move = None
    st.session_state.game_over = False
    st.session_state.status_msg = "あなたの番です（先手）。駒をクリックしてください。"
    st.session_state.kif_path = None
    st.session_state.kif_text = None


if "board" not in st.session_state:
    init_game()


# ── Sidebar controls ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 設定")
    difficulty = st.selectbox("難易度", DIFFICULTIES, index=4,
                              key="difficulty_select")
    player_color = st.radio("あなたの手番", ["先手（黒）", "後手（白）"],
                            key="player_color_radio")
    player_is_black = player_color == "先手（黒）"

    if st.button("🆕 新しい対局", use_container_width=True):
        init_game()
        st.rerun()

    st.markdown("---")
    st.markdown("**操作方法**")
    st.markdown("1. 動かしたい駒をクリック（黄色）\n2. 移動先をクリック（水色）\n3. 持ち駒は持ち駒エリアをクリック")


# ── Main layout ──────────────────────────────────────────────────────────
board: shogi.Board = st.session_state.board
game_over = st.session_state.game_over

col_board, col_info = st.columns([2, 1])

with col_board:
    # Render board
    img = render_board(
        board,
        selected_sq=st.session_state.selected_sq,
        legal_squares=st.session_state.legal_sqs,
        last_move=st.session_state.last_move,
        selected_drop=st.session_state.selected_drop,
    )

    if HAS_SIC and not game_over:
        coords = streamlit_image_coordinates(img, key="board_click")
    else:
        if not HAS_SIC:
            st.warning("streamlit-image-coordinates が未インストールです。`pip install streamlit-image-coordinates` でインストールしてください。")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=False)
        coords = None

    st.markdown(f"**{st.session_state.status_msg}**")

with col_info:
    st.subheader("対局情報")
    turn_str = "▲先手（黒）" if board.turn == shogi.BLACK else "△後手（白）"
    st.metric("手番", turn_str)
    st.metric("手数", st.session_state.move_count)
    st.metric("難易度", difficulty)

    st.subheader("持ち駒")
    PIECE_NAMES = {
        shogi.PAWN: "歩", shogi.LANCE: "香", shogi.KNIGHT: "桂",
        shogi.SILVER: "銀", shogi.GOLD: "金", shogi.BISHOP: "角", shogi.ROOK: "飛"
    }

    def hand_str(color):
        h = board.pieces_in_hand[color]
        parts = [f"{PIECE_NAMES[pt]}×{c}" for pt, c in h.items() if c > 0]
        return "　".join(parts) if parts else "なし"

    st.markdown(f"**▲先手:** {hand_str(shogi.BLACK)}")
    st.markdown(f"**△後手:** {hand_str(shogi.WHITE)}")

    if st.session_state.game_log:
        st.subheader("棋譜")
        log_text = "\n".join(st.session_state.game_log[-10:])
        st.code(log_text, language=None)

    if game_over and st.session_state.kif_text:
        st.subheader("KIF保存")
        st.download_button(
            "📥 棋譜をダウンロード",
            data=st.session_state.kif_text,
            file_name=os.path.basename(st.session_state.kif_path or "game.kif"),
            mime="text/plain",
        )


# ── Click handling ───────────────────────────────────────────────────────
def get_legal_destinations(board, from_sq):
    """Return list of destination squares for pieces on from_sq."""
    dests = []
    for mv in board.legal_moves:
        if mv.from_square == from_sq:
            dests.append(mv.to_square)
    return list(set(dests))


def get_drop_destinations(board, piece_type):
    """Return list of destination squares for dropping piece_type."""
    dests = []
    for mv in board.legal_moves:
        if mv.from_square is None and mv.drop_piece_type == piece_type:
            dests.append(mv.to_square)
    return list(set(dests))


def handle_click(px, py):
    """Process a board click at pixel (px, py)."""
    board = st.session_state.board
    if st.session_state.game_over:
        return

    current_turn = board.turn
    human_turn = (current_turn == shogi.BLACK) == player_is_black
    if not human_turn:
        return

    stand_hit = pixel_in_stand(px, py, board, current_turn)
    board_hit  = pixel_to_square(px, py)

    # ── State: drop piece selected (持ち駒選択中) ──────────────────────────
    if st.session_state.selected_drop is not None:
        pt, color = st.session_state.selected_drop

        if board_hit is not None:
            file_0, rank_0 = board_hit
            dest_sq = display_to_shogi_sq(file_0, rank_0)
            drop_move = shogi.Move(None, dest_sq, False, pt)
            if drop_move in board.legal_moves:
                execute_move(drop_move)
            # Invalid drop destination → keep selection, do nothing
            return

        if stand_hit:
            # Switch to another hand piece (or deselect same)
            if stand_hit != st.session_state.selected_drop:
                new_pt, _ = stand_hit
                st.session_state.selected_drop = stand_hit
                st.session_state.selected_sq   = None
                st.session_state.legal_sqs     = get_drop_destinations(board, new_pt)
            else:
                st.session_state.selected_drop = None
                st.session_state.legal_sqs     = []
            return

        # Clicked outside board and outside stand → keep selection
        return

    # ── State: board piece selected (盤上の駒選択中) ──────────────────────
    if st.session_state.selected_sq is not None:
        sel_sq = st.session_state.selected_sq

        if board_hit is not None:
            file_0, rank_0 = board_hit
            dest_sq = display_to_shogi_sq(file_0, rank_0)

            # Clicked another own piece → re-select
            piece = board.piece_at(dest_sq)
            if piece is not None and piece.color == current_turn and dest_sq != sel_sq:
                st.session_state.selected_sq   = dest_sq
                st.session_state.selected_drop = None
                st.session_state.legal_sqs     = get_legal_destinations(board, dest_sq)
                return

            # Try to move to destination
            matching = [mv for mv in board.legal_moves
                        if mv.from_square == sel_sq and mv.to_square == dest_sq]
            if matching:
                promo_moves = [mv for mv in matching if mv.promotion]
                execute_move(promo_moves[0] if promo_moves else matching[0])
                return

            # Deselect if clicked same square again
            if dest_sq == sel_sq:
                st.session_state.selected_sq   = None
                st.session_state.legal_sqs     = []
            # Invalid destination → keep selection, do nothing
            return

        if stand_hit:
            # Switch to hand piece selection
            new_pt, _ = stand_hit
            st.session_state.selected_drop = stand_hit
            st.session_state.selected_sq   = None
            st.session_state.legal_sqs     = get_drop_destinations(board, new_pt)
            return

        # Clicked outside board and outside stand → keep selection
        return

    # ── No selection yet ──────────────────────────────────────────────────
    if stand_hit:
        pt, color = stand_hit
        st.session_state.selected_drop = stand_hit
        st.session_state.selected_sq   = None
        st.session_state.legal_sqs     = get_drop_destinations(board, pt)
        return

    if board_hit is not None:
        file_0, rank_0 = board_hit
        sq = display_to_shogi_sq(file_0, rank_0)
        piece = board.piece_at(sq)
        if piece is not None and piece.color == current_turn:
            st.session_state.selected_sq   = sq
            st.session_state.selected_drop = None
            st.session_state.legal_sqs     = get_legal_destinations(board, sq)


def execute_move(move: shogi.Move):
    board = st.session_state.board
    mc = st.session_state.move_count + 1
    kif_line = move_to_kif(board, move, mc)
    board.push(move)
    st.session_state.move_count = mc
    st.session_state.last_move = move
    st.session_state.game_log.append(kif_line)
    st.session_state.selected_sq = None
    st.session_state.selected_drop = None
    st.session_state.legal_sqs = []

    if board.is_game_over():
        end_game()
        return

    st.session_state.status_msg = "AIが考えています..."
    # Trigger AI on next rerun via flag
    st.session_state.ai_should_move = True


def ai_move():
    board = st.session_state.board
    if board.is_game_over():
        end_game()
        return
    diff = st.session_state.difficulty_select
    time_limit = DIFFICULTY_TIME_LIMITS.get(diff, 3.0)
    ai_mv = get_best_move(board, diff, time_limit=time_limit)
    if ai_mv is None:
        end_game()
        return
    mc = st.session_state.move_count + 1
    kif_line = move_to_kif(board, ai_mv, mc)
    board.push(ai_mv)
    st.session_state.move_count = mc
    st.session_state.last_move = ai_mv
    st.session_state.game_log.append(kif_line)

    if board.is_game_over():
        end_game()
        return

    turn_str = "あなたの番です（先手）。" if board.turn == shogi.BLACK else "あなたの番です（後手）。"
    st.session_state.status_msg = turn_str + "駒をクリックしてください。"
    st.session_state.ai_should_move = False


def end_game():
    board = st.session_state.board
    st.session_state.game_over = True
    st.session_state.ai_should_move = False
    winner = "後手" if board.turn == shogi.BLACK else "先手"
    st.session_state.status_msg = f"対局終了！ {winner}の勝ちです。"
    path, text = save_kif(
        st.session_state.game_log,
        st.session_state.difficulty_select,
        "black" if player_is_black else "white"
    )
    st.session_state.kif_path = path
    st.session_state.kif_text = text


# ── Process click ─────────────────────────────────────────────────────────
if coords and not game_over:
    handle_click(coords["x"], coords["y"])
    st.rerun()

# ── AI move trigger ────────────────────────────────────────────────────────
if st.session_state.get("ai_should_move", False) and not game_over:
    ai_move()
    st.rerun()

# ── If it's AI's turn from the start (player chose white) ─────────────────
if not game_over and not st.session_state.get("ai_should_move", False):
    human_turn = (board.turn == shogi.BLACK) == player_is_black
    if not human_turn and st.session_state.move_count == 0:
        # AI moves first
        st.session_state.ai_should_move = True
        st.rerun()
