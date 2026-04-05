import streamlit as st

st.set_page_config(
    page_title="将棋アプリ",
    page_icon="♟",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("♟ 将棋アプリ")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎮 対局")
    st.write("AIと対局できます。難易度は1級から棋士レベルまで選択可能。")
    st.page_link("pages/1_対局.py", label="対局を始める", icon="🎮")

with col2:
    st.subheader("🧩 次の一手")
    st.write("300問の詰将棋・次の一手問題に挑戦できます。（1級〜五段レベル）")
    st.page_link("pages/2_次の一手.py", label="問題を解く", icon="🧩")

with col3:
    st.subheader("📊 棋譜解析")
    st.write("保存された棋譜を解析し、好手・悪手をハイライト表示します。")
    st.page_link("pages/3_棋譜解析.py", label="棋譜を解析する", icon="📊")

st.markdown("---")
st.markdown("### 使い方")
st.markdown("""
- **対局**: 難易度を選択してAIと対局。駒をクリックして移動先をクリックするだけ。
- **次の一手**: 問題の盤面を見て、最善手を選んでください。クリック操作で回答。
- **棋譜解析**: 対局後の棋譜を読み込んで、各局面の評価値を確認。
""")
