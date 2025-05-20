import streamlit as st
import chromadb
import os
from dotenv import load_dotenv
from advise_earnings import advise_earnings_from_query
from chroma import add_ticker_to_chroma

# Load environment variables from .env
load_dotenv()

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@st.cache_resource
def initialize_chromadb():
    return chromadb.PersistentClient(path="./chroma")

CLIENT = initialize_chromadb()

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Please set it in your .env file.")
elif CLIENT:
    st.subheader(f"💬 Ask Groq")
    stock = st.text_input("Ask Groq about the most recent earnings calls", "TSLA")
    stock_db = stock + "12" if len(stock) < 3 else stock 

    user_question = st.text_input("Your question: ", "What are the latest developments?")
    
    if st.button("Ask"):
        with st.spinner("Asking Groq..."):
            add_ticker_to_chroma(stock, stock_db, CLIENT)
            stock_collection = CLIENT.get_collection(f"{stock_db}")
            
            db_query = stock_collection.query(
                query_texts=[user_question],
                n_results=10
            )

            groq_analysis = advise_earnings_from_query(GROQ_API_KEY, stock, db_query, user_question)
            st.write(groq_analysis)
