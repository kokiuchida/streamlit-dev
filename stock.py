import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt

st.title('米国株価可視化アプリ')
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1 , 825, 15)

st.write(f"""
### 過去 **{days}日間**のGAFA株価
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.cancat([df, hist])
    return df

st.sidebar.write("""
## 株価の指定
""")

ymin, ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0, 3500.0, (0.0, 3500,0)
)

tickers = {
    'apple':'AAPL',
    'facebook':'FB',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'netflix':'NFLX',
    'amazon':'AMZN'
}

df = get_data(days, tickers)
companies = st.multiselect(
    '会社名を選択してください',
    list(df.index),
    ['google','amazon','apple','facebook']
)

if not companies:
    st.error('少なくとも1社は選んでください')

companies = ['apple', 'facebook']
data = df.loc[companies]
data.sort_index()
data.T.reset_index()

data = pd.melt(data, id_vars=['Date']).rename(
    columns={'value': 'Stock Prices(USD)'}
)



chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
        color='Name:N'
    )
)





'''
def get_info(tickers):
    for company in tickers.keys():
        info = company.info
        action = company.actions
        company.dividends.plot()
        company.actions['Stock Splits'].plot()

'''