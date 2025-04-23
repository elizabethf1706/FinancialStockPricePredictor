# This file is to call apis for sentiment analysis.
# note youll have to download TEXTBLOB and NEWSAPI and python.
# imports the library with textlob so we can use it

from textblob import TextBlob
from datetime import datetime, timedelta
# imports newsapi to pull news.
from newsapi import NewsApiClient
import os # Need this to check for the API key env var

def get_sentiment_analysis(api_key, stock_keyword):
    """Grabs news for a stock and figures out the sentiment.

    Needs:
     - api_key: Your NewsAPI key.
     - stock_keyword: The stock/company name to search for.

    Returns:
     A dictionary with the results (counts, percentages, etc.)
     or None if something went wrong (like no articles found).
    """
    newsapi = NewsApiClient(api_key=api_key)

    # pull time, calculate and format date.
    # NOTE: NEWSAPI free plan only goes back A MONTH
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    try:
        # articles is a newsapi object and it defines the lang, date, uses stock name to search articles.
        articles = newsapi.get_everything(
            q=stock_keyword,
            language='en',
            sort_by='publishedAt',
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            page_size=100  # max is 100.
        )
    except Exception as e:
        print(f"Problem getting articles from NewsAPI: {e}")
        return None

    # counter for pos articles and neg
    sentiment = 0
    accumulated_positive = 0
    accumulated_negative = 0
    #used for retaining total values
    accumulated_pos = 0
    accumulated_neg = 0
    neutral = 0
    
    for article in articles['articles']:
    # this combines the title, description and content, and the '' is used in case
    # there is a missing item.
        art_combined = (
            (article.get('title') or '') + ' ' + # Added space
            (article.get('description') or '') + ' ' + # Added space
            (article.get('content') or '')
        )

        if art_combined.strip():
            # here we analyze sentiment. for each article we see the polarity.
            # if pos, add to positive polarity and if neg add to neg pol, else add to neutral.
        
            blob = TextBlob(art_combined)
            current_article_polarity = blob.sentiment.polarity

            # check polarity and add to tallies
            if current_article_polarity > 0.1:
                accumulated_positive += 1
                accumulated_pos += current_article_polarity
            elif current_article_polarity < -0.1:
                accumulated_negative += 1
                accumulated_neg += current_article_polarity 
            else:
                neutral += 1
    
    # This is the value of the average sentiment that we can use in the chart.
    
    total_articles = accumulated_positive + accumulated_negative + neutral

    if total_articles > 0:
        positive_pct = (accumulated_positive / total_articles) * 100
        negative_pct = (accumulated_negative / total_articles) * 100
        neutral_pct = (neutral / total_articles) * 100
        average_positive_over_all = accumulated_pos / total_articles
        average_negative_over_all = accumulated_neg / total_articles

        average_polarity_of_pos = accumulated_pos / accumulated_positive if accumulated_positive else 0
        average_polarity_of_neg = accumulated_neg / accumulated_negative if accumulated_negative else 0

        results = {
            "stock": stock_keyword,
            "total_articles": total_articles,
            "positive_count": accumulated_positive,
            "negative_count": accumulated_negative,
            "neutral_count": neutral,
            "positive_pct": positive_pct,
            "negative_pct": negative_pct,
            "neutral_pct": neutral_pct,
            "avg_pos_polarity_all": average_positive_over_all,
            "avg_neg_polarity_all": average_negative_over_all,
            "avg_polarity_of_pos": average_polarity_of_pos,
            "avg_polarity_of_neg": average_polarity_of_neg
        }
        return results
    else:
        print(f"No articles found for {stock_keyword} to analyze.")
        return None
    
    
# adding polarity and subjectivity in case we wanted to use this.


# --- Removed the old direct execution part --- 
# (No more stock_keyword definition, API client init, printing) 