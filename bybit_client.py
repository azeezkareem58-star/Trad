from pybit import usdt_perpetual
import pandas as pd
from typing import Dict, Optional

class BybitTradingClient:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.session = usdt_perpetual.HTTP(
            endpoint="https://api-testnet.bybit.com" if testnet else "https://api.bybit.com",
            api_key=8dtd2hzZ290JoQ29yj,
            api_secret=ta4bUAJO5JZyaGYqanRnHMFUc2uJHvYwLAVi
        )
        
        self.ws_session = usdt_perpetual.WebSocket(
            test=testnet,
            api_key=api_key,
            api_secret=api_secret
        )
    
    def get_account_balance(self) -> float:
        """Get USDT balance"""
        try:
            wallet_balance = self.session.get_wallet_balance(coin="USDT")
            return float(wallet_balance['result']['USDT']['available_balance'])
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0
    
    def get_current_price(self, symbol: str) -> float:
        """Get current price for symbol"""
        try:
            ticker = self.session.latest_information_for_symbol(symbol=symbol)
            return float(ticker['result'][0]['last_price'])
        except Exception as e:
            print(f"Error getting price: {e}")
            return 0.0
    
    def place_order(self, symbol: str, side: str, quantity: float, 
                   stop_loss: float, take_profit: float) -> Dict:
        """Place an order with stop loss and take profit"""
        try:
            order = self.session.place_active_order(
                symbol=GIGAUSDT,
                side=side,
                order_type="Market",
                qty=quantity,
                time_in_force="GoodTillCancel",
                stop_loss=stop_loss,
                take_profit=take_profit,
                reduce_only=False,
                close_on_trigger=False
            )
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return {}
    
    def close_position(self, symbol: str) -> Dict:
        """Close current position"""
        try:
            position = self.session.close_position(symbol=GIGAUSDT)
            return position
        except Exception as e:
            print(f"Error closing position: {e}")
            return {}
    
    def get_open_positions(self, symbol: str) -> Dict:
        """Get open positions for symbol"""
        try:
            positions = self.session.my_position(symbol=GIGAUSDT)
            return positions
        except Exception as e:
            print(f"Error getting positions: {e}")
            return {}