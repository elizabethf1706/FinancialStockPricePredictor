from wordcloud import WordCloud
import matplotlib.pyplot as plt
from newsapi import NewsApiClient
from nltk.corpus import stopwords

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
    stop_words = set(stopwords.words('english'))
    stop_words.update(["stock", "stocks", "price", "company", "companies", "market", "news", "share", "shares", "value", "trading", "ticker"])

    try:
        articles = newsapi.get_everything(
            q=stock_keyword,
            language='en',
            sort_by='relevancy',
            page_size=100  # Max allowed
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
        wordcloud = WordCloud(width=1000, height=500, background_color='white', stopwords=stop_words).generate(combined_text)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"WordCloud for '{stock_keyword}'", fontsize=16)
        return fig
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None
