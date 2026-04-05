"""
次の一手ページ - Next-move problems
"""

import streamlit as st
import shogi
import json
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shogi_engine.board_renderer import (
    render_board, pixel_to_square, display_to_shogi_sq
)

try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    HAS_SIC = True
except ImportError:
    HAS_SIC = False

st.set_page_config(page_title="次の一手", layout="wide")
st.title("🧩 次の一手")

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "problems.json"
)

@st.cache_data
def load_problems():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

all_problems = load_problems()

# ── Session state ─────────────────────────────────────────────────────────
def init_problems():
    st.session_state.prob_index = 0
    st.session_state.prob_answered = False
    st.session_state.prob_correct = None
    st.session_state.prob_sel_sq = None
    st.session_state.prob_legal_sqs = []
    st.session_state.prob_score = 0
    st.session_state.prob_total = 0
    st.session_state.prob_filter = "すべて"
    st.session_state.prob_ids = list(range(len(all_problems)))


if "prob_index" not in st.session_state:
    init_problems()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ フィルター")
    difficulty_opts = ["すべて"] + sorted(
        list(set(p["difficulty"] for p in all_problems)),
        key=lambda x: ["1級","初段","二段","三段","四段","五段"].index(x)
        if x in ["1級","初段","二段","三段","四段","五段"] else 99
    )
    diff_filter = st.selectbox("難易度", difficulty_opts,
                               key="prob_diff_filter")

    category_opts = ["すべて"] + sorted(
        list(set(p["category"] for p in all_problems))
    )
    cat_filter = st.selectbox("カテゴリ", category_opts,
                              key="prob_cat_filter")

    if st.button("🔄 フィルター適用", use_container_width=True):
        filtered = [
            i for i, p in enumerate(all_problems)
            if (diff_filter == "すべて" or p["difficulty"] == diff_filter)
            and (cat_filter == "すべて" or p["category"] == cat_filter)
        ]
        st.session_state.prob_ids = filtered
        st.session_state.prob_index = 0
        st.session_state.prob_answered = False
        st.session_state.prob_sel_sq = None
        st.session_state.prob_legal_sqs = []
        st.rerun()

    st.markdown("---")
    st.metric("スコア", f"{st.session_state.prob_score} / {st.session_state.prob_total}")

    if st.button("🆕 スコアリセット"):
        st.session_state.prob_score = 0
        st.session_state.prob_total = 0
        st.rerun()


# ── Get current problem ───────────────────────────────────────────────────
prob_ids = st.session_state.prob_ids
if not prob_ids:
    st.warning("条件に合う問題がありません。フィルターを変更してください。")
    st.stop()

idx = min(st.session_state.prob_index, len(prob_ids) - 1)
prob = all_problems[prob_ids[idx]]

# Load board
@st.cache_data
def load_board_from_sfen(sfen: str):
    try:
        board = shogi.Board(sfen)
        return board
    except Exception as e:
        return None

board = load_board_from_sfen(prob["sfen"])
if board is None:
    # Try starting position
    board = shogi.Board()
    st.warning(f"SFEN読み込みエラー: {prob['sfen']}")

correct_move_usi = prob["correct_move"]
try:
    correct_move = shogi.Move.from_usi(correct_move_usi)
except Exception:
    correct_move = None

# ── Problem header ────────────────────────────────────────────────────────
col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
with col_h1:
    st.subheader(f"問題 {prob['id']} / 300: {prob['description']}")
with col_h2:
    st.metric("難易度", prob["difficulty"])
with col_h3:
    st.metric("カテゴリ", prob["category"])

st.markdown("---")

# ── Board display ─────────────────────────────────────────────────────────
col_board, col_info = st.columns([2, 1])

answered = st.session_state.prob_answered
sel_sq = st.session_state.prob_sel_sq
legal_sqs = st.session_state.prob_legal_sqs

highlight_move = correct_move if answered else None

img = render_board(
    board,
    selected_sq=sel_sq,
    legal_squares=legal_sqs,
    last_move=highlight_move,
)

