"""
筋肉ダッシュボード - Google Drive上のスプレッドシートデータを可視化するStreamlitアプリ
"""

import pandas as pd
import plotly.express as px
import streamlit as st

import os

from dotenv import load_dotenv

from data_loader import load_muscle_data

load_dotenv()

# ──────────────────────────────────────────────
# ページ設定
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="筋肉ダッシュボード",
    page_icon="💪",
    layout="wide",
)

st.title("💪 筋肉トレーニングダッシュボード")

# ──────────────────────────────────────────────
# 環境変数から設定を読み込む（.env ファイルまたはシステム環境変数）
# ──────────────────────────────────────────────
FILE_ID = os.environ.get("GDRIVE_FILE_ID", "")
SHEET_NAME = os.environ.get("GDRIVE_SHEET_NAME", "workout")

if not FILE_ID:
    st.error("設定が不足しています。管理者に連絡してください。")
    st.stop()


@st.cache_data(ttl=600)
def fetch_data() -> pd.DataFrame:
    """Google Sheetsからデータを取得する（10分キャッシュ）。"""
    return load_muscle_data(FILE_ID, sheet_name=SHEET_NAME)

# ──────────────────────────────────────────────
# 列名定数
# ──────────────────────────────────────────────
COL_DATE = "日付"
COL_EXERCISE = "種目名"
COL_MUSCLE_MAJOR = "部位(大カテゴリー)"
COL_MUSCLE_MINOR = "部位(小カテゴリー)"
COL_WEIGHT = "重量"
COL_REPS = "回数"
COL_BILATERAL = "左右=2"
COL_TOTAL_WEIGHT = "計重量"
COL_SCORE = "点数"
COL_BODY_WEIGHT = "体重"
COL_MUSCLE_TOTAL = "総筋肉量(kg)"
COL_FAT_RATE = "体脂肪率(%)"
COL_FAT_MASS = "体脂肪量(kg)"
COL_BMI = "BMI"
COL_VISCERAL_FAT = "内臓脂肪レベル"
MUSCLE_REGION_COLS = ["筋肉量(左腕)", "筋肉量(右腕)", "筋肉量(左脚)", "筋肉量(右脚)", "筋肉量(胴)"]
FAT_REGION_COLS = ["脂肪量(左腕)", "脂肪量(右腕)", "脂肪量(左脚)", "脂肪量(右脚)", "脂肪量(胴)"]

# ──────────────────────────────────────────────
# データ読み込み
# ──────────────────────────────────────────────
with st.spinner("データを読み込み中..."):
    try:
        df_raw: pd.DataFrame = fetch_data()
    except Exception as e:
        st.error("データの読み込みに失敗しました。接続設定を確認してください。")
        st.stop()

# ──────────────────────────────────────────────
# サイドバー: フィルター
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("フィルター")

# ──────────────────────────────────────────────
# データ前処理
# ──────────────────────────────────────────────
df_raw[COL_DATE] = pd.to_datetime(df_raw[COL_DATE], errors="coerce")
df_raw = df_raw.dropna(subset=[COL_DATE])

# トレーニングデータ（種目名がある行）
df_train = df_raw.dropna(subset=[COL_EXERCISE]).copy()
for col in [COL_WEIGHT, COL_REPS, COL_TOTAL_WEIGHT]:
    df_train[col] = pd.to_numeric(df_train[col], errors="coerce")

# 身体データ（体重がある行を日付ごとに集約）
body_cols = [COL_DATE, COL_BODY_WEIGHT, COL_MUSCLE_TOTAL, COL_FAT_RATE, COL_FAT_MASS,
             COL_BMI, COL_VISCERAL_FAT] + MUSCLE_REGION_COLS + FAT_REGION_COLS
