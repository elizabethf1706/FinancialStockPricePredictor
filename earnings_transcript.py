import requests
import chromadb

"""
    Fetches the earnings call transcript for a given company and quarter.
    
    Args:
        apikey (str): The API key for Alpha Vantage.
        ticker (str): The stock ticker symbol of the company.
        quarter (str): The quarter for which the earnings call transcript is needed.
        
    Returns:
        str: The earnings call transcript.
    """
def get_earnings_call_transcript(apikey: str, ticker: str, quarter: str) -> str:
    
    clientDB = chromadb.PersistentClient()
    collection = clientDB.get_or_create_collection("database")


    query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={quarter}&apikey={apikey}'

    response = requests.get(query_url)

    if response.status_code != 200:
        print(f"Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

    else:
        data: dict = response.json()
        
    
    try: #If API was bad, trascript_dict will be empty and a type error will be thrown
        # Extract the earnings call transcript
            transcript_dict: set = data["transcript"]
            transcript_words = ""
            total_sentiment = 0.0
            id = 0

            for entry in transcript_dict:
                total_sentiment += float(entry["sentiment"])
                transcript_words += entry["speaker"] + "\n" + entry["content"] + "\n\n"
                collection.add(
                    documents=[entry["content"]],
                    metadatas=[{"source": entry["speaker"]}],
                    ids=[f"{ticker}_{id}"] 
                )
                print(f"Added to collection for {ticker} and id {ticker}_{id}")
                
                id += 1


            """TODO: SUPER SLOW TO ADD TO DB BY PARAGRAPH, MAYBE JUST DO ALL OF IT AT ONCE"""
            print(f"Transcript for {ticker} added to the database.")


    except Exception as e:
        print(f"No transcript found. Probably API rate limit exceeded.")
        return None


    return transcript_words
# or return transcript_dict later on;