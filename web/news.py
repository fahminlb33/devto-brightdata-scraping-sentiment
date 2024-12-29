import pandas as pd
import streamlit as st

from extras import calc_value, load_remote_sentiment, TICKER_COMPANY_MAP, STOCK_TICKERS


@st.cache_data
def load_sentiment() -> pd.DataFrame:
    df = load_remote_sentiment()

    df["ts"] = pd.to_datetime(df["publication_date"].dt.date)
    df["value"] = df.apply(calc_value, axis=1)

    df = df.sort_values("ts")

    return df


def main():
    st.title("📰 Sentiment Analysis")

    df = load_sentiment()
    df_counts = df["company"].value_counts()

    st.subheader("Number of news by Ticker")
    cols = st.columns(5)
    cols[0].metric("AAPL", df_counts[TICKER_COMPANY_MAP["AAPL"]])
    cols[1].metric("META", df_counts[TICKER_COMPANY_MAP["META"]])
    cols[2].metric("MSFT", df_counts[TICKER_COMPANY_MAP["MSFT"]])
    cols[3].metric("NVDA", df_counts[TICKER_COMPANY_MAP["NVDA"]])
    cols[4].metric("Other", df_counts["OTHER"])

    # select ticker
    ticker = st.selectbox("Ticker", STOCK_TICKERS)

    # subset data
    df_subset = df[df["company"] == TICKER_COMPANY_MAP[ticker]]

    # metric
    st.subheader("Number of sentiments")
    df_subset_sentiment_counts = df_subset["sentiment"].value_counts()

    cols = st.columns(3)
    cols[0].metric("Positive", df_subset_sentiment_counts["POSITIVE"])
    cols[1].metric("Neutral", df_subset_sentiment_counts["NEUTRAL"])
    cols[2].metric("Negative", df_subset_sentiment_counts["NEGATIVE"])

    # metric
    st.subheader("Number of sentiments by News Source")
    df_subset_source_counts = df_subset["source"].value_counts()

    cols = st.columns(3)
    cols[0].metric("BBC", df_subset_source_counts["BBC"])
    cols[1].metric("CNN", df_subset_source_counts["CNN"])
    cols[2].metric("Reuters", df_subset_source_counts["Reuters"])

    # table
    df_show = df_subset.drop(columns=["id", "value"]).sort_values(
        ["source", "publication_date"], ascending=[True, False]
    )
    st.dataframe(df_show, use_container_width=True)


# bootstrap
main()
