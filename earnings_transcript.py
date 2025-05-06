import requests

# ticker: str = "MSFT"  # ticker symbol for the company
# quarter: str = "2024Q1"  # quarter for which the earnings call transcript is needed
# apikey: str = "QP68QGJM0FU3IM1U"


def get_earnings_call_transcript(apikey: str, ticker: str, quarter: str) -> str:
    """
    Fetches the earnings call transcript for a given company and quarter.
    
    Args:
        apikey (str): The API key for Alpha Vantage.
        ticker (str): The stock ticker symbol of the company.
        quarter (str): The quarter for which the earnings call transcript is needed.
        
    Returns:
        str: The earnings call transcript.
    """

    query_url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={quarter}&apikey={apikey}'

    response = requests.get(query_url)

    if response.status_code != 200:
        print(f"Failed to retrieve transcript for {ticker}. Status code: {response.status_code}")

    else:
        print(f"Successfully retrieved transcript for {ticker}.")
        data: dict = response.json()
        

        # Extract the earnings call transcript
        #quarter = data["quarter"]
        transcript_dict: set = data["transcript"]
        transcript_words = ""
        total_sentiment = 0

        for entry in transcript_dict:
            total_sentiment += float(entry["sentiment"])
            transcript_words += entry["speaker"] + "\n" + entry["content"] + "\n\n"

        print(f"\nURL: {query_url}\n")
        print(f"\n{quarter}\n")
        print(f"Total Sentiment: {total_sentiment}\n")
        print(f"\n{ticker} Earnings Call Transcript:\n")
        print(f"\n{transcript_words}\n")


    return transcript_words
# or return transcript_dict later on;