body_cols_present = [c for c in body_cols if c in df_raw.columns]
df_body = (
    df_raw[body_cols_present]
    .dropna(subset=[COL_BODY_WEIGHT])
    .groupby(COL_DATE)
    .first()
    .reset_index()
    .sort_values(COL_DATE)
)
for col in body_cols_present[1:]:
    df_body[col] = pd.to_numeric(df_body[col], errors="coerce")

# ──────────────────────────────────────────────
# フィルター UI（サイドバー）
# ──────────────────────────────────────────────
with st.sidebar:
    date_min = df_raw[COL_DATE].min().date()
    date_max = df_raw[COL_DATE].max().date()
    date_range = st.date_input("期間", value=(date_min, date_max), min_value=date_min, max_value=date_max)

    major_muscles = sorted(df_train[COL_MUSCLE_MAJOR].dropna().unique())
    selected_muscles = st.multiselect("部位（大カテゴリー）", options=major_muscles, default=major_muscles)

    st.divider()
    if st.button("データ更新", use_container_width=True):
        fetch_data.clear()
        st.rerun()

# フィルター適用
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df_train = df_train[(df_train[COL_DATE] >= start) & (df_train[COL_DATE] <= end)]
    df_body = df_body[(df_body[COL_DATE] >= start) & (df_body[COL_DATE] <= end)]

if selected_muscles:
    df_train = df_train[df_train[COL_MUSCLE_MAJOR].isin(selected_muscles)]

# ──────────────────────────────────────────────
# タブ
# ──────────────────────────────────────────────
tab_train, tab_body = st.tabs(["🏋️ トレーニング記録", "📊 身体データ"])

# ============================================================
# タブ1: トレーニング記録
# ============================================================
with tab_train:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("トレーニング日数", f"{df_train[COL_DATE].nunique()} 日")
    k2.metric("総セット数", f"{len(df_train):,}")
    k3.metric("総ボリューム (kg)", f"{int(df_train[COL_TOTAL_WEIGHT].sum()):,}")
    k4.metric("最大重量 (kg)", f"{df_train[COL_WEIGHT].max():.1f}")

    st.divider()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("ボリューム推移")
        vol_by_date = (
            df_train.groupby(df_train[COL_DATE].dt.date)[COL_TOTAL_WEIGHT]
            .sum()
            .reset_index()
        )
        vol_by_date.columns = ["日付", "ボリューム (kg)"]
        fig_line = px.line(vol_by_date, x="日付", y="ボリューム (kg)", markers=True,
                           color_discrete_sequence=["#E74C3C"])
        fig_line.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("部位別ボリューム")
        vol_by_muscle = (
            df_train.groupby(COL_MUSCLE_MAJOR)[COL_TOTAL_WEIGHT]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        vol_by_muscle.columns = ["部位", "ボリューム (kg)"]
        fig_bar = px.bar(vol_by_muscle, x="ボリューム (kg)", y="部位", orientation="h",
                         color="ボリューム (kg)", color_continuous_scale="Reds")
        fig_bar.update_layout(margin=dict(l=0, r=0, t=20, b=0), showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    col_bl, col_br = st.columns(2)

    with col_bl:
        st.subheader("種目別 最大重量 (kg)")
        max_weight = (
            df_train.groupby(COL_EXERCISE)[COL_WEIGHT]
            .max()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )
        max_weight.columns = ["種目", "最大重量 (kg)"]
        fig_max = px.bar(max_weight, x="最大重量 (kg)", y="種目", orientation="h",
                         color="最大重量 (kg)", color_continuous_scale="Blues")
        fig_max.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_max, use_container_width=True)

    with col_br:
        st.subheader("曜日別 トレーニング頻度")
        DOW_LABELS = ["月", "火", "水", "木", "金", "土", "日"]
        freq_by_dow = (
            df_train.assign(dow=df_train[COL_DATE].dt.dayofweek)
            .groupby("dow")[COL_DATE]
            .nunique()
            .reindex(range(7), fill_value=0)
            .reset_index()
        )
        freq_by_dow.columns = ["dow_num", "日数"]
        freq_by_dow["曜日"] = freq_by_dow["dow_num"].map(lambda x: DOW_LABELS[x])
        fig_dow = px.bar(freq_by_dow, x="曜日", y="日数", color="日数",
                         color_continuous_scale="Oranges")
        fig_dow.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_dow, use_container_width=True)

    with st.expander("生データを表示"):
        st.dataframe(df_train, use_container_width=True)

