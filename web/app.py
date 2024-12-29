import streamlit as st

# --- initialize Streamlit app
pg = st.navigation(
    [
        st.Page(
            "signal.py", title="Trading Signal", icon=":material/candlestick_chart:"
        ),
        st.Page("news.py", title="Sentiment Analysis", icon=":material/newspaper:"),
    ]
)

st.set_page_config(page_title="Bright Data Hackathon")

# bootstrap
pg.run()
