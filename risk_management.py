import math
from typing import Dict, Tuple

class RiskManager:
    def __init__(self, max_risk_per_trade: float, max_position_size: float):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_position_size = max_position_size
        
    def calculate_position_size(self, current_price: float, account_balance: float, 
                              stop_loss_price: float) -> Tuple[float, float]:
        """
        Calculate position size based on risk parameters
        Returns: (position_size, quantity)
        """
        # Calculate risk per unit
        price_diff = abs(current_price - stop_loss_price)
        risk_per_unit = price_diff / current_price
        
        if risk_per_unit == 0:
            return 0, 0
            
        # Maximum capital to risk
        max_risk_capital = account_balance * self.max_risk_per_trade
        
        # Calculate position value based on risk
        position_value_risk = max_risk_capital / risk_per_unit
        
        # Calculate position value based on maximum position size
        position_value_size = account_balance * self.max_position_size
        
        # Use the smaller of the two
        position_value = min(position_value_risk, position_value_size)
        
        # Calculate quantity
        quantity = position_value / current_price
        
        return position_value, quantity
    
    def validate_trade(self, quantity: float, current_price: float, account_balance: float) -> bool:
        """Validate if trade meets risk criteria"""
        position_value = quantity * current_price
        
        # Check if position size exceeds maximum
        if position_value > account_balance * self.max_position_size:
            return False
            
        # Check if risk exceeds maximum
        potential_loss = position_value * self.max_risk_per_trade
        if potential_loss > account_balance * self.max_risk_per_trade:
            return False
            
        return True
    
    def calculate_stop_loss_take_profit(self, entry_price: float, direction: str) -> Tuple[float, float]:
        """Calculate stop loss and take profit levels"""
        if direction == "long":
            stop_loss = entry_price * (1 - STOP_LOSS_PERCENTAGE)
            take_profit = entry_price * (1 + TAKE_PROFIT_PERCENTAGE)
        else:  # short
            stop_loss = entry_price * (1 + STOP_LOSS_PERCENTAGE)
            take_profit = entry_price * (1 - TAKE_PROFIT_PERCENTAGE)
            
        return stop_loss, take_profit