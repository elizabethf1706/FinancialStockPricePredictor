import requests
import streamlit as st
from chromadb import Client
from chromadb.config import Settings

def get_chroma_client():
    return Client(Settings(
        chroma_db_impl="duckdb",
        persist_directory=".chroma",
        anonymized_telemetry=False
    ))

def add_ticker_to_chroma(ticker: str, ticker_db: str, client) -> None:
    collections_names = [collection.name for collection in client.list_collections()]

    if ticker_db in collections_names:
        st.info(f"📂 Collection `{ticker_db}` already exists in ChromaDB.")
        return
    else:
        stock_collection = client.create_collection(f"{ticker_db}")
        st.success(f"✅ Created new collection `{ticker_db}` in ChromaDB.")

    transcript_dict: dict = {}
    year = 2025
    quarter = 4

    alpha_key = st.secrets["ALPHA_VANTAGE_API_KEY"]

    while len(transcript_dict) == 0 and transcript_dict is not None:
        query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={year}Q{quarter}&apikey={alpha_key}'
        response = requests.get(query_url)

        if response.status_code != 200:
            st.error(f"❌ Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")
        else:
            data = response.json()
            try:
                transcript_dict = data["transcript"]

                if len(transcript_dict) == 0:
                    quarter -= 1
                    if quarter == 0:
                        quarter = 4
                        year -= 1
                    if year == 2024 and quarter < 3:
                        st.warning(f"⚠️ No recent transcript found for {ticker}.")
                        return
            except Exception:
                st.warning(f"⚠️ API limit hit or no transcript for {ticker}.")
                return
    
    documents = []
    metadatas = []
    ids = []

    for i, entry in enumerate(transcript_dict):
        documents.append(entry["content"])
        metadatas.append({
            "speaker": entry["speaker"],
            "title": entry["title"],
            "sentiment": entry["sentiment"]
        })
        ids.append(f"{ticker}_{i}")

    stock_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    client.persist()

    st.success(f"📈 Added {len(documents)} entries for {ticker} (Q{quarter} {year}) to ChromaDB.")
