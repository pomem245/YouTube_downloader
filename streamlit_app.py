import datetime as dt
import time as tm
import yfinance as yf
import streamlit as st
import pandas as pd

# Current date
date_now = tm.strftime('%Y-%m-%d')
start = (dt.date.today() - dt.timedelta(days=1104)).strftime('%Y-%m-%d')


df = yf.download('AAPL', start=start , end=date_now)
df = df.to_csv(df)
# Defaults to "application/octet-stream"
st.download_button("Download binary file", df)
