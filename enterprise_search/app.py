import streamlit as st
import yfinance as yf
from yfinance import EquityQuery, screen
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="トレンド企業検索",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔍 トレンド企業検索")
st.caption("企業ジャンル・国・TopN を選択してトレンド企業を検索します")

# ─── 定数 ────────────────────────────────────────────────────────────────────

SECTORS: dict[str, str] = {
    "テクノロジー": "Technology",
    "ヘルスケア": "Healthcare",
    "金融サービス": "Financial Services",
    "エネルギー": "Energy",
    "一般消費財": "Consumer Cyclical",
    "生活必需品": "Consumer Defensive",
    "素材": "Basic Materials",
    "不動産": "Real Estate",
    "通信サービス": "Communication Services",
    "公益事業": "Utilities",
    "資本財": "Industrials",
}

COUNTRIES: dict[str, str] = {
    "アメリカ": "us",
    "日本": "jp",
    "イギリス": "gb",
    "ドイツ": "de",
    "フランス": "fr",
    "中国": "cn",
    "韓国": "kr",
    "カナダ": "ca",
    "オーストラリア": "au",
    "インド": "in",
    "ブラジル": "br",
    "シンガポール": "sg",
    "香港": "hk",
}

SORT_OPTIONS: dict[str, str] = {
    "時価総額": "intradaymarketcap",
    "出来高": "dayvolume",
    "価格上昇率": "percentchange",
}

CHART_PERIODS: dict[str, str] = {
    "1ヶ月": "1mo",
    "3ヶ月": "3mo",
    "6ヶ月": "6mo",
    "1年": "1y",
}

# ─── サイドバー ───────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("🎯 検索条件")

    selected_sector = st.selectbox("企業ジャンル", list(SECTORS.keys()))
    selected_country = st.selectbox("国", list(COUNTRIES.keys()))
    sort_by = st.selectbox("ランキング基準", list(SORT_OPTIONS.keys()))
    top_n = st.slider("TopN", min_value=3, max_value=20, value=5)
    chart_period = st.selectbox("チャート期間", list(CHART_PERIODS.keys()), index=1)

    search = st.button("🔍 検索", type="primary", use_container_width=True)

    st.divider()
    with st.expander("📌 使い方"):
        st.markdown(
            """
1. **企業ジャンル** — 業種を選択
2. **国** — 検索対象の国を選択
3. **ランキング基準** — 時価総額 / 出来高 / 価格上昇率
4. **TopN** — 表示企業数（3〜20 社）
5. **チャート期間** — 株価グラフの期間
6. **検索ボタン** — クリックで実行

各企業の **株価チャート・企業概要・最新ニュース・公式サイト** を確認できます。
        """
        )

# ─── データ取得関数 ───────────────────────────────────────────────────────────


@st.cache_data(ttl=300)
def fetch_trending_tickers(region: str, sector: str, sort_field: str, count: int) -> list[str]:
    """yfinance EquityQuery + screen でトレンド企業のティッカーを取得"""
    try:
        query = EquityQuery("and", [
            EquityQuery("eq", ["region", region]),
            EquityQuery("eq", ["sector", sector]),
        ])
        result = screen(query, sortField=sort_field, sortAsc=False, size=count)
        quotes = result.get("quotes", [])
        return [q["symbol"] for q in quotes if "symbol" in q]
    except Exception as e:
        st.error(f"スクリーナーエラー: {e}")
    return []


@st.cache_data(ttl=60)
def get_company_info(symbol: str) -> dict:
    try:
        return yf.Ticker(symbol).info
    except Exception:
        return {}


@st.cache_data(ttl=60)
def get_stock_history(symbol: str, period: str = "3mo") -> pd.DataFrame:
    try:
        return yf.Ticker(symbol).history(period=period)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_company_news(symbol: str) -> list:
    try:
        return yf.Ticker(symbol).news or []
    except Exception:
        return []


# ─── グラフ生成 ───────────────────────────────────────────────────────────────


