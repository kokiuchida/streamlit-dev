"""Git Command 1000-Knock App — Streamlit."""

import random
import re
import json
from pathlib import Path

import streamlit as st

from questions import QUESTIONS

# ─── Constants ────────────────────────────────────────────────────────────────
SAVE_FILE = Path(__file__).parent / ".progress.json"
TOTAL = len(QUESTIONS)

# ─── Progress persistence ──────────────────────────────────────────────────────

def load_progress() -> dict:
    if SAVE_FILE.exists():
        try:
            return json.loads(SAVE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_progress(progress: dict) -> None:
    SAVE_FILE.write_text(json.dumps(progress))


# ─── Session-state bootstrap ───────────────────────────────────────────────────

def init_session():
    if "progress" not in st.session_state:
        st.session_state.progress = load_progress()  # {str(id): "correct" | "skipped"}
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "queue" not in st.session_state:
        st.session_state.queue = []
    if "hint_shown" not in st.session_state:
        st.session_state.hint_shown = False
    if "giveup_shown" not in st.session_state:
        st.session_state.giveup_shown = False
    if "answer_result" not in st.session_state:
        st.session_state.answer_result = None  # "correct" | "wrong" | None
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""
    if "submitted_answer" not in st.session_state:
        st.session_state.submitted_answer = ""


# ─── Queue helpers ─────────────────────────────────────────────────────────────

def build_queue(levels: list[int], mode: str) -> list[dict]:
    pool = [q for q in QUESTIONS if q["level"] in levels]
    if mode == "未正解のみ":
        pool = [q for q in pool if str(q["id"]) not in st.session_state.progress]
    if mode == "レベルランダム":
        random.shuffle(pool)
    return pool


def current_question() -> dict | None:
    q = st.session_state.queue
    idx = st.session_state.current_index
    if not q or idx >= len(q):
        return None
    return q[idx]


# ─── Answer check ──────────────────────────────────────────────────────────────

def normalize(s: str) -> str:
    """Normalize whitespace and quotes for lenient comparison."""
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    return s


def check_answer(user: str, question: dict) -> bool:
    u = normalize(user)
    for ans in question["answer"]:
        if normalize(ans) == u:
            return True
    return False


# ─── Navigation ────────────────────────────────────────────────────────────────

def reset_question_state():
    st.session_state.hint_shown = False
    st.session_state.giveup_shown = False
    st.session_state.answer_result = None
    st.session_state.user_answer = ""
    st.session_state.submitted_answer = ""


def go_next():
    st.session_state.current_index += 1
    reset_question_state()


def go_prev():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        reset_question_state()


def start_quiz(levels, mode):
    st.session_state.queue = build_queue(levels, mode)
    st.session_state.current_index = 0
    reset_question_state()


# ─── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ 設定")

        st.subheader("レベル選択")
        all_levels = list(range(1, 11))
        selected_levels = []
        cols = st.columns(2)
        for i, lv in enumerate(all_levels):
            col = cols[i % 2]
            checked = col.checkbox(f"Lv {lv}", value=True, key=f"lv_{lv}")
            if checked:
                selected_levels.append(lv)

        st.subheader("出題モード")
        mode = st.radio(
            "モード",
            ["通常", "未正解のみ", "レベルランダム"],
            label_visibility="collapsed",
        )

        st.divider()

        if st.button("▶ スタート / 再構成", use_container_width=True, type="primary"):
            if not selected_levels:
                st.warning("レベルを1つ以上選んでください。")
            else:
                start_quiz(selected_levels, mode)
                st.rerun()

        st.divider()

        # Progress summary
        st.subheader("📊 進捗")
        progress = st.session_state.progress
        correct_ids = {k for k, v in progress.items() if v == "correct"}
        total_in_queue = len(st.session_state.queue) if st.session_state.queue else 0
        st.metric("正解済み（全体）", f"{len(correct_ids)} / {TOTAL}")
        if total_in_queue:
            answered_in_queue = sum(
                1 for q in st.session_state.queue if str(q["id"]) in correct_ids
            )
            st.metric("正解済み（現キュー）", f"{answered_in_queue} / {total_in_queue}")

        if st.button("🔄 進捗リセット", use_container_width=True):
            st.session_state.progress = {}
            save_progress({})
            reset_question_state()
            st.rerun()


# ─── Main content ──────────────────────────────────────────────────────────────

def render_progress_bar():
    q = st.session_state.queue
    idx = st.session_state.current_index
    if not q:
        return
    pct = min(idx / len(q), 1.0)
    st.progress(pct, text=f"問題 {idx + 1} / {len(q)}")


def render_question(question: dict):
    progress = st.session_state.progress
    qid = str(question["id"])
    already_correct = progress.get(qid) == "correct"

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"### Q{question['id']}. [{question['category']}] "
            f"<span style='background:#4a90e2;color:white;padding:2px 8px;"
            f"border-radius:4px;font-size:0.85em'>Lv {question['level']}</span>",
            unsafe_allow_html=True,
        )
    with col2:
        if already_correct:
            st.success("✅ 正解済み")

    st.markdown(f"**{question['question']}**")

    # ── Answer input ──────────────────────────────────────────────────────────
    user_input = st.text_input(
        "コマンドを入力してください",
        value=st.session_state.user_answer,
        key="answer_input",
        placeholder="git ...",
    )
    st.session_state.user_answer = user_input

    col_sub, col_hint, col_skip, col_give = st.columns([2, 1, 1, 1])

    with col_sub:
        submitted = st.button("✔ 答え合わせ", type="primary", use_container_width=True)
    with col_hint:
        hint_btn = st.button("💡 ヒント", use_container_width=True)
    with col_skip:
        skip_btn = st.button("⏭ スキップ", use_container_width=True)
    with col_give:
        giveup_btn = st.button("🏳 ギブアップ", use_container_width=True)

    # ── Button actions ────────────────────────────────────────────────────────
    if submitted:
        st.session_state.submitted_answer = user_input
        if check_answer(user_input, question):
            st.session_state.answer_result = "correct"
            st.session_state.progress[qid] = "correct"
            save_progress(st.session_state.progress)
        else:
            st.session_state.answer_result = "wrong"

    if hint_btn:
        st.session_state.hint_shown = True

    if skip_btn:
        go_next()
        st.rerun()

    if giveup_btn:
        st.session_state.giveup_shown = True
        st.session_state.progress[qid] = "skipped"
        save_progress(st.session_state.progress)

    # ── Feedback area ─────────────────────────────────────────────────────────
    result = st.session_state.answer_result

    if result == "correct":
        st.success("🎉 正解！")
        with st.expander("📖 解説を読む", expanded=True):
            st.markdown(question["explanation"])
        if st.button("次の問題へ ➡", type="primary"):
            go_next()
            st.rerun()

    elif result == "wrong":
        st.error(f'❌ 不正解です。入力: `{st.session_state.submitted_answer}`')

    if st.session_state.hint_shown and result != "correct":
        st.info(f"💡 ヒント: {question['hint']}")

    if st.session_state.giveup_shown:
        st.warning("🏳 ギブアップ — 正解例:")
        for ans in question["answer"]:
            st.code(ans, language="bash")
        with st.expander("📖 解説を読む", expanded=True):
            st.markdown(question["explanation"])
        if st.button("次の問題へ ➡", key="next_after_giveup", type="primary"):
            go_next()
            st.rerun()


