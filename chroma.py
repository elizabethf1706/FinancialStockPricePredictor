import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Uncomment and configure ChromaDB client
import chromadb
from chromadb.config import Settings

load_dotenv()

# --- Setup ChromaDB client ---
chroma_client = chromadb.Client(Settings())

# --- Streamlit UI ---
st.set_page_config(page_title="ChromaDB Ticker Importer", layout="centered")
st.title("📊 Add Ticker's Earnings Transcript to ChromaDB")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", value="")
submit = st.button("Add Transcript to ChromaDB")

# --- Main Function ---
def add_ticker_to_chroma(ticker: str, ticker_db: str, client) -> str:
    collections_names = [collection.name for collection in client.list_collections()]
    status_messages = []

    if ticker_db in collections_names:
        return f"✅ `{ticker_db}` already exists in the database."

    stock_collection = client.create_collection(f"{ticker_db}")
    status_messages.append(f"🆕 `{ticker_db}` collection created.")

    transcript_dict: dict = {}
    year = 2025
    quarter = 4

    while len(transcript_dict) == 0 and transcript_dict is not None:
        query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={year}Q{quarter}&apikey={os.getenv("ALPHA_API_KEY")}'
        response = requests.get(query_url)

        if response.status_code != 200:
            return f"❌ Failed to retrieve transcript. Status code: {response.status_code}"

        try:
            data: dict = response.json()
            transcript_dict: dict = data["transcript"]

            if len(transcript_dict) == 0:
                quarter -= 1
                if quarter == 0:
                    quarter = 4
                    year -= 1
                if year == 2024 and quarter < 3:
                    return f"⚠️ No transcript found for {ticker} in recent quarters."

        except Exception as e:
            return f"❌ Error parsing response: {e}"

    documents = []
    metadatas = []
    ids = []

    for i, entry in enumerate(transcript_dict):
        speaker: str = entry["speaker"]
        speaker_title: str = entry["title"]
        content: str = entry["content"]
        sentiment: str = entry["sentiment"]

        documents.append(content)
        metadatas.append({"speaker": speaker, "title": speaker_title, "sentiment": sentiment})
        ids.append(f"{ticker}_{i}")

    stock_collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return f"✅ Added {len(documents)} entries to `{ticker_db}` for {year}Q{quarter}."


# --- Trigger Logic ---
if submit:
    if ticker:
        ticker_db = f"{ticker}_transcript"
        result = add_ticker_to_chroma(ticker.upper(), ticker_db, chroma_client)
        st.success(result) if result.startswith("✅") else st.warning(result)
    else:
        st.error("Please enter a valid stock ticker.")
