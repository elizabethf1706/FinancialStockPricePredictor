# Function to get top 5 headlines for a stock
def get_top_headlines(stock_keyword): 
    "pull top 5 headlines for a stock and prints them"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

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
            st.write(f"   Published: {article['publishedAt']}\n")  # Removed the URL line
    else:
        st.error("Error fetching headlines:", headlines.get("message"))
