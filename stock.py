import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import altair as alt

days = 20
tickers = {
    'apple':'AAPL',
    'facebook':'FB',
    'google':'GOOGL',
    'microsoft':'MSFT',
    'netflix':'NFLX',
    'amazon':'AMZN'
}

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
    st.write(df)

df = pd.DataFrame()

companies = ['apple', 'facebook']
data = df.loc[companies]
data.sort_index()
data.T.reset_index()

data = pd.melt(data, id_vars=['Date'])

st.write(data)

'''
def get_info(tickers):
    for company in tickers.keys():
        info = company.info
        action = company.actions
        company.dividends.plot()
        company.actions['Stock Splits'].plot()

'''