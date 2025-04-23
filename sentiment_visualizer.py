import matplotlib.pyplot as plt
import os

def plot_sentiment_distribution(positive_count, negative_count, neutral_count, stock_keyword, save_dir='charts', st=None):
    """
    Alright, so this function just takes the sentiment counts we got
    (how many positive, negative, and neutral articles) and makes a
    simple bar chart out of it.

    Needs these bits of info:
     - positive_count: how many good news articles
     - negative_count: how many bad news articles
     - neutral_count: how many meh news articles
     - stock_keyword: which stock we looked up (goes in the title)
     - save_dir: where to put the chart image, defaults to 'charts' folder
     - st: optional Streamlit object (if provided, uses st.pyplot)
    """
    labels = ['Positive', 'Negative', 'Neutral']
    counts = [positive_count, negative_count, neutral_count]

    # quick check: bail if nothing came back
    if sum(counts) == 0:
        print("No sentiment data to plot.")
        return None # Return the figure object, or None

    # okay, set up the actual plot
    fig, ax = plt.subplots()
    bars = ax.bar(labels, counts, color=['green', 'red', 'grey'])

    ax.set_ylabel('Number of Articles')
    ax.set_title(f'Sentiment Analysis Results for {stock_keyword}')
    # show the numbers on the bars themselves, looks better
    ax.bar_label(bars, padding=3)

    # need to make the charts/ folder if it's not there
    # (Only relevant if saving is uncommented)
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)

    #!!! UNCOMMENT THIS TO SAVE THE CHART TO YOUR COMPUTER
    # saving the chart to your computer by the name of the stock ticker
    # filename = f'{stock_keyword}_sentiment_distribution.png'
    # filepath = os.path.join(save_dir, filename)
    # plt.savefig(filepath)
    # print(f"Chart saved to {filepath}")

    # If we got a streamlit object, use it to show the plot
    if st:
        st.pyplot(fig)
    else:
        # otherwise, just display it normally (like in a regular script)
        plt.show()

    return fig # Return the figure object in case it's needed 