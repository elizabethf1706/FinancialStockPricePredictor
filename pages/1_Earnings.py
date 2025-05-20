import streamlit as st
import chromadb
import os
from advise_earnings import advise_earnings_from_query
from chroma import add_ticker_to_chroma


@st.cache_resource
def initialize_chromadb():
    return chromadb.PersistentClient(path="./chroma")

CLIENT = initialize_chromadb()


if CLIENT:
    st.subheader(f"💬 Ask Groq")
    stock = st.text_input("Ask Groq about the most recent earnings calls", "TSLA")
    stock_db = stock+"12" if len(stock) < 3 else stock 

    print(f"[{os.path.basename(__file__)}]  Stock: {stock}, DB name: {stock_db}")

    user_question = st.text_input("Your question: ", "What are the latest developments?")
    
    if st.button("Ask"):
        with st.spinner("Asking Groq..."):
            add_ticker_to_chroma(stock, stock_db, CLIENT)
            stock_collection = CLIENT.get_collection(f"{stock_db}")
            print(f"[{os.path.basename(__file__)}]  Got collection")
            
            db_query = stock_collection.query(
                query_texts=[user_question],
                n_results=10
            )
            print(f"[{os.path.basename(__file__)}]  Got query results")

            groq_analysis = advise_earnings_from_query(st.secrets["GROQ_API_KEY"], stock, db_query, user_question)

            st.write(groq_analysis)