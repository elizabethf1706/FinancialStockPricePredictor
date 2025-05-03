import os
from groq import Groq

def predictStockPrice(GROQ_API_KEY, stock_keyword, financial_results):
    # Create the Groq client
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user", 
            "content": f"""
            I am providing you with the following financial data for the stock {stock_keyword}:
            {financial_results}

            Using this data, apply time series forecasting methods to predict the stock's closing price for tomorrow. Consider trends, volatility, and historical movements in the stock's price. Explain the reasoning behind your prediction,highlighting key patterns, trends, or anomalies that influenced the forecast. 
    Please do not apologize or provide general explanations. Focus solely on predicting the stock price for tomorrow.
            """}],
        max_tokens=4000,
        temperature=0.0  # Factual-based responses with minimal creativity
    )   

    return response.choices[0].message.content
