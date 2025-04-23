# # This file is to call apis for sentiment analysis.
# # note youll have to download TEXTBLOB and NEWSAPI and python.
# # imports the library with textlob so we can use it
# from textblob import TextBlob
# from datetime import datetime, timedelta
# # imports newsapi to pull news.
# from newsapi import NewsApiClient
# # Import the plotting function
# from visualize_sentiment import plot_sentiment_distribution

# newsapi = NewsApiClient(api_key='8f2e5849e7144acba9d5a9201c3b3542')
# # stock keyword needs to be given by user, but we will use tesla to test this for now.
# stock_keyword = "TESLA"
# # ideally text will be data from news api.
# # for sentiment analysis figure out how you will do it. will it be combining each text and then doing it ?
# # or will we sentiment analysis each text then combine? 

# # pulls articles using newsapi, but how many articles should we pull, and what length
# # of time?

# # pull time, calculate and format date.
# # NOTE: NEWSAPI free plan onle goes back A MONTH
# end_date = datetime.now()
# start_date = end_date - timedelta(days=30)


# # articles is a newsapi object and it defines the lang, date, uses stock name to search articles. 
# articles = newsapi.get_everything(
#     q=stock_keyword,
#     language='en',
#     sort_by='publishedAt',
#     from_param= start_date.strftime('%Y-%m-%d'),
#     to = end_date.strftime('%Y-%m-%d'),  
#     page_size=100  # max is 100.
# )

# # counter for pos articles and neg
# sentiment = 0
# accumulated_positive = 0
# accumulated_negative = 0
# #used for retaining total values
# accumulated_pos = 0
# accumulated_neg = 0
# neutral = 0

# for article in articles['articles']:
#     # this combines the title, description and content, and the '' is used in case
#     # there is a missing item.
#     art_combined =  (
#         (article.get('title') or '') + '' +         
#         (article.get('description') or '')+ '' + 
#         (article.get('content') or '')
#     )

#     if art_combined.strip():
#         # here we analyze sentiment. for each article we see the polarity.
#         # if pos, add to positive polarity and if neg add to neg pol, else add to neutral.
        
        
#         blob = TextBlob(art_combined)
#         current_article_polarity = blob.sentiment.polarity
#         if current_article_polarity > 0.1:
#             accumulated_positive += 1
#             accumulated_pos += current_article_polarity 
#         elif current_article_polarity < -0.1:
#             accumulated_negative += 1
#             accumulated_neg = current_article_polarity 
#         else:
#             neutral = neutral + 1
# # This is the value of the average sentiment that we can use in the chart.

# total_articles = accumulated_positive + accumulated_negative + neutral

# if total_articles > 0:
#     positive_pct = (accumulated_positive / total_articles) * 100
#     negative_pct = (accumulated_negative / total_articles) * 100
#     neutral_pct = (neutral / total_articles) * 100
#     average_positive = accumulated_pos / total_articles  if accumulated_positive else 0
#     average_negative = accumulated_neg / total_articles if accumulated_negative else 0

#     average_over_all_pos = accumulated_pos / accumulated_positive
#     average_over_all_neg = accumulated_neg / accumulated_negative
#     # this prints the count of pos articles and neg articles and states perentages.
#     print(f"Positive articles: {accumulated_positive} ({positive_pct:.2f}%)")
#     print(f"Negative articles: {accumulated_negative} ({negative_pct:.2f}%)")
#     print(f"Neutral articles: {neutral} ({neutral_pct:.2f}%)")
    
#     # this is the added pos and  polarity divided by all articles.
#     print(f"Positive articles average polarity over all articles: {average_positive:.3f}")
#     print(f"Negative articles average polarity over all articles: {average_negative:.3f}")
#     # this prints average by adding up all polarity divided by # of pos articles
#     print(f"Positive articles average polarity over all pos articles: {average_over_all_pos :.3f}")
#     # then print percentage
#     print(f"above as a percentag: {average_over_all_pos * 100:.2f}%")

#     print(f"Negative articles average polarity over all neg articles: {average_over_all_neg :.3f}")
#     print(f"above as a percentage: {average_over_all_neg * 100:.2f}%")

#     # calling visualize function to plot the chart 
#     plot_sentiment_distribution(accumulated_positive, accumulated_negative, neutral, stock_keyword)

# else:
#     print("No articles found to analyze.")

# # adding polarity and subjectivity in case we wanted to use this.
