import streamlit as st

st.set_page_config(page_title="Finance Analysis", layout="centered")
st.title("💰 Finance Analysis")

st.session_state
st.subheader("Choosen stock is {}".format(st.session_state["stock"]))

#Bug
#You does not reset session_state["stock"] for whatever reason
if st.button("🔙 Return to Search"):
    st.session_state["stock"] = ""
    print("Switching to {}".format(st.session_state["stock_search_page"]))
    st.switch_page(st.session_state["stock_search_page"])