# ============================================================
# タブ2: 身体データ
# ============================================================
with tab_body:
    if df_body.empty:
        st.info("選択期間に身体データがありません。")
        st.stop()

    latest = df_body.iloc[-1]
    b1, b2, b3, b4, b5 = st.columns(5)
    if COL_BODY_WEIGHT in df_body.columns:
        b1.metric("体重 (kg)", f"{latest[COL_BODY_WEIGHT]:.1f}")
    if COL_MUSCLE_TOTAL in df_body.columns:
        b2.metric("総筋肉量 (kg)", f"{latest[COL_MUSCLE_TOTAL]:.1f}")
    if COL_FAT_RATE in df_body.columns:
        b3.metric("体脂肪率 (%)", f"{latest[COL_FAT_RATE]:.1f}")
    if COL_BMI in df_body.columns:
        b4.metric("BMI", f"{latest[COL_BMI]:.1f}")
    if COL_VISCERAL_FAT in df_body.columns:
        b5.metric("内臓脂肪レベル", f"{latest[COL_VISCERAL_FAT]:.0f}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("体重・筋肉量・体脂肪量の推移")
        rows = []
        for col, label in [(COL_BODY_WEIGHT, "体重"), (COL_MUSCLE_TOTAL, "総筋肉量"), (COL_FAT_MASS, "体脂肪量")]:
            if col in df_body.columns:
                tmp = df_body[[COL_DATE, col]].rename(columns={col: "値"})
                tmp["指標"] = label
                rows.append(tmp)
        if rows:
            fig_body = px.line(pd.concat(rows), x=COL_DATE, y="値", color="指標", markers=True)
            fig_body.update_layout(margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_body, use_container_width=True)

    with c2:
        st.subheader("体脂肪率・BMI推移")
        rows2 = []
        for col, label in [(COL_FAT_RATE, "体脂肪率(%)"), (COL_BMI, "BMI")]:
            if col in df_body.columns:
                tmp = df_body[[COL_DATE, col]].rename(columns={col: "値"})
                tmp["指標"] = label
                rows2.append(tmp)
        if rows2:
            fig_fat = px.line(pd.concat(rows2), x=COL_DATE, y="値", color="指標", markers=True)
            fig_fat.update_layout(margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_fat, use_container_width=True)

    present_muscle_cols = [c for c in MUSCLE_REGION_COLS if c in df_body.columns]
    if present_muscle_cols:
        st.subheader("部位別 筋肉量の推移")
        mr_rows = []
        for col in present_muscle_cols:
            tmp = df_body[[COL_DATE, col]].rename(columns={col: "値"})
            tmp["部位"] = col
            mr_rows.append(tmp)
        fig_mr = px.line(pd.concat(mr_rows), x=COL_DATE, y="値", color="部位", markers=True)
        fig_mr.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_mr, use_container_width=True)

    present_fat_cols = [c for c in FAT_REGION_COLS if c in df_body.columns]
    if present_fat_cols:
        st.subheader("部位別 脂肪量の推移")
        fr_rows = []
        for col in present_fat_cols:
            tmp = df_body[[COL_DATE, col]].rename(columns={col: "値"})
            tmp["部位"] = col
            fr_rows.append(tmp)
        fig_fr = px.line(pd.concat(fr_rows), x=COL_DATE, y="値", color="部位", markers=True)
        fig_fr.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_fr, use_container_width=True)

    with st.expander("身体データを表示"):
        st.dataframe(df_body, use_container_width=True)
