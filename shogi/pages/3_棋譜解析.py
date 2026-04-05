"""
棋譜解析ページ - Game log analysis
"""

import streamlit as st
import shogi
import os
import sys
import io
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shogi_engine.board_renderer import render_board
from shogi_engine.ai_engine import evaluate, get_best_move, MATERIAL_VALUES

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

st.set_page_config(page_title="棋譜解析", layout="wide")
st.title("📊 棋譜解析")

LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logs"
)
os.makedirs(LOG_DIR, exist_ok=True)


# ── KIF parser ────────────────────────────────────────────────────────────
KIF_PIECE_MAP = {
    "歩": shogi.PAWN, "香": shogi.LANCE, "桂": shogi.KNIGHT,
    "銀": shogi.SILVER, "金": shogi.GOLD, "角": shogi.BISHOP,
    "飛": shogi.ROOK, "玉": shogi.KING, "王": shogi.KING,
    "と": shogi.PROM_PAWN, "成香": shogi.PROM_LANCE,
    "杏": shogi.PROM_LANCE,
    "成桂": shogi.PROM_KNIGHT, "圭": shogi.PROM_KNIGHT,
    "成銀": shogi.PROM_SILVER, "全": shogi.PROM_SILVER,
    "馬": shogi.PROM_BISHOP, "龍": shogi.PROM_ROOK,
    "竜": shogi.PROM_ROOK,
}

FILE_MAP = {str(i): i for i in range(1, 10)}
RANK_MAP = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9}


def kif_to_usi_moves(kif_text: str):
    """Parse KIF text and return list of USI move strings."""
    moves = []
    lines = kif_text.splitlines()
    move_pattern = re.compile(
        r'^\s*(\d+)\s+([１-９])([一二三四五六七八九])([\w成]+?)(打|\(\d\d\))'
    )
    for line in lines:
        m = move_pattern.match(line)
        if not m:
            continue
        to_file_full = m.group(2)
        to_rank_ja = m.group(3)
        piece_and_promo = m.group(4)
        from_part = m.group(5)

        # Convert full-width digit to int
        to_file = ord(to_file_full) - ord('１') + 1
        to_rank = RANK_MAP.get(to_rank_ja, 0)
        if to_rank == 0:
            continue

        to_sq_name = f"{to_file}{chr(ord('a') + to_rank - 1)}"
        try:
            to_sq = shogi.SQUARE_NAMES.index(to_sq_name)
        except ValueError:
            continue

        if from_part == "打":
            # Drop: find piece type
            piece_name = piece_and_promo.replace("成", "")
            pt = KIF_PIECE_MAP.get(piece_name)
            if pt is None:
                continue
            piece_char = {
                shogi.PAWN: "P", shogi.LANCE: "L", shogi.KNIGHT: "N",
                shogi.SILVER: "S", shogi.GOLD: "G", shogi.BISHOP: "B",
                shogi.ROOK: "R",
            }.get(pt, "P")
            moves.append(f"{piece_char}*{to_sq_name}")
        else:
            # Board move
            from_file = int(from_part[1])
            from_rank = int(from_part[2])
            from_sq_name = f"{from_file}{chr(ord('a') + from_rank - 1)}"
            try:
                from_sq = shogi.SQUARE_NAMES.index(from_sq_name)
            except ValueError:
                continue
            promotion = "成" in piece_and_promo
            usi = from_sq_name + to_sq_name + ("+" if promotion else "")
            moves.append(usi)

    return moves


def analyze_game_fast(moves_usi: list, depth: int = 2):
    """
    Analyze a game quickly.
    Returns list of dicts with move info and evaluation.
    """
    board = shogi.Board()
    results = []

    for i, move_usi in enumerate(moves_usi):
        try:
            move = shogi.Move.from_usi(move_usi)
        except Exception:
            continue
        if move not in board.legal_moves:
            break

        # Evaluate before move
        score_before = evaluate(board)

        # Make the move
        board.push(move)
        score_after = evaluate(board)

        # From current player perspective (negate for white)
        if board.turn == shogi.BLACK:
            # White just moved
            score_delta = score_after - score_before
        else:
            # Black just moved
            score_delta = score_before - score_after

        results.append({
            "move_num": i + 1,
            "move_usi": move_usi,
            "score": score_after,
            "score_delta": score_delta,
        })

    return results


# ── Load existing logs ────────────────────────────────────────────────────
def list_kif_files():
    files = [f for f in os.listdir(LOG_DIR) if f.endswith(".kif")]
    return sorted(files, reverse=True)


# ── Session state ─────────────────────────────────────────────────────────
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []
    st.session_state.analysis_moves = []
    st.session_state.analysis_view_idx = 0
    st.session_state.analysis_board_states = []


# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 棋譜読み込み")

    kif_files = list_kif_files()
    if kif_files:
        selected_file = st.selectbox("保存済み棋譜", kif_files)
        if st.button("📂 読み込む", use_container_width=True):
            path = os.path.join(LOG_DIR, selected_file)
            with open(path, encoding="utf-8") as f:
                kif_text = f.read()
            with st.spinner("解析中..."):
                moves_usi = kif_to_usi_moves(kif_text)
                results = analyze_game_fast(moves_usi)
                # Reconstruct board states
                board_states = []
                b = shogi.Board()
                board_states.append(b.copy())
                for usi in moves_usi:
                    try:
                        mv = shogi.Move.from_usi(usi)
                        if mv in b.legal_moves:
                            b.push(mv)
                            board_states.append(b.copy())
                    except Exception:
                        break

            st.session_state.analysis_results = results
            st.session_state.analysis_moves = moves_usi
            st.session_state.analysis_view_idx = 0
            st.session_state.analysis_board_states = board_states
            st.success(f"解析完了: {len(results)}手")

    st.markdown("---")
    uploaded = st.file_uploader("棋譜ファイルをアップロード", type=["kif", "txt"])
    if uploaded:
        kif_text = uploaded.read().decode("utf-8", errors="replace")
        with st.spinner("解析中..."):
            moves_usi = kif_to_usi_moves(kif_text)
            results = analyze_game_fast(moves_usi)
            board_states = []
            b = shogi.Board()
            board_states.append(b.copy())
            for usi in moves_usi:
                try:
                    mv = shogi.Move.from_usi(usi)
                    if mv in b.legal_moves:
                        b.push(mv)
                        board_states.append(b.copy())
                except Exception:
                    break
        st.session_state.analysis_results = results
        st.session_state.analysis_moves = moves_usi
        st.session_state.analysis_view_idx = 0
        st.session_state.analysis_board_states = board_states
        st.success(f"解析完了: {len(results)}手")


# ── Main content ──────────────────────────────────────────────────────────
results = st.session_state.analysis_results
board_states = st.session_state.analysis_board_states
moves_usi = st.session_state.analysis_moves

if not results:
    st.info("左サイドバーから棋譜を読み込んでください。")
    st.markdown("""
    ### 使い方
    1. **対局**ページで対局し、棋譜を保存
    2. 上のサイドバーから保存済み棋譜を選択して「読み込む」
    3. または棋譜ファイルをアップロード
    4. 各手の評価値と好手・悪手がハイライト表示されます
    """)
    st.stop()


# ── Evaluation graph ──────────────────────────────────────────────────────
st.subheader("📈 評価値グラフ")

scores = [r["score"] for r in results]
move_nums = [r["move_num"] for r in results]

# Build chart data
chart_data = {"手数": move_nums, "評価値": scores}

try:
    import pandas as pd
    df = pd.DataFrame(chart_data)
    st.line_chart(df.set_index("手数"))
except ImportError:
    st.line_chart({"評価値": scores})


# ── Move table ────────────────────────────────────────────────────────────
st.subheader("📋 手の評価一覧")

THRESHOLD_GOOD = -30
THRESHOLD_BLUNDER = -300

def classify_move(delta):
    if delta >= THRESHOLD_GOOD:
        return "好手", "#90EE90"
    elif delta >= THRESHOLD_BLUNDER:
        return "普通", "#FFFFFF"
    else:
        return "悪手", "#FFB6C1"


# Display table with colors
col_table, col_board_view = st.columns([1, 1])

with col_table:
    st.markdown("クリックで局面を表示")
    header = "| 手数 | 指手 | 評価値 | 変化 | 評価 |"
    sep    = "|------|------|--------|------|------|"
    rows = [header, sep]
    for r in results:
        label, _ = classify_move(r["score_delta"])
        delta_str = f"{r['score_delta']:+d}"
        rows.append(
            f"| {r['move_num']} | `{r['move_usi']}` | {r['score']} | {delta_str} | {label} |"
        )
    st.markdown("\n".join(rows))


with col_board_view:
    st.subheader("局面ビューア")
    view_idx = st.slider(
        "手数を選択",
        min_value=0,
        max_value=len(board_states) - 1,
        value=st.session_state.analysis_view_idx,
        key="analysis_slider"
    )
    st.session_state.analysis_view_idx = view_idx

    if view_idx < len(board_states):
        view_board = board_states[view_idx]
        last_mv = None
        if view_idx > 0 and view_idx - 1 < len(moves_usi):
            try:
                last_mv = shogi.Move.from_usi(moves_usi[view_idx - 1])
            except Exception:
                pass

        img = render_board(view_board, last_move=last_mv)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=False)

        if view_idx > 0 and view_idx - 1 < len(results):
            r = results[view_idx - 1]
            label, color = classify_move(r["score_delta"])
            st.metric("評価値", r["score"], delta=r["score_delta"])
            if label == "好手":
                st.success(f"この手は{label}です！")
            elif label == "悪手":
                st.error(f"この手は{label}です。")
            else:
                st.info(f"この手は{label}です。")


# ── Statistics ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📊 統計")

good_moves = sum(1 for r in results if classify_move(r["score_delta"])[0] == "好手")
blunders = sum(1 for r in results if classify_move(r["score_delta"])[0] == "悪手")
normal_moves = len(results) - good_moves - blunders

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    st.metric("総手数", len(results))
with col_s2:
    st.metric("好手", good_moves, delta=None)
with col_s3:
    st.metric("普通", normal_moves)
with col_s4:
    st.metric("悪手", blunders, delta=None)

black_blunders = sum(1 for i, r in enumerate(results)
                     if r["move_num"] % 2 == 1
                     and classify_move(r["score_delta"])[0] == "悪手")
white_blunders = sum(1 for i, r in enumerate(results)
                     if r["move_num"] % 2 == 0
                     and classify_move(r["score_delta"])[0] == "悪手")

col_b, col_w = st.columns(2)
with col_b:
    st.metric("▲先手の悪手数", black_blunders)
with col_w:
    st.metric("△後手の悪手数", white_blunders)
