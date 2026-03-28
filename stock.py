import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

aapl = yf.Ticker('AAPL')
days = 20
hist = aapl.history(period=f'{days}d')

st.write(hist)