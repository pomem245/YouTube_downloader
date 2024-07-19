import datetime as dt
import time as tm
import yfinance as yf
import streamlit as st

# Current date
date_now = tm.strftime('%Y-%m-%d')
start = (dt.date.today() - dt.timedelta(days=1104)).strftime('%Y-%m-%d')


df = yf.download('AAPL', start=start , end=date_now)

# Defaults to "application/octet-stream"
st.download_button("Download binary file", df)
