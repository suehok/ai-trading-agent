import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
from src.config_loader import CONFIG

class RiskManager:
    """Comprehensive risk management system for fund limits and position sizing."""
    
    def __init__(self):
        # Fund limits from configuration
        self.max_total_allocation = float(CONFIG.get("max_total_allocation", 1000.0))  # Maximum total USD allocation
        self.max_single_position = float(CONFIG.get("max_single_position", 500.0))     # Maximum single position size
        self.max_daily_loss = float(CONFIG.get("max_daily_loss", 100.0))               # Maximum daily loss limit
        self.max_leverage = float(CONFIG.get("max_leverage", 5.0))                     # Maximum leverage allowed
        self.min_position_size = float(CONFIG.get("min_position_size", 10.0))          # Minimum position size
        
        # Risk tracking
        self.daily_pnl = 0.0
        self.daily_reset_time = None
        self.total_allocated = 0.0
        self.position_count = 0
        
        # Circuit breakers
        self.max_consecutive_losses = int(CONFIG.get("max_consecutive_losses", 3))
        self.consecutive_losses = 0
        self.circuit_breaker_active = False
        
        logging.info(f"Risk Manager initialized with limits: "
                    f"Max Total: ${self.max_total_allocation}, "
                    f"Max Single: ${self.max_single_position}, "
                    f"Max Daily Loss: ${self.max_daily_loss}, "
                    f"Max Leverage: {self.max_leverage}x")
    
    def reset_daily_tracking(self):
        """Reset daily tracking at start of new day."""
        current_time = datetime.now(timezone.utc)
        if self.daily_reset_time is None or current_time.date() > self.daily_reset_time.date():
            self.daily_pnl = 0.0
            self.daily_reset_time = current_time
            self.consecutive_losses = 0
            self.circuit_breaker_active = False
            logging.info("Daily risk tracking reset")
    
    def update_daily_pnl(self, pnl: float):
        """Update daily PnL and check daily loss limit."""
        self.daily_pnl += pnl
        logging.info(f"Daily PnL updated: {self.daily_pnl:.2f}")
        
        if self.daily_pnl <= -self.max_daily_loss:
            logging.warning(f"Daily loss limit reached: {self.daily_pnl:.2f} <= -{self.max_daily_loss}")
            return False
        return True
    
    def update_consecutive_losses(self, is_loss: bool):
        """Track consecutive losses for circuit breaker."""
        if is_loss:
            self.consecutive_losses += 1
            if self.consecutive_losses >= self.max_consecutive_losses:
                self.circuit_breaker_active = True
                logging.warning(f"Circuit breaker activated: {self.consecutive_losses} consecutive losses")
        else:
            self.consecutive_losses = 0
            self.circuit_breaker_active = False
    
    def validate_allocation(self, allocation_usd: float, current_balance: float, 
                          existing_positions: List[Dict], asset: str) -> Tuple[bool, str, float]:
        """
        Validate if allocation is within risk limits.
        
        Returns:
            (is_valid, reason, adjusted_allocation)
        """
        self.reset_daily_tracking()
        
        # Check circuit breaker
        if self.circuit_breaker_active:
            return False, "Circuit breaker active - too many consecutive losses", 0.0
        
        # Check daily loss limit
        if not self.update_daily_pnl(0):  # Just check, don't update
            return False, "Daily loss limit exceeded", 0.0
        
        # Check minimum position size
        if allocation_usd < self.min_position_size:
            return False, f"Allocation too small (${allocation_usd:.2f} < ${self.min_position_size})", 0.0
        
        # Check maximum single position
        if allocation_usd > self.max_single_position:
            adjusted_allocation = self.max_single_position
            logging.warning(f"Allocation capped to max single position: ${adjusted_allocation}")
            return True, "Allocation capped to max single position", adjusted_allocation
        
        # Calculate current total allocation
        current_total = sum(abs(pos.get('szi', 0)) * pos.get('entryPx', 0) for pos in existing_positions)
        
        # Check if adding this allocation would exceed total limit
        new_total = current_total + allocation_usd
        if new_total > self.max_total_allocation:
            remaining_capacity = self.max_total_allocation - current_total
            if remaining_capacity < self.min_position_size:
                return False, "No remaining allocation capacity", 0.0
            else:
                adjusted_allocation = remaining_capacity
                logging.warning(f"Allocation reduced to fit total limit: ${adjusted_allocation}")
                return True, "Allocation reduced to fit total limit", adjusted_allocation
        
        # Check leverage limits
        effective_leverage = new_total / current_balance if current_balance > 0 else 0
        if effective_leverage > self.max_leverage:
            max_allocation_by_leverage = current_balance * self.max_leverage - current_total
            if max_allocation_by_leverage < self.min_position_size:
                return False, "Leverage limit would be exceeded", 0.0
            else:
                adjusted_allocation = max_allocation_by_leverage
                logging.warning(f"Allocation reduced due to leverage limit: ${adjusted_allocation}")
                return True, "Allocation reduced due to leverage limit", adjusted_allocation
        
        # Check if we have sufficient balance for this allocation
        if allocation_usd > current_balance:
            # Calculate maximum allocation we can afford
            max_allocation_by_balance = current_balance
            
            # Check if the maximum allocation meets minimum position size
            if max_allocation_by_balance < self.min_position_size:
                return False, f"Insufficient balance for minimum position size (need ${self.min_position_size:.2f}, have ${current_balance:.2f})", 0.0
            
            # Adjust allocation to what we can afford
            adjusted_allocation = max_allocation_by_balance
            logging.warning(f"Allocation reduced due to insufficient balance: ${allocation_usd:.2f} -> ${adjusted_allocation:.2f}")
            return True, "Allocation reduced due to insufficient balance", adjusted_allocation
        
        return True, "Allocation approved", allocation_usd
    
    def validate_position_sizing(self, asset: str, amount: float, price: float, 
                               is_buy: bool, current_balance: float) -> Tuple[bool, str, float]:
        """
        Validate position sizing for a specific trade.
        
        Returns:
            (is_valid, reason, adjusted_amount)
        """
        allocation_usd = amount * price
        
        # Basic validation
        if amount <= 0:
            return False, "Invalid position size", 0.0
        
        if price <= 0:
            return False, "Invalid price", 0.0
        
        # Check if we have sufficient balance (for spot trading, no leverage)
        if allocation_usd > current_balance:
            # Calculate maximum amount we can afford
            max_amount = current_balance / price
            
            # Check if the maximum amount meets minimum position size
            if max_amount * price < self.min_position_size:
                return False, f"Insufficient balance for minimum position size (need ${self.min_position_size:.2f}, have ${current_balance:.2f})", 0.0
            
            # Adjust amount to what we can afford
            adjusted_amount = max_amount
            logging.warning(f"Position size adjusted due to insufficient balance: {amount:.4f} -> {adjusted_amount:.4f} (${allocation_usd:.2f} -> ${current_balance:.2f})")
            return True, "Position size adjusted due to insufficient balance", adjusted_amount
        
        return True, "Position size approved", amount
    
    def get_risk_summary(self) -> Dict:
        """Get current risk management summary."""
        return {
            "max_total_allocation": self.max_total_allocation,
            "max_single_position": self.max_single_position,
            "max_daily_loss": self.max_daily_loss,
            "max_leverage": self.max_leverage,
            "min_position_size": self.min_position_size,
            "daily_pnl": self.daily_pnl,
            "consecutive_losses": self.consecutive_losses,
            "circuit_breaker_active": self.circuit_breaker_active,
            "total_allocated": self.total_allocated
        }
    
    def log_risk_event(self, event_type: str, details: str):
        """Log risk management events."""
        logging.info(f"RISK EVENT [{event_type}]: {details}")
    
    def emergency_stop(self, reason: str):
        """Emergency stop all trading."""
        self.circuit_breaker_active = True
        logging.critical(f"EMERGENCY STOP: {reason}")
