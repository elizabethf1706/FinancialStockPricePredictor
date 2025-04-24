import streamlit as st
from streamlit_searchbox import st_searchbox

st.set_page_config(page_title="Stock Search", layout="centered")
st.title("📈 Stock Search")


stock_names: list = ["AAPL", "AAPL2", "AAPLE", "MSFT", "NVDA", "AMZN", "GOOG",
                     "META", "BRK-B", "AVGO", "TSM", "TSLA"]

def search_func(keyword: str) -> list:
    stocks: list = []

    if keyword == "":
        return stock_names

    for stock in stock_names:
        if keyword.upper() in stock:
            stocks.append(stock)
    
    return stocks


stock_name: str = st_searchbox(search_func, placeholder="Search for Stock", key="searchbox")
is_disabled: bool = not stock_name


if st.button("🔍 Search", disabled=is_disabled):
    st.session_state["stock"] = stock_name
    print("Set stock to: {}".format(stock_name))
    print("Switching to {}".format(st.session_state["finance_analysis_page"]))
    st.switch_page(st.session_state["finance_analysis_page"])