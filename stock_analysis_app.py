
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Analysis Tool", layout="wide")

st.title("📊 Stock Analysis Tool")
ticker_input = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT, TSLA):")

if ticker_input:
    stock = yf.Ticker(ticker_input.upper())

    try:
        info = stock.info

        st.header(f"Summary: {info.get('longName', ticker_input.upper())}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Sector**: {info.get('sector', 'N/A')}")
            st.markdown(f"**Industry**: {info.get('industry', 'N/A')}")
            st.markdown(f"**Description**: {info.get('longBusinessSummary', 'N/A')}")
            st.markdown(f"**Key Segments**: {info.get('category', 'N/A')}")
        with col2:
            st.markdown(f"**Current Price**: ${info.get('currentPrice', 'N/A')}")
            st.markdown(f"**52-Week High**: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.markdown(f"**52-Week Low**: ${info.get('fiftyTwoWeekLow', 'N/A')}")
            st.markdown(f"**Market Cap**: ${info.get('marketCap', 0):,}")

        hist = stock.history(period="1y")
        for ma in [7, 28, 50, 100, 200]:
            hist[f"MA_{ma}"] = hist["Close"].rolling(ma).mean()

        st.subheader("Financial Metrics")
        st.markdown(f"**Revenue (TTM)**: ${info.get('totalRevenue', 'N/A'):,}")
        st.markdown(f"**EBITDA (TTM)**: ${info.get('ebitda', 'N/A'):,}")
        st.markdown(f"**Free Cash Flow (FCF)**: ${info.get('freeCashflow', 'N/A'):,}")
        st.markdown(f"**Enterprise Value (EV)**: ${info.get('enterpriseValue', 'N/A'):,}")

        st.subheader("Price Trends with Moving Averages")
        for ma in [7, 50, 100, 200]:
            st.write(f"### {ma}-Day Moving Average")
            st.line_chart(hist[["Close", f"MA_{ma}"]])

        st.subheader("Analyst Target Price")
        st.markdown(f"**Target Mean**: ${info.get('targetMeanPrice', 'N/A')}")
        st.markdown(f"**Target High**: ${info.get('targetHighPrice', 'N/A')}")
        st.markdown(f"**Target Low**: ${info.get('targetLowPrice', 'N/A')}")
        st.markdown("**Top Analysts (Example Data Placeholder)**:")
        st.markdown("- Morgan Stanley: $X target")
        st.markdown("- Goldman Sachs: $Y target")
        st.markdown("- JPMorgan: $Z target")
        st.markdown("- BofA: $A target")
        st.markdown("- Barclays: $B target")

        st.subheader("Intrinsic Value Estimate (Simple DCF)")
        try:
            fcf = stock.cashflow.loc["Total Cash From Operating Activities"].mean() / 1e9
            growth = 0.08
            discount_rate = 0.10
            terminal_growth = 0.02

            dcf_value = sum(fcf * ((1 + growth)**year) / ((1 + discount_rate)**year) for year in range(1, 6))
            terminal_value = (fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
            terminal_value /= (1 + discount_rate)**5
            intrinsic_value = dcf_value + terminal_value
            shares_outstanding = info.get('sharesOutstanding', np.nan)
            value_per_share = (intrinsic_value * 1e9) / shares_outstanding if shares_outstanding else "N/A"
            st.success(f"Estimated Intrinsic Value/Share: ${value_per_share:.2f}")
        except Exception:
            st.warning("Insufficient data for intrinsic value calculation.")

        st.subheader("Download Data")
        financials_df = pd.DataFrame.from_dict({
            'Sector': info.get('sector'),
            'Market Cap': info.get('marketCap'),
            'Trailing PE': info.get('trailingPE'),
            'EPS (TTM)': info.get('trailingEps'),
            'ROE': info.get('returnOnEquity'),
            'Price to Book': info.get('priceToBook'),
            'Target Mean': info.get('targetMeanPrice'),
            'Target High': info.get('targetHighPrice'),
            'Target Low': info.get('targetLowPrice')
        }, orient='index', columns=['Value'])

        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        csv_fin = convert_df(financials_df)
        st.download_button("Download Financial Summary (CSV)", csv_fin, f"{ticker_input}_financials.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {e}")
