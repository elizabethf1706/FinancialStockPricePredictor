#import chromadb
import requests
import os


#7OOYZDM6H53OW8L8 : 1st
#YQBAK9042LP6L4W6 : 2nd
#E2BGLXNMJ7P0G7NS : 3rd
#use vpn to switch between servers and ip addresses.

'''
Add a ticker's most recent earnings call transcript to the ChromaDB collection, if not already in it.
'''
def add_ticker_to_chroma(ticker: str, ticker_db: str, client) -> None:
    collections_names = [collection.name for collection in client.list_collections()]

    if ticker_db in collections_names:
        print(f"[{os.path.basename(__file__)}]  {ticker_db} already exists in the database.")
        return None
    else:
        stock_collection = client.create_collection(f"{ticker_db}")
        print(f"[{os.path.basename(__file__)}]  {ticker_db} was not in the database. A {ticker_db} collection was created.")

    transcript_dict: dict = {}
    year = 2025
    quarter = 4

    while len(transcript_dict) == 0 and transcript_dict is not None:

        query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={year}Q{quarter}&apikey=KCMNKODOBZ1L8YW7'
        response = requests.get(query_url)

        if response.status_code != 200:
            print(f"[{os.path.basename(__file__)}]  Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

        else:
            data: dict = response.json()
            try:
                transcript_dict: dict = data["transcript"]

                if len(transcript_dict) == 0:
                    quarter -= 1
                    if quarter == 0:
                        quarter = 4
                        year -= 1

                    if year == 2024 and quarter < 3:
                        print(f"[{os.path.basename(__file__)}]  No transcript found for {ticker} in any recent quarter.")
                        return None
            
            except Exception as e:
                print(f"[{os.path.basename(__file__)}]  No transcript found for {ticker}. Probably API rate limit exceeded.")
                return None
    
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
    print(f"[{os.path.basename(__file__)}]  Added {len(documents)} entries to ChromaDB for {ticker} in quarter {year}Q{quarter}.")

    return None
        