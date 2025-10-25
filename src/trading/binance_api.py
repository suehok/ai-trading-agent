import asyncio
import logging
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import hmac
import hashlib
import time
import json
from urllib.parse import urlencode
from src.config_loader import CONFIG
from src.trading.base_trading_api import BaseTradingAPI

class BinanceAPI(BaseTradingAPI):
    """Binance API client implementing the BaseTradingAPI interface."""
    
    def __init__(self):
        self.api_key = CONFIG.get("binance_api_key")
        self.secret_key = CONFIG.get("binance_secret_key")
        self.testnet = CONFIG.get("binance_testnet", "false").lower() == "true"
        
        if not self.api_key or not self.secret_key:
            raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be provided")
        
        # Choose base URL based on testnet setting
        if self.testnet:
            self.base_url = "https://testnet.binance.vision"
        else:
            self.base_url = "https://api.binance.com"
        
        self.ws_url = "wss://testnet.binance.vision/ws" if self.testnet else "wss://stream.binance.com:9443/ws"
        
    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature for Binance API."""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _get_headers(self, signature: str = None) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        }
        if signature:
            headers['X-MBX-SIGNATURE'] = signature
        return headers
    
    async def _make_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False) -> Dict[str, Any]:
        """Make HTTP request to Binance API with retry logic."""
        if params is None:
            params = {}
        
        # Add timestamp for signed requests
        if signed:
            params['timestamp'] = int(time.time() * 1000)
        
        # Generate signature for signed requests
        if signed:
            query_string = urlencode(params)
            signature = self._generate_signature(query_string)
            headers = self._get_headers(signature)
        else:
            headers = self._get_headers()
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    if method.upper() == 'GET':
                        async with session.get(url, params=params, headers=headers, timeout=10) as response:
                            data = await response.json()
                    elif method.upper() == 'POST':
                        async with session.post(url, data=params, headers=headers, timeout=10) as response:
                            data = await response.json()
                    elif method.upper() == 'DELETE':
                        async with session.delete(url, params=params, headers=headers, timeout=10) as response:
                            data = await response.json()
                    
                    if response.status != 200:
                        raise aiohttp.ClientError(f"HTTP {response.status}: {data}")
                    
                    return data
                    
            except Exception as e:
                if attempt == 2:  # Last attempt
                    raise e
                await asyncio.sleep(0.5 * (2 ** attempt))
                logging.warning(f"Binance API request failed (attempt {attempt + 1}/3): {e}")
        
        raise RuntimeError("Max retries exceeded")
    
    async def get_user_state(self) -> Dict[str, Any]:
        """Get user account state including balance and positions."""
        try:
            # Get account information
            account_info = await self._make_request('GET', '/api/v3/account', signed=True)
            
            # Get futures account info for positions
            futures_account = await self._make_request('GET', '/fapi/v2/account', signed=True)
            
            balance = float(account_info.get('totalWalletBalance', 0.0))
            positions = []
            
            # Process futures positions
            for position in futures_account.get('positions', []):
                if float(position.get('positionAmt', 0)) != 0:
                    pos_data = {
                        'coin': position.get('symbol', '').replace('USDT', ''),
                        'szi': float(position.get('positionAmt', 0)),
                        'entryPx': float(position.get('avgPrice', 0)),
                        'leverage': float(position.get('leverage', 1)),
                        'pnl': float(position.get('unrealizedPnl', 0)),
                        'liquidationPx': float(position.get('liquidationPrice', 0))
                    }
                    positions.append(pos_data)
            
            return {
                'balance': balance,
                'positions': positions
            }
        except Exception as e:
            logging.error(f"Error getting user state: {e}")
            return {'balance': 0.0, 'positions': []}
    
    async def get_current_price(self, asset: str) -> float:
        """Get current price for an asset."""
        try:
            symbol = f"{asset}USDT"
            data = await self._make_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
            return float(data.get('price', 0.0))
        except Exception as e:
            logging.error(f"Error getting current price for {asset}: {e}")
            return 0.0
    
    async def place_buy_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a buy order."""
        try:
            symbol = f"{asset}USDT"
            quantity = self.round_size(asset, amount)
            
            params = {
                'symbol': symbol,
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': quantity
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'filled': {'oid': result.get('orderId')}}]}}}
        except Exception as e:
            logging.error(f"Error placing buy order for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_sell_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a sell order."""
        try:
            symbol = f"{asset}USDT"
            quantity = self.round_size(asset, amount)
            
            params = {
                'symbol': symbol,
                'side': 'SELL',
                'type': 'MARKET',
                'quantity': quantity
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'filled': {'oid': result.get('orderId')}}]}}}
        except Exception as e:
            logging.error(f"Error placing sell order for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_take_profit(self, asset: str, is_buy: bool, amount: float, tp_price: float) -> Dict[str, Any]:
        """Place a take profit order."""
        try:
            symbol = f"{asset}USDT"
            quantity = self.round_size(asset, amount)
            side = 'SELL' if is_buy else 'BUY'
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': tp_price,
                'timeInForce': 'GTC'
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'resting': {'oid': result.get('orderId')}}]}}}
        except Exception as e:
            logging.error(f"Error placing take profit for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_stop_loss(self, asset: str, is_buy: bool, amount: float, sl_price: float) -> Dict[str, Any]:
        """Place a stop loss order."""
        try:
            symbol = f"{asset}USDT"
            quantity = self.round_size(asset, amount)
            side = 'SELL' if is_buy else 'BUY'
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'STOP_MARKET',
                'quantity': quantity,
                'stopPrice': sl_price
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'resting': {'oid': result.get('orderId')}}]}}}
        except Exception as e:
            logging.error(f"Error placing stop loss for {asset}: {e}")
            return {'error': str(e)}
    
    async def cancel_order(self, asset: str, order_id: str) -> Dict[str, Any]:
        """Cancel a specific order."""
        try:
            symbol = f"{asset}USDT"
            params = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            result = await self._make_request('DELETE', '/api/v3/order', params, signed=True)
            return result
        except Exception as e:
            logging.error(f"Error canceling order {order_id} for {asset}: {e}")
            return {'error': str(e)}
    
    async def cancel_all_orders(self, asset: str) -> Dict[str, Any]:
        """Cancel all orders for an asset."""
        try:
            symbol = f"{asset}USDT"
            params = {'symbol': symbol}
            
            result = await self._make_request('DELETE', '/api/v3/openOrders', params, signed=True)
            return {'status': 'ok', 'cancelled_count': len(result)}
        except Exception as e:
            logging.error(f"Error canceling all orders for {asset}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_open_orders(self) -> List[Dict[str, Any]]:
        """Get all open orders."""
        try:
            orders = await self._make_request('GET', '/api/v3/openOrders', signed=True)
            normalized_orders = []
            
            for order in orders:
                normalized_order = {
                    'coin': order.get('symbol', '').replace('USDT', ''),
                    'oid': str(order.get('orderId')),
                    'isBuy': order.get('side') == 'BUY',
                    'sz': float(order.get('origQty', 0)),
                    'px': float(order.get('price', 0)) if order.get('price') else None,
                    'orderType': order.get('type'),
                    'triggerPx': float(order.get('stopPrice', 0)) if order.get('stopPrice') else None
                }
                normalized_orders.append(normalized_order)
            
            return normalized_orders
        except Exception as e:
            logging.error(f"Error getting open orders: {e}")
            return []
    
    async def get_recent_fills(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent fills/trades."""
        try:
            fills = await self._make_request('GET', '/api/v3/myTrades', {'limit': limit}, signed=True)
            normalized_fills = []
            
            for fill in fills:
                normalized_fill = {
                    'coin': fill.get('symbol', '').replace('USDT', ''),
                    'asset': fill.get('symbol', '').replace('USDT', ''),
                    'isBuy': fill.get('isBuyer'),
                    'sz': float(fill.get('qty', 0)),
                    'size': float(fill.get('qty', 0)),
                    'px': float(fill.get('price', 0)),
                    'price': float(fill.get('price', 0)),
                    'time': fill.get('time'),
                    'timestamp': fill.get('time')
                }
                normalized_fills.append(normalized_fill)
            
            return normalized_fills
        except Exception as e:
            logging.error(f"Error getting recent fills: {e}")
            return []
    
    def extract_oids(self, order_result: Dict[str, Any]) -> List[str]:
        """Extract order IDs from order result."""
        oids = []
        try:
            if 'response' in order_result and 'data' in order_result['response']:
                statuses = order_result['response']['data'].get('statuses', [])
                for status in statuses:
                    if 'resting' in status and 'oid' in status['resting']:
                        oids.append(status['resting']['oid'])
                    if 'filled' in status and 'oid' in status['filled']:
                        oids.append(status['filled']['oid'])
        except Exception:
            pass
        return oids
    
    async def get_open_interest(self, asset: str) -> Optional[float]:
        """Get open interest for an asset (Binance futures only)."""
        try:
            symbol = f"{asset}USDT"
            data = await self._make_request('GET', '/fapi/v1/openInterest', {'symbol': symbol})
            return float(data.get('openInterest', 0))
        except Exception as e:
            logging.error(f"Error getting open interest for {asset}: {e}")
            return None
    
    async def get_funding_rate(self, asset: str) -> Optional[float]:
        """Get funding rate for an asset (Binance futures only)."""
        try:
            symbol = f"{asset}USDT"
            data = await self._make_request('GET', '/fapi/v1/premiumIndex', {'symbol': symbol})
            return float(data.get('lastFundingRate', 0))
        except Exception as e:
            logging.error(f"Error getting funding rate for {asset}: {e}")
            return None
    
    def round_size(self, asset: str, amount: float) -> float:
        """Round amount to asset's precision."""
        # Binance typically uses 8 decimal places for most assets
        # This is a simplified implementation - in production, you'd fetch
        # the actual precision from the exchange info endpoint
        return round(amount, 8)
