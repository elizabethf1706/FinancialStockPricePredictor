from wordcloud import WordCloud
import matplotlib.pyplot as plt
from newsapi import NewsApiClient
from nltk.corpus import stopwords
import nltk 
nltk.download('stopwords')

def get_wordcloud(api_key, stock_keyword):
    """Generates a word cloud from recent relevant news for a given stock.

    Args:
        api_key (str): NewsAPI key.
        stock_keyword (str): The stock/company name to search for.

    Returns:
        matplotlib.figure.Figure: Word cloud plot if successful.
        None: If no articles or an error occurred.
    """
    newsapi = NewsApiClient(api_key=api_key)
    
    nltk_stopwords_set = set()
    try:
        nltk_stopwords_set = set(stopwords.words('english'))
    except (LookupError, AttributeError) as e:
        print(f" some issue with stopwords that could not be loaded (Error: {type(e).__name__}: {e}).")
    
    final_stopwords = nltk_stopwords_set.copy()
    custom_stopwords = {
        "stock", "stocks", "price", "company", "companies", "market", "news", 
        "share", "shares", "value", "trading", "ticker", 
        stock_keyword.lower()
    }
    final_stopwords.update(custom_stopwords)

    try:
        articles = newsapi.get_everything(
            q=stock_keyword,
            language='en',
            sort_by='relevancy',
            page_size=5  # Max allowed
        )
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return None

    if not articles.get("articles"):
        print(f"No articles found for '{stock_keyword}'")
        return None

    combined_text = ""
    for article in articles["articles"]:
        combined_text += (article.get("title") or "") + " "
        combined_text += (article.get("description") or "") + " "

    if not combined_text.strip():
        print(f"No usable text data found for '{stock_keyword}'")
        return None

    try:
        wordcloud = WordCloud(width=1000, height=500, background_color='white', stopwords=final_stopwords, max_words=30).generate(combined_text)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"WordCloud for '{stock_keyword}'", fontsize=16)
        return fig
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None
