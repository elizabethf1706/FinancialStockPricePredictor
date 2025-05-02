import os
from groq import Groq

def predictStockPrice(GROQ_API_KEY, stock_keyword):
    # Create the Groq client
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": f"Give me today's date. Predict the Stock Price for {stock_keyword} for tomorrow."}],
        max_tokens=1000,
        temperature=0.1 # this affects the AI's creativity to generate responses where 0 is only factual based responses.
    )   

    return response.choices[0].message.content
