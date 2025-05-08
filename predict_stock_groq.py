import os
from groq import Groq

def predictStockPrice(GROQ_API_KEY, stock_keyword, financial_results, sentiment_analysis):
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial forecasting assistant. "
                    "Analyze stock data using time-series methods and sentiment analysis. "
                    "Only provide a direct forecast and the reasoning behind it. "
                    "Avoid general explanations or apologies."
                )
            },
            {
                "role": "user",
                "content": f"""
Here is 6-month financial data and sentiment analysis for {stock_keyword}:
{financial_results}
{sentiment_analysis}

Based on this, predict tomorrow's closing price. Include reasoning using trends, anomalies, and volatility.
                """
            }
        ],
        max_tokens=4000,
        temperature=0.0
    )

    return response.choices[0].message.content
