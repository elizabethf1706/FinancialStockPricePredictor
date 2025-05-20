import os
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

from textblob import TextBlob
from newsapi import NewsApiClient
from dotenv import load_dotenv

from stock_predictor import (
    get_5_month_stock_data,
    prepare_data_for_prophet,
    train_prophet_model,
    evaluate_model,
    get_tomorrow_forecast
)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")


def fetch_news_documents(api_key, query="stocks", num_articles=5):
    newsapi = NewsApiClient(api_key=api_key)
    from datetime import datetime, timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        headlines = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            page_size=num_articles
        )
    except Exception as e:
        print(f"Problem getting articles from NewsAPI: {e}")
        return []

    if headlines['status'] == 'ok' and headlines['articles']:
        return [
            Document(page_content=article['title'] + "\n" + (article.get('description') or ""))
            for article in headlines['articles']
        ]
    else:
        return []

# Fetch documents dynamically
documents = fetch_news_documents(newsapi_key)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)

split_docs = [doc for doc in split_docs if doc.page_content.strip()]
if not split_docs:
    raise ValueError("No valid documents to index in FAISS.")

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = vector_store.as_retriever()

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

def get_sentiment_analysis(api_key, stock_keyword):
    newsapi = NewsApiClient(api_key=api_key)
    from datetime import datetime, timedelta

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        headlines = newsapi.get_everything(
            q=stock_keyword,
            language='en',
            sort_by='relevancy',
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            page_size=5
        )
    except Exception as e:
        print(f"Problem getting articles from NewsAPI: {e}")
        return "Sentiment unavailable due to API error."

    if headlines['status'] == 'ok' and headlines['articles']:
        combined_text = " ".join(article['title'] for article in headlines['articles'])
        sentiment = TextBlob(combined_text).sentiment
        return f"Polarity: {sentiment.polarity:.2f}, Subjectivity: {sentiment.subjectivity:.2f}"
    else:
        return "No recent articles found to analyze sentiment."

print("Ask me about stocks, e.g., 'What's the forecast for TSLA?':")

while True:
    query = input("\n>> ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if any(ticker := word.strip().upper() for word in query.split() if word.isalpha() and len(word) <= 5):
        stock_data = get_5_month_stock_data(ticker)
        if stock_data is not None:
            prophet_data = prepare_data_for_prophet(stock_data)
            model, forecast = train_prophet_model(prophet_data)

            if model and forecast is not None:
                tomorrow_pred = get_tomorrow_forecast(forecast)
                evaluation_metrics = evaluate_model(model, forecast, prophet_data)
                sentiment = get_sentiment_analysis(newsapi_key, ticker)

                print(f"\n Forecast for {ticker}:")
                print(f"Predicted closing price for tomorrow: ${tomorrow_pred:.2f}" if tomorrow_pred else "No forecast available.")
                print(f"MAE: {evaluation_metrics['mae']:.2f}, RMSE: {evaluation_metrics['rmse']:.2f}, MAPE: {evaluation_metrics['mape']:.2f}%")
                print(f" Sentiment analysis: {sentiment}")
            else:
                print("Model training failed.")
        else:
            print("Could not retrieve stock data.")
    else:
        answer = qa_chain.run(query)
        print(f"\nAnswer: {answer}")
