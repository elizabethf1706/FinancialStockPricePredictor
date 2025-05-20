import streamlit as st 
          
from sentiment_analyzer import get_sentiment_analysis   
from sentiment_visualizer import plot_sentiment_distribution 
from news_word_cloud import get_wordcloud
from predict_stock_groq import predictStockPrice
from financial_data import get_StockSummary
from stock_predictor import get_5_month_stock_data, get_stock_data, get_tomorrow_forecast, prepare_data_for_prophet, train_prophet_model, evaluate_model
import plotly.graph_objects as go
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from financial_plotter import plot_historical_price_with_volume, plot_candlestick_chart, plot_price_with_moving_averages

# NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# ALPHA_API_KEY = st.secrets["ALPHA_API_KEY"]
NEWS_API_KEY='5a209c06298e4a60a4ea32789d08bbc7'
GROQ_API_KEY='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'
ALPHA_API_KEY='KHR0IMG7PZF7OHFK'


# Initialize NewsApiClient
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Function to get top 5 headlines for a stock
def get_top_headlines(stock_keyword): 
    "pull top 5 headlines for a stock and prints them"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        headlines = newsapi.get_everything(
                q=stock_keyword,
                language='en',
                sort_by='relevancy',
                from_param= start_date.strftime('%Y-%m-%d'),
                to=end_date.strftime('%Y-%m-%d'),  
                page_size=5
            )
    except Exception as e:
        print(f"Problem getting articles from NewsAPI: {e}")
        return None
        
    if headlines['status'] == 'ok':
        st.write(f"\n**Top 5 News Headlines for: {stock_keyword}**\n")
        for i, article in enumerate(headlines['articles'], 1):
            st.write(f"{i}. {article['title']}")
            st.write(f"   Source: {article['source']['name']}")
            st.write(f"   Published: {article['publishedAt']}")
    else:
        st.error("Error fetching headlines:", headlines.get("message"))

st.title("Stock News Sentiment Analyzer")

st.write("""
First enter a stock ticker to obtain headline articles and analyze news sentiment, then choose a model to forecast stock price.
""")

# ──────────────── INPUT ROW ──────────────── #
stock_keyword = st.text_input("Enter Stock Ticker", "TSLA")
model_options = ['llama3-8b-8192', 'llama3-70b-8192', 'Machine Learning Model']
selected_option = st.selectbox("Choose an option:", model_options)

continue_clicked = st.button("Continue")

# ──────────────── OUTPUT SECTION ──────────────── #
if continue_clicked:
    st.write(f"Okay, looking for news about '{stock_keyword}'...")
    with st.spinner('Fetching and analyzing news...'):
        # Fetch and display top headlines
        get_top_headlines(stock_keyword)

        # Continue with sentiment analysis and other tasks
        analysis_results = get_sentiment_analysis(NEWS_API_KEY, stock_keyword)
        wordcloud_results = get_wordcloud(NEWS_API_KEY, stock_keyword)
        financial_results = get_5_month_stock_data(stock_keyword)

        if selected_option != 'Machine Learning Model':
            stock_prediction = predictStockPrice(GROQ_API_KEY, selected_option, stock_keyword, financial_results, analysis_results)
        else:
            stock_prediction = None

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
        with st.spinner(f"Fetching and forecasting stock prices for {stock_keyword}..."):
            raw_data = get_stock_data(stock_keyword)
            prophet_ready = prepare_data_for_prophet(raw_data)
            model, forecast = train_prophet_model(prophet_ready)
            predicted_price = get_tomorrow_forecast(forecast)

        if predicted_price is not None:
            st.metric("📈 Predicted Closing Price (Tomorrow)", f"${predicted_price:.2f}")

        if forecast is not None and raw_data is not None and not raw_data.empty:
            st.success(f"Forecast and data analysis complete for {stock_keyword}!")

            tab1, tab2, tab3, tab4 = st.tabs(["Forecast Plot", "Historical Price & Volume", "Candlestick Chart", "Price & Moving Averages"])

            with tab1:
                st.subheader("Price Forecast")
                fig_forecast = go.Figure()
                fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
                fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound', line=dict(dash='dot')))
                fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound', line=dict(dash='dot')))
                st.plotly_chart(fig_forecast, use_container_width=True)

                if prophet_ready is not None:
                    metrics = evaluate_model(model, forecast, prophet_ready)
                    st.write("Model Evaluation Metrics:")
                    st.json(metrics)
            
            with tab2:
                st.subheader("Historical Price and Volume")
                fig_hist_volume = plot_historical_price_with_volume(raw_data, stock_keyword)
                st.plotly_chart(fig_hist_volume, use_container_width=True)

            with tab3:
                st.subheader("Candlestick Chart")
                fig_candlestick = plot_candlestick_chart(raw_data, stock_keyword)
                st.plotly_chart(fig_candlestick, use_container_width=True)

            with tab4:
                st.subheader("Price and Moving Averages")
                fig_ma = plot_price_with_moving_averages(raw_data, stock_keyword)
                st.plotly_chart(fig_ma, use_container_width=True)

        elif forecast is None:
            st.error(f"Forecasting failed for {stock_keyword}.")
        elif raw_data is None or raw_data.empty:
            st.error(f"Could not retrieve historical data for {stock_keyword} to display charts.")
