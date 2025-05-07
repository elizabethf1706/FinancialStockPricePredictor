# now uses env file for keys

import streamlit as st 
import os              
from sentiment_analyzer import get_sentiment_analysis   
from sentiment_visualizer import plot_sentiment_distribution 
from news_word_cloud import get_wordcloud
from predict_stock_groq import predictStockPrice
from financial_data import get_StockSummary
from stock_predictor import get_stock_data, get_tomorrow_forecast, prepare_data_for_prophet, train_prophet_model, evaluate_model
import plotly.graph_objects as go
from dotenv import load_dotenv
load_dotenv() 

# Load API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")

st.title("Stock News Sentiment Analyzer")

st.write("""
Use the left box to analyze news sentiment, or the right box to forecast stock price.
""")

# ────────────── INPUT ROW ────────────── #
col1, col2 = st.columns(2)
with col1:
    stock_keyword = st.text_input("Sentiment: Enter Stock Ticker or Company Name", "TSLA")
    sentiment_clicked = st.button("Analyze Sentiment")

with col2:
    forecast_ticker = st.text_input("Forecast: Enter Stock Ticker", "AAPL")
    forecast_clicked = st.button("Forecast Stock Price")

# ────────────── OUTPUT SECTION ────────────── #
# FULL WIDTH: FORECAST
if forecast_clicked:
    st.write("## 📈 Forecast Results")
    if not forecast_ticker:
        st.warning("Please enter a stock ticker to forecast.")
    else:
        with st.spinner(f"Fetching and forecasting stock prices for {forecast_ticker}..."):
            raw_data = get_stock_data(forecast_ticker)
            prophet_ready = prepare_data_for_prophet(raw_data)
            model, forecast = train_prophet_model(prophet_ready)
            predicted_price = get_tomorrow_forecast(forecast)

        if predicted_price is not None:
            st.metric("📈 Predicted Closing Price (Tomorrow)", f"${predicted_price:.2f}")

        if forecast is not None:
            st.success(f"Forecast complete for {forecast_ticker}!")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound', line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound', line=dict(dash='dot')))
            st.plotly_chart(fig, use_container_width=True)

            if prophet_ready is not None:
                metrics = evaluate_model(model, forecast, prophet_ready)
                st.write("Model Evaluation Metrics:")
                st.json(metrics)
        else:
            st.error(f"Forecasting failed for {forecast_ticker}.")

# FULL WIDTH: SENTIMENT
if sentiment_clicked:
    st.write("## 📰 Sentiment Analysis Results")
    if not stock_keyword:
        st.warning("Please enter a stock keyword to analyze.")
    else:
        st.write(f"Okay, looking for news about '{stock_keyword}'...")

        with st.spinner('Fetching and analyzing news...'):
            analysis_results = get_sentiment_analysis(NEWS_API_KEY, stock_keyword)
            wordcloud_results = get_wordcloud(NEWS_API_KEY, stock_keyword)
            financial_results = get_StockSummary(ALPHA_API_KEY, stock_keyword) 
            stock_prediction = predictStockPrice(GROQ_API_KEY, stock_keyword, financial_results, analysis_results)

        if analysis_results:
            st.success("Sentiment Analysis complete!")

            col1, col2, col3 = st.columns(3)
            col1.metric("Positive Articles", f"{analysis_results['positive_count']}", f"{analysis_results['positive_pct']:.1f}%")
            col2.metric("Negative Articles", f"{analysis_results['negative_count']}", f"{analysis_results['negative_pct']:.1f}%")
            col3.metric("Neutral Articles", f"{analysis_results['neutral_count']}", f"{analysis_results['neutral_pct']:.1f}%")

            st.write(f"*(Based on {analysis_results['total_articles']} articles from the last 30 days)*")

            st.subheader("Sentiment Distribution Chart:")
            plot_sentiment_distribution(
                positive_count=analysis_results['positive_count'],
                negative_count=analysis_results['negative_count'],
                neutral_count=analysis_results['neutral_count'],
                stock_keyword=analysis_results['stock'],
                st=st 
            )
        else:
            st.error(f"Couldn't analyze news for '{stock_keyword}'.")

        if wordcloud_results:
            st.success("Wordcloud complete!")
            st.pyplot(wordcloud_results) 
        else:
            st.error(f"Couldn't generate wordcloud for '{stock_keyword}'.")

        if stock_prediction and financial_results:
            st.success("Here is the predicted analysis:")
            st.write(stock_prediction)
        else:
            st.error(f"Couldn't create stock analysis for '{stock_keyword}'.")