with col_board:
    if HAS_SIC and not answered:
        coords = streamlit_image_coordinates(img, key=f"prob_board_{prob['id']}_{idx}")
    else:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=False)
        if not HAS_SIC:
            st.warning("streamlit-image-coordinates が未インストールです。")
        coords = None

with col_info:
    st.subheader("問題情報")
    turn_str = "▲先手番" if board.turn == shogi.BLACK else "△後手番"
    st.info(f"手番: {turn_str}")

    if answered:
        if st.session_state.prob_correct:
            st.success("🎉 正解！")
        else:
            st.error("❌ 不正解")
        st.markdown(f"**正解手:** `{correct_move_usi}`")
        st.markdown(f"**解説:** {prob['explanation']}")

    st.markdown("---")
    # Navigation
    col_p, col_n = st.columns(2)
    with col_p:
        if st.button("⬅️ 前の問題", use_container_width=True,
                     disabled=(idx == 0)):
            st.session_state.prob_index = max(0, idx - 1)
            st.session_state.prob_answered = False
            st.session_state.prob_sel_sq = None
            st.session_state.prob_legal_sqs = []
            st.rerun()
    with col_n:
        if st.button("次の問題 ➡️", use_container_width=True,
                     disabled=(idx >= len(prob_ids) - 1)):
            st.session_state.prob_index = min(len(prob_ids) - 1, idx + 1)
            st.session_state.prob_answered = False
            st.session_state.prob_sel_sq = None
            st.session_state.prob_legal_sqs = []
            st.rerun()

    if not answered:
        if st.button("💡 ヒントを見る"):
            st.info(f"正解手: `{correct_move_usi}`")
    else:
        if st.button("▶️ 次の問題へ"):
            next_idx = min(len(prob_ids) - 1, idx + 1)
            st.session_state.prob_index = next_idx
            st.session_state.prob_answered = False
            st.session_state.prob_sel_sq = None
            st.session_state.prob_legal_sqs = []
            st.rerun()

    # Progress
    st.markdown("---")
    st.progress((idx + 1) / len(prob_ids),
                text=f"{idx + 1} / {len(prob_ids)} 問")


# ── Click handling ────────────────────────────────────────────────────────
def get_legal_destinations_for_sq(board, from_sq):
    return list(set(mv.to_square for mv in board.legal_moves
                    if mv.from_square == from_sq))


def check_answer(move: shogi.Move) -> bool:
    """Check if user's move matches the correct move."""
    if correct_move is None:
        return False
    if move.from_square != correct_move.from_square:
        return False
    if move.to_square != correct_move.to_square:
        return False
    return True


if coords and not answered:
    px, py = coords["x"], coords["y"]
    board_hit = pixel_to_square(px, py)

    if board_hit is not None:
        file_0, rank_0 = board_hit
        clicked_sq = display_to_shogi_sq(file_0, rank_0)

        if sel_sq is None:
            # Select a piece
            piece = board.piece_at(clicked_sq)
            if piece is not None and piece.color == board.turn:
                st.session_state.prob_sel_sq = clicked_sq
                st.session_state.prob_legal_sqs = get_legal_destinations_for_sq(
                    board, clicked_sq)
        else:
            # Try to move
            matching = [mv for mv in board.legal_moves
                        if mv.from_square == sel_sq and mv.to_square == clicked_sq]
            if matching:
                user_move = matching[0]
                correct = check_answer(user_move)
                st.session_state.prob_answered = True
                st.session_state.prob_correct = correct
                st.session_state.prob_total += 1
                if correct:
                    st.session_state.prob_score += 1
            else:
                # Re-select
                piece = board.piece_at(clicked_sq)
                if piece is not None and piece.color == board.turn:
                    st.session_state.prob_sel_sq = clicked_sq
                    st.session_state.prob_legal_sqs = get_legal_destinations_for_sq(
                        board, clicked_sq)
                else:
                    st.session_state.prob_sel_sq = None
                    st.session_state.prob_legal_sqs = []

        st.rerun()
