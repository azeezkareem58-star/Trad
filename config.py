import os
from dotenv import load_dotenv

load_dotenv()

# Bybit API Configuration
BYBIT_API_KEY = os.getenv('8dtd2hzZ290JoQ29yj')
BYBIT_API_SECRET = os.getenv('ta4bUAJO5JZyaGYqanRnHMFUc2uJHvYwLAVi')
BYBIT_TESTNET = True  # Set to False for live trading

# Trading Parameters
MAX_RISK_PER_TRADE = 0.05  # 5% maximum risk per trade
LEVERAGE = 10
TRADING_PAIR = "BTCUSDT"
TIMEFRAME = "15"

# Sentiment Analysis Sources
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Risk Management
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.04  # 4% take profit
MAX_POSITION_SIZE = 0.1  # 10% of capital per position

# Monitoring
SENTIMENT_UPDATE_INTERVAL = 300  # 5 minutes
PRICE_UPDATE_INTERVAL = 60  # 1 minute