def render_complete():
    st.balloons()
    st.success("🏆 すべての問題が完了しました！おめでとうございます！")
    progress = st.session_state.progress
    correct_ids = {k for k, v in progress.items() if v == "correct"}
    queue = st.session_state.queue
    correct_in_q = sum(1 for q in queue if str(q["id"]) in correct_ids)
    st.metric("正解数", f"{correct_in_q} / {len(queue)}")
    if st.button("もう一度"):
        st.session_state.current_index = 0
        reset_question_state()
        st.rerun()


def render_empty():
    st.info(
        "サイドバーでレベルと出題モードを選択して「▶ スタート」を押してください。\n\n"
        "「未正解のみ」モードで問題が0件の場合は、進捗リセットするか別のモードを選んでください。"
    )


# ─── App entry point ───────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Git コマンド 1000本ノック",
        page_icon="🔨",
        layout="wide",
    )

    init_session()
    render_sidebar()

    st.title("🔨 Git コマンド 1000本ノック")
    st.caption(f"全 {TOTAL} 問 | レベル 1〜10")

    if not st.session_state.queue:
        render_empty()
        return

    render_progress_bar()
    st.divider()

    q = current_question()
    if q is None:
        render_complete()
    else:
        render_question(q)

    # Navigation footer
    st.divider()
    nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
    with nav_col1:
        if st.button("◀ 前の問題", disabled=st.session_state.current_index == 0):
            go_prev()
            st.rerun()
    with nav_col3:
        q_list = st.session_state.queue
        if st.button(
            "次の問題 ▶",
            disabled=st.session_state.current_index >= len(q_list) - 1,
        ):
            go_next()
            st.rerun()


if __name__ == "__main__":
    main()
