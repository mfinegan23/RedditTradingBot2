
import logging
from reddit_scraper import fetch_wallstreetbets_posts
from sentiment_analysis import analyze_sentiment, train_sentiment_model
import alpaca_trade_api as tradeapi
import time

# Set up logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Alpaca API setup
API_KEY = 'PK10TO199I4MPOAPT2IL'
API_SECRET = 'Dj3THjQHCrqZVGhoCYfcHgfIimug5gucG8blhOGJ'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Initialize the sentiment model
train_sentiment_model()

def trade_stock(ticker, action):
    """Trade stock based on the action and ticker symbol."""
    try:
        api.submit_order(
            symbol=ticker,
            qty=1,  # Quantity is set to 1 for demonstration
            side=action,
            type='market',
            time_in_force='gtc'
        )
        logging.info(f"Trade executed: {action} 1 share of {ticker}")
    except Exception as e:
        logging.error(f"Error placing trade for {ticker}: {e}")

def run_bot():
    """Fetch posts, analyze sentiment, and trade based on analysis."""
    # Get the recent posts from WallStreetBets
    posts = fetch_wallstreetbets_posts()
    ticker_sentiment = {}

    # Process each post
    for post in posts:
        combined_text = post['title'] + " " + post['body']
        sentiment = analyze_sentiment(combined_text)
        
        # Update sentiment for each ticker mentioned in the post
        for ticker in post['tickers']:
            ticker = ticker.replace("$", "").upper()
            if ticker not in ticker_sentiment:
                ticker_sentiment[ticker] = {'positive': 0, 'negative': 0}
            
            # Increment sentiment count
            if sentiment == "positive":
                ticker_sentiment[ticker]['positive'] += 1
            else:
                ticker_sentiment[ticker]['negative'] += 1

    # Decision logic for each ticker
    for ticker, sentiment_counts in ticker_sentiment.items():
        pos_count = sentiment_counts['positive']
        neg_count = sentiment_counts['negative']

        # Example trading decision: Buy if positive mentions > negative by 2x
        if pos_count > neg_count * 2:
            trade_stock(ticker, 'buy')
        elif neg_count > pos_count * 2:
            trade_stock(ticker, 'sell')
        else:
            logging.info(f"No strong sentiment for {ticker}. Skipping trade.")

if __name__ == "__main__":
    print("Starting Reddit Trading Bot...")
    # Run the bot every hour
    while True:
        logging.info("Running bot cycle...")
        run_bot()
        logging.info("Cycle complete. Waiting for next run...")
        time.sleep(3600)  # Wait 1 hour before running again
