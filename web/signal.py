import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from extras import (
    calc_value,
    load_remote_stock,
    load_remote_sentiment,
    TICKER_COMPANY_MAP,
    STOCK_TICKERS,
)


@st.cache_data
def load_stock_ticker(ticker: str) -> pd.DataFrame:
    df = load_remote_stock(ticker)

    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    df["ts"] = pd.to_datetime(df["Date"].dt.date)

    df["Close+1"] = df["Close"].shift(1)
    df["Close+7"] = df["Close"].shift(7)
    df["Close+30"] = df["Close"].shift(30)

    return df


@st.cache_data
def load_sentiment(ticker: str) -> pd.DataFrame:
    df = load_remote_sentiment()

    df["ts"] = pd.to_datetime(df["publication_date"].dt.date)

    df_subset = df[
        (df["company"] == TICKER_COMPANY_MAP[ticker]) & (df["ts"] >= "2022-12-28")
    ]

    df_subset = df_subset.copy().sort_values("publication_date")
    df_subset["value"] = df_subset.apply(calc_value, axis=1)

    return df_subset


def main():
    st.title("📈 Trading Signal")

    # select ticker
    ticker = st.selectbox("Ticker", STOCK_TICKERS)

    # load data
    df_stock = load_stock_ticker(ticker)
    df_sentiment = load_sentiment(ticker)

    # derive signal
    sel_cols = ["ts", "Close", "Close+1", "Close+7", "Close+30"]
    signals = df_sentiment.groupby("ts")["value"].mean().reset_index()
    signals = signals.merge(df_stock[sel_cols], on="ts", how="left").dropna()

    # plot
    fig = px.line(df_stock, x="Date", y="Close")
    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=signals[signals["value"] < 0.0]["ts"],
            y=signals[signals["value"] < 0.0]["Close"],
            fillcolor="red",
            name="Negative sentiment",
        )
    )
    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=signals[signals["value"] > 0.0]["ts"],
            y=signals[signals["value"] > 0.0]["Close"],
            fillcolor="green",
            name="Positive sentiment",
        )
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, key="trading_signal", use_container_width=True, theme=None)
    st.text("")
    st.text("")

    # df
    df_show = signals.copy()
    df_show["Sentiment"] = np.where(df_show["value"] > 0.0, "Up", "Down")
    df_show = df_show.drop(columns=["value"])
    st.dataframe(df_show, use_container_width=True)


# bootstrap
main()
