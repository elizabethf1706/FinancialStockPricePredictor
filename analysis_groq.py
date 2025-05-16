import os
from groq import Groq

def predictStockPrice(GROQ_API_KEY, stock_keyword, financial_results,sentiment_analysis):
    # Create the Groq client
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user", 
            "content": f"""
            I am providing you with the following 6 month financial data for the stock {stock_keyword} and a sentiment analysis:
            {financial_results} {sentiment_analysis}

            Using this data, apply time series forecasting methods to predict the stock's closing price for tomorrow. Consider trends, sentiment, volatility, and historical movements in the stock's price. Explain the reasoning behind your prediction,highlighting key patterns, trends, or anomalies that influenced the forecast. 
    Please do not apologize or provide general explanations. Focus solely on predicting the stock price for tomorrow.
            """}],
        max_tokens=4000,
        temperature=0.0  # Factual-based responses with minimal creativity
    )   

    return response.choices[0].message.content


def advise_earnings_from_query(GROQ_API_KEY, stock_keyword, query_results, user_question):
    client = Groq(api_key=GROQ_API_KEY)
    documents = query_results["documents"][0]
    speaker_title = query_results["metadatas"][0]

    content = ""
    
    for passage in range(len(documents)):
        entry = f"{speaker_title[passage]["speaker"]} ({speaker_title[passage]["title"]}): \n {documents[passage]} \n\n"
        content += entry
    
    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": f"""Using only the following excerpts from {stock_keyword}'s most recent earnings call transcript, 
                        provide a direct and well-supported answer to the user’s question: '{user_question}'. Base your response 
                        strictly on the information in the excerpts. Here are the excerpts: {content}. Whenever you refer
                        to the provided texts, instead say the most recent earnings calls. When you can, use numbered points."""
        }],
        temperature = 0
    )
    
    return response.choices[0].message.content