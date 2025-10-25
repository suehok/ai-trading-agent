from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import asyncio

class BaseTradingAPI(ABC):
    """Abstract base class for trading platform APIs."""
    
    @abstractmethod
    async def get_user_state(self) -> Dict[str, Any]:
        """Get user account state including balance and positions."""
        pass
    
    @abstractmethod
    async def get_current_price(self, asset: str) -> float:
        """Get current price for an asset."""
        pass
    
    @abstractmethod
    async def place_buy_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a buy order."""
        pass
    
    @abstractmethod
    async def place_sell_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a sell order."""
        pass
    
    @abstractmethod
    async def place_take_profit(self, asset: str, is_buy: bool, amount: float, tp_price: float) -> Dict[str, Any]:
        """Place a take profit order."""
        pass
    
    @abstractmethod
    async def place_stop_loss(self, asset: str, is_buy: bool, amount: float, sl_price: float) -> Dict[str, Any]:
        """Place a stop loss order."""
        pass
    
    @abstractmethod
    async def cancel_order(self, asset: str, order_id: str) -> Dict[str, Any]:
        """Cancel a specific order."""
        pass
    
    @abstractmethod
    async def cancel_all_orders(self, asset: str) -> Dict[str, Any]:
        """Cancel all orders for an asset."""
        pass
    
    @abstractmethod
    async def get_open_orders(self) -> List[Dict[str, Any]]:
        """Get all open orders."""
        pass
    
    @abstractmethod
    async def get_recent_fills(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent fills/trades."""
        pass
    
    @abstractmethod
    def extract_oids(self, order_result: Dict[str, Any]) -> List[str]:
        """Extract order IDs from order result."""
        pass
    
    @abstractmethod
    async def get_open_interest(self, asset: str) -> Optional[float]:
        """Get open interest for an asset (if supported)."""
        pass
    
    @abstractmethod
    async def get_funding_rate(self, asset: str) -> Optional[float]:
        """Get funding rate for an asset (if supported)."""
        pass
    
    @abstractmethod
    def round_size(self, asset: str, amount: float) -> float:
        """Round amount to asset's precision."""
        pass
