import pandas as pd

USER_AGENT = "Mozilla/5.0"
FILE_URLS = {
    "stock_root": "https://blob.kodesiana.com/kodesiana-public-assets/devto/bright-data-web-scraping-hackathon-2024/trading-signal/",
    "sentiment": "https://blob.kodesiana.com/kodesiana-public-assets/devto/bright-data-web-scraping-hackathon-2024/trading-signal/sentiment.csv",
}

STOCK_TICKERS = ["AAPL", "META", "MSFT", "NVDA"]
TICKER_COMPANY_MAP = {
    "AAPL": "APPLE",
    "META": "META",
    "MSFT": "MICROSOFT",
    "NVDA": "NVIDIA",
}


def load_remote_sentiment():
    return pd.read_csv(
        FILE_URLS["sentiment"],
        parse_dates=["publication_date"],
        storage_options={"User-Agent": USER_AGENT},
    )


def load_remote_stock(ticker: str):
    return pd.read_csv(
        FILE_URLS["stock_root"] + ticker + ".csv",
        storage_options={"User-Agent": USER_AGENT},
    )


def calc_value(row):
    if row["sentiment"] == "POSITIVE":
        return 1
    if row["sentiment"] == "NEGATIVE":
        return -1

    return 0
