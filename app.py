import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import requests  # Added for the header fix

st.title("📈 Stock Price Analyzer")

# 1. Updated function with a User-Agent to fix the 403 Forbidden error
@st.cache_data 
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # This header tells Wikipedia you are a browser, not a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    table = pd.read_html(response.text)
    df = table[0]
    return df['Symbol'].tolist()

# 2. Sidebar inputs using the new list
tickers_list = get_sp500_tickers()
ticker = st.sidebar.selectbox("Select Stock Ticker (S&P 500)", tickers_list)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch stock data using yfinance
stock = yf.download(ticker, start=start_date, end=end_date)

if stock.empty:
    st.error("No data found. Check ticker symbol.")
else:
    # Plot closing prices
    st.subheader(f"{ticker} Closing Price Chart")
    
    st.line_chart(stock["Close"])

    # Plot 7-day, 30-day, 90-day Moving Averages
    st.subheader("Moving Averages")
    ma_periods = [7, 30, 90]
    for ma in ma_periods:
        stock[f"MA{ma}"] = stock["Close"].rolling(ma).mean()

    fig, ax = plt.subplots()
    ax.plot(stock["Close"], label="Close", linewidth=1.5)
    for ma in ma_periods:
        ax.plot(stock[f"MA{ma}"], label=f"MA {ma}")
    ax.legend()
    st.pyplot(fig)

    # Plot Daily Returns
    st.subheader("Daily Returns")
    stock["Daily Return (%)"] = stock["Close"].pct_change() * 100
    st.line_chart(stock["Daily Return (%)"])
