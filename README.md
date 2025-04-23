This project aims to analyze and predict future prices of stocks using llms. Main components:

    1.Data pulling to feed for analysis
    2.Create charts for display
    3.Create sentiment analysis and pull articles related to stock.
    4.Implement LLM

Sentiment analysis - uses library Textblob for calculating polarity and library NewsAPI to pull articles.

I've made some changes to the project structure. Here's a very small explanation.
**Project Structure (Current Setup):**

So how's it laid out?

*   `main.py`: This is the Streamlit app you actually run. It's got the UI (text box, button) and calls the other bits.
*   `sentiment_analyzer.py`: This guy does the actual work of talking to NewsAPI, getting articles, and using TextBlob to analyze them.
*   `sentiment_visualizer.py`: Takes the analysis results and draws the bar chart.
*   `.env`: Super important - holds the `NEWS_API_KEY`. Make sure the key is in here!
*   `requirements.txt`: Just the list of Python libraries you need to install.
*   `README.md`: You're lookin' at it! 😉

**How to Run the App:**


1.  **Check the `.env` file:** Make sure your NewsAPI key is in there
2.  **Install stuff (if you haven't):** Open your terminal *in this project folder* and run `pip3 install -r requirements.txt` (or `pip3`, `python3 -m pip`, whatever works for you).
3.  **Run it!:** In the same terminal, just type:
    ```
    python3 -m streamlit run main.py
    ```
    That should pop open the app in your browser.

**Quick Note:**

*   **About `.env` / API Keys:** Just a heads-up, normally you wouldn't push your `.env` file with the real API key to something like GitHub. It's better to keep secrets out of github and keep it locally


*   **commented-files:** Heads up for the new structure to Work I had to comment the earlier file Structure, Which is SentimentAnalysis.py