def create_stock_chart(symbol: str, hist: pd.DataFrame, period_label: str) -> go.Figure | None:
    if hist.empty:
        return None

    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name="株価",
            increasing_line_color="#00b09b",
            decreasing_line_color="#ff4b4b",
        )
    )
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist["Volume"],
            name="出来高",
            yaxis="y2",
            opacity=0.25,
            marker_color="#6c757d",
        )
    )
    fig.update_layout(
        title=f"{symbol} — 株価チャート ({period_label})",
        xaxis_title="日付",
        yaxis_title="株価",
        yaxis2=dict(title="出来高", overlaying="y", side="right", showgrid=False),
        height=420,
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


# ─── ニュース表示 ─────────────────────────────────────────────────────────────


def render_news(news_list: list) -> None:
    if not news_list:
        st.info("ニュースが見つかりません")
        return

    displayed = 0
    for article in news_list:
        if displayed >= 5:
            break
        if not isinstance(article, dict):
            continue

        # yfinance >= 0.2.50 の新形式
        content = article.get("content", {})
        if content:
            title = content.get("title", "")
            url_obj = content.get("canonicalUrl") or content.get("clickThroughUrl") or {}
            link = url_obj.get("url", "") if isinstance(url_obj, dict) else ""
            provider = (content.get("provider") or {}).get("displayName", "")
            pub_date = content.get("pubDate", "")[:10] if content.get("pubDate") else ""
        else:
            # 旧形式
            title = article.get("title", "")
            link = article.get("link", "")
            provider = article.get("publisher", "")
            pub_ts = article.get("providerPublishTime", 0)
            pub_date = datetime.fromtimestamp(pub_ts).strftime("%Y/%m/%d") if pub_ts else ""

        if title and link:
            st.markdown(f"**[{title}]({link})**")
            st.caption(f"{provider}　{pub_date}")
            st.markdown("---")
            displayed += 1

    if displayed == 0:
        st.info("表示できるニュースがありません")


# ─── 企業カード表示 ───────────────────────────────────────────────────────────


def display_company_card(symbol: str, rank: int, period: str, period_label: str) -> None:
    info = get_company_info(symbol)
    if not info:
        st.warning(f"{symbol}: 情報を取得できませんでした")
        return

    company_name = info.get("longName") or info.get("shortName") or symbol
    currency = info.get("currency", "")

    st.markdown(f"### #{rank}　{company_name}　`{symbol}`")

    # ── メトリクス行 ──────────────────────────────────────────────────────────
    col_p, col_mc, col_per, col_vol, col_web = st.columns(5)

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")

    with col_p:
        if current_price:
            if current_price and prev_close:
                chg = current_price - prev_close
                chg_pct = chg / prev_close * 100
                delta_str = f"{chg:+.2f} ({chg_pct:+.2f}%)"
            else:
                delta_str = None
            st.metric("株価", f"{current_price:,.2f} {currency}", delta_str)

    with col_mc:
        mc = info.get("marketCap")
        if mc:
            if mc >= 1e12:
                mc_str = f"{mc / 1e12:.2f} 兆"
            elif mc >= 1e8:
                mc_str = f"{mc / 1e8:.2f} 億"
            else:
                mc_str = f"{mc:,.0f}"
            st.metric("時価総額", f"{mc_str} {currency}")

    with col_per:
        pe = info.get("trailingPE")
        if pe:
            st.metric("PER", f"{pe:.1f} x")

    with col_vol:
        vol = info.get("regularMarketVolume") or info.get("volume")
        if vol:
            if vol >= 1e8:
                vol_str = f"{vol / 1e8:.2f} 億"
            elif vol >= 1e4:
                vol_str = f"{vol / 1e4:.2f} 万"
            else:
                vol_str = f"{vol:,}"
            st.metric("出来高", vol_str)

    with col_web:
        website = info.get("website", "")
        if website:
            display_url = website.replace("https://", "").replace("http://", "").rstrip("/")
            st.markdown(f"**🌐 公式サイト**")
            st.markdown(f"[{display_url}]({website})")

    # ── チャート & ニュース ────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        hist = get_stock_history(symbol, period)
        if not hist.empty:
            fig = create_stock_chart(symbol, hist, period_label)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{symbol}_{rank}")
        else:
            st.warning("株価データを取得できませんでした")

        summary = info.get("longBusinessSummary", "")
        if summary:
            with st.expander("📋 企業概要"):
                st.write(summary)

    with col_right:
        st.markdown("#### 📰 最新ニュース")
        news_list = get_company_news(symbol)
        render_news(news_list)

    st.divider()


# ─── メイン ───────────────────────────────────────────────────────────────────

if search:
    region = COUNTRIES[selected_country]
    sector = SECTORS[selected_sector]
    sort_field = SORT_OPTIONS[sort_by]
    period = CHART_PERIODS[chart_period]

    with st.spinner(f"{selected_country} / {selected_sector} のトレンド企業を検索中..."):
        tickers = fetch_trending_tickers(region, sector, sort_field, top_n)

    st.session_state["results"] = {
        "tickers": tickers,
        "sector": selected_sector,
        "country": selected_country,
        "sort_by": sort_by,
        "period": period,
        "period_label": chart_period,
    }

if "results" in st.session_state:
    res = st.session_state["results"]
    tickers = res["tickers"]

    if tickers:
        st.success(
            f"✅ {res['country']} | {res['sector']} | "
            f"{res['sort_by']}順 | {len(tickers)} 社"
        )
        for i, sym in enumerate(tickers, 1):
            display_company_card(sym, i, res["period"], res["period_label"])
    else:
        st.warning("条件に一致する企業が見つかりませんでした。条件を変更して再検索してください。")
else:
    st.info("👈 左のサイドバーで検索条件を設定し、「検索」ボタンを押してください。")
