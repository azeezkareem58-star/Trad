import time
import schedule
from datetime import datetime
import logging
from typing import Dict, Tuple

from config import *
from bybit_client import BybitTradingClient
from sentiment_analyzer import SentimentAnalyzer
from risk_management import RiskManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)

class TradingBot:
    def __init__(self):
        self.bybit_client = BybitTradingClient(
            BYBIT_API_KEY, 
            BYBIT_API_SECRET, 
            BYBIT_TESTNET
        )
        self.sentiment_analyzer = SentimentAnalyzer(
            NEWS_API_KEY, 
            TWITTER_BEARER_TOKEN
        )
        self.risk_manager = RiskManager(
            MAX_RISK_PER_TRADE,
            MAX_POSITION_SIZE
        )
        
        self.current_sentiment = 0.0
        self.sentiment_label = "NEUTRAL"
        self.account_balance = 0.0
        self.has_open_position = False
        
    def update_sentiment(self):
        """Update market sentiment"""
        try:
            self.current_sentiment, self.sentiment_label = \
                self.sentiment_analyzer.calculate_overall_sentiment()
            
            logging.info(f"Current Sentiment: {self.sentiment_label} ({self.current_sentiment:.3f})")
        except Exception as e:
            logging.error(f"Error updating sentiment: {e}")
    
    def update_account_info(self):
        """Update account balance and positions"""
        try:
            self.account_balance = self.bybit_client.get_account_balance()
            positions = self.bybit_client.get_open_positions(TRADING_PAIR)
            
            # Check if we have an open position
            if positions and 'result' in positions:
                position_data = positions['result']
                self.has_open_position = any(
                    float(pos['size']) > 0 for pos in position_data
                )
                
            logging.info(f"Account Balance: ${self.account_balance:.2f}")
            logging.info(f"Open Position: {self.has_open_position}")
            
        except Exception as e:
            logging.error(f"Error updating account info: {e}")
    
    def should_enter_trade(self) -> Tuple[bool, str]:
        """Determine if we should enter a trade based on sentiment"""
        if self.has_open_position:
            return False, "Position already open"
        
        if self.account_balance == 0:
            return False, "No balance available"
        
        # Strong bullish sentiment
        if self.current_sentiment > 0.15:
            return True, "LONG"
        
        # Strong bearish sentiment  
        elif self.current_sentiment < -0.15:
            return True, "SHORT"
        
        return False, "Neutral sentiment"
    
    def execute_trading_decision(self):
        """Execute trading logic"""
        try:
            # Update current price
            current_price = self.bybit_client.get_current_price(TRADING_PAIR)
            
            # Check if we should enter a trade
            should_trade, direction = self.should_enter_trade()
            
            if should_trade and current_price > 0:
                logging.info(f"Signal to enter {direction} trade")
                
                # Calculate stop loss and take profit
                stop_loss, take_profit = self.risk_manager.calculate_stop_loss_take_profit(
                    current_price, direction.lower()
                )
                
                # Calculate position size
                position_value, quantity = self.risk_manager.calculate_position_size(
                    current_price, self.account_balance, stop_loss
                )
                
                # Validate trade meets risk criteria
                if self.risk_manager.validate_trade(quantity, current_price, self.account_balance):
                    # Place order
                    order_side = "Buy" if direction == "LONG" else "Sell"
                    order_result = self.bybit_client.place_order(
                        symbol=TRADING_PAIR,
                        side=order_side,
                        quantity=quantity,
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
                    
                    if order_result:
                        logging.info(f"Successfully placed {direction} order")
                        logging.info(f"Quantity: {quantity}, Entry: ${current_price:.2f}")
                        logging.info(f"Stop Loss: ${stop_loss:.2f}, Take Profit: ${take_profit:.2f}")
                    else:
                        logging.error("Failed to place order")
                else:
                    logging.warning("Trade rejected by risk manager")
            
            elif self.has_open_position:
                logging.info("Monitoring open position...")
                
        except Exception as e:
            logging.error(f"Error in trading decision: {e}")
    
    def run(self):
        """Main bot execution loop"""
        logging.info("Starting Trading Bot...")
        
        # Schedule tasks
        schedule.every(SENTIMENT_UPDATE_INTERVAL).seconds.do(self.update_sentiment)
        schedule.every(PRICE_UPDATE_INTERVAL).seconds.do(self.update_account_info)
        schedule.every(PRICE_UPDATE_INTERVAL).seconds.do(self.execute_trading_decision)
        
        # Initial updates
        self.update_sentiment()
        self.update_account_info()
        
        # Main loop
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Bot stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error in main loop: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()