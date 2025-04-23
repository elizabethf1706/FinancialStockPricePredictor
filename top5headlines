# This file calls apis to pull top 5 relevant headlines for a given stock word and prints them.
# note youll have to download NEWSAPI and python.
# imports the library with textlob so we can use it
from datetime import datetime, timedelta
# imports newsapi to pull news.
from newsapi import NewsApiClient

 
def get_top_headlines(api_key, stock_keyword): 
    "pull top 5 headlines for a stock and prints them"
    # NOTE: NEWSAPI free plan only goes back A MONTH
    # we set the time and date to use as args for newsapi.
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)


    # headlines is a obj that gets top 5 most relevant articles from last 30 days.
    
    try:
        headlines = newsapi.get_everything(
                q=stock_keyword,
                language='en',
                sort_by='relevancy',
                from_param= start_date.strftime('%Y-%m-%d'),
                to = end_date.strftime('%Y-%m-%d'),  
                page_size=5  # max is 100.
            )
    except Exception as e:
        print(f"Problem getting articles from NewsAPI: {e}")
        return None
        

    if headlines['status'] == 'ok':
        print(f"\nTop 5 news headlines for: {stock_keyword}\n")
        for i, article in enumerate(headlines['articles'], 1):
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Published: {article['publishedAt']}")
            print(f"   URL: {article['url']}\n")
    else:
        print("Error fetching headlines:", headlines.get("message"))
