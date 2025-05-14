# now uses env file for keys

import streamlit as st 
import os              
from dotenv import load_dotenv
import chromadb

from sentiment_analyzer import get_sentiment_analysis   
from sentiment_visualizer import plot_sentiment_distribution 
from news_word_cloud import get_wordcloud
from predict_stock_groq import predictStockPrice
from financial_data import get_StockSummary

load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')

@st.cache_resource
def start_db():
    return chromadb.PersistentClient(path="./chroma")
    
client = start_db()



#START
st.title("Stock News Sentiment Analyzer")

st.write("""
Let's see if the news about a stock is generally positive or negative.
Just type in a stock ticker or company name below.
""")

# text box where the user can type in the stock 
stock_keyword = st.text_input("Enter Stock Ticker or Company Name:", "TSLA")

@st.cache_resource
def define_collection(ticker: str):
    if len(ticker) < 3:
        ticker += "12"
    return client.create_collection(f"{ticker}")
stock_collection = define_collection(stock_keyword)

if st.button("Analyze Sentiment"):
    if not stock_keyword:
        st.warning("Please enter a stock keyword to analyze.")

    else:
        st.write(f"Okay, looking for news about '{stock_keyword}'...")
        


        with st.spinner('Fetching and analyzing news...'): # spinning wheel while the analysis is happening
            analysis_results = get_sentiment_analysis(NEWS_API_KEY, stock_keyword)
            wordcloud_results = get_wordcloud(NEWS_API_KEY, stock_keyword)
            financial_results = get_StockSummary(ALPHA_API_KEY, stock_keyword) 
            stock_prediction = predictStockPrice(GROQ_API_KEY, stock_keyword, financial_results, analysis_results)


        if analysis_results: # if we got results back
            st.success("Sentiment Analysis complete!")

            # the metrics
            st.subheader("Analysis Results:")
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive Articles", f"{analysis_results['positive_count']}", f"{analysis_results['positive_pct']:.1f}%")
            col2.metric("Negative Articles", f"{analysis_results['negative_count']}", f"{analysis_results['negative_pct']:.1f}%")
            col3.metric("Neutral Articles", f"{analysis_results['neutral_count']}", f"{analysis_results['neutral_pct']:.1f}%")


            st.write(f"*(Based on {analysis_results['total_articles']} articles from the last 30 days)*")

            # the bar char
            st.subheader("Sentiment Distribution Chart:")
            plot_sentiment_distribution(
                positive_count=analysis_results['positive_count'],
                negative_count=analysis_results['negative_count'],
                neutral_count=analysis_results['neutral_count'],
                stock_keyword=analysis_results['stock'],
                st=st )  
        else:
            st.error(f"Couldn't get or analyze news for '{stock_keyword}'. Maybe check the ticker or try again later?") 
        

        if wordcloud_results: # checks to make sure word cloud results is returned then outputs them
            st.success("Wordcloud complete!")
            st.pyplot(wordcloud_results) 
        else:
            st.error(f"Couldn't make wordcloud for '{stock_keyword}'. Maybe check the ticker or try again later?") 
        
        
        if stock_prediction and financial_results: # checks to make sure stocks results is returned then outputs them
            st.success("Here is the predicted analysis: ")
            st.write(stock_prediction)  
        else:
            st.error(f"Couldn't make stock analysis for '{stock_keyword}'. Maybe check the ticker or try again later?") 


        if stock_collection:
            st.subheader("🤖Ask Grok")
            st.write("Ask Grok about something related to the stock.")
                
            user_input = st.text_input("Ask Grok:", "What do the earnings calls say?")
            
            with st.spinner('Grok is thinking...'):
                # Query the collection
                results = stock_collection.query(
                    query_texts=[user_input],
                    n_results=3
                )
                # Display the results
                #TODO: put through ai so we see what Grok says about it.
                st.write("Grok's response:")
                for result in results['documents'][0]:
                    st.write(result)
