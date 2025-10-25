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
        self.futures_enabled = CONFIG.get("binance_futures_enabled", "false").lower() == "true"
        self.futures_leverage = float(CONFIG.get("binance_futures_leverage", "5.0"))
        self.futures_margin_type = CONFIG.get("binance_futures_margin_type", "ISOLATED")
        
        if not self.api_key or not self.secret_key:
            raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be provided")
        
        # Choose base URL based on testnet setting
        if self.testnet:
            self.base_url = "https://testnet.binance.vision"
            self.futures_base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://api.binance.com"
            self.futures_base_url = "https://fapi.binance.com"
        
        self.ws_url = "wss://testnet.binance.vision/ws" if self.testnet else "wss://stream.binance.com:9443/ws"
        self.futures_ws_url = "wss://testnet.binancefuture.com/ws" if self.testnet else "wss://fstream.binance.com/ws"
        
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
    
    async def _make_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False, use_futures: bool = False) -> Dict[str, Any]:
        """Make HTTP request to Binance API with retry logic."""
        if params is None:
            params = {}
        
        # Add timestamp for signed requests
        if signed:
            params['timestamp'] = int(time.time() * 1000)
        
        # Generate signature for signed requests
        if signed:
            query_string = urlencode(params, doseq=True)
            signature = self._generate_signature(query_string)
            params['signature'] = signature
        
        headers = self._get_headers()
        base_url = self.futures_base_url if use_futures else self.base_url
        url = f"{base_url}{endpoint}"
        
        for attempt in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    if method.upper() == 'GET':
                        async with session.get(url, params=params, headers=headers, timeout=10) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise aiohttp.ClientError(f"HTTP {response.status}: {error_text}")
                            data = await response.json()
                    elif method.upper() == 'POST':
                        # Binance POST requests use form data, not JSON
                        async with session.post(url, data=params, headers=headers, timeout=10) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise aiohttp.ClientError(f"HTTP {response.status}: {error_text}")
                            data = await response.json()
                    elif method.upper() == 'DELETE':
                        async with session.delete(url, params=params, headers=headers, timeout=10) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                raise aiohttp.ClientError(f"HTTP {response.status}: {error_text}")
                            data = await response.json()
                    
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
            # Get spot account information
            account_info = await self._make_request('GET', '/api/v3/account', signed=True)
            
            # Calculate total balance from all assets
            balance = 0.0
            positions = []
            
            # Process spot balances
            for balance_info in account_info.get('balances', []):
                asset = balance_info.get('asset', '')
                free = float(balance_info.get('free', 0.0))
                locked = float(balance_info.get('locked', 0.0))
                total = free + locked
                
                if total > 0:
                    if asset == 'USDT':
                        balance += total
                    else:
                        # For non-USDT assets, we'll treat them as positions
                        # In a real implementation, you'd convert to USDT value
                        pos_data = {
                            'coin': asset,
                            'szi': total,
                            'entryPx': 0.0,  # Would need to track entry price
                            'leverage': 1.0,
                            'pnl': 0.0,  # Would need to calculate PnL
                            'liquidationPx': 0.0
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
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            data = await self._make_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
            return float(data.get('price', 0.0))
        except Exception as e:
            logging.error(f"Error getting current price for {asset}: {e}")
            return 0.0
    
    async def place_buy_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a buy order."""
        try:
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            
            # Get current price to determine if we should use quantity or quoteOrderQty
            current_price = await self.get_current_price(asset)
            order_value = amount * current_price
            
            # Use quoteOrderQty for small amounts to avoid LOT_SIZE errors
            if order_value < 10.0:  # If order value is less than $10, use quoteOrderQty
                params = {
                    'symbol': symbol,
                    'side': 'BUY',
                    'type': 'MARKET',
                    'quoteOrderQty': str(round(order_value, 2))  # Use dollar amount
                }
                logging.info(f"Using quoteOrderQty for {asset}: ${order_value:.2f}")
            else:
                quantity = await self.round_size_async(asset, amount)
                params = {
                    'symbol': symbol,
                    'side': 'BUY',
                    'type': 'MARKET',
                    'quantity': str(quantity)
                }
                logging.info(f"Using quantity for {asset}: {quantity} (order value: ${order_value:.2f})")
            
            # Log the exact parameters being sent
            logging.info(f"Order parameters for {asset}: {params}")
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'filled': {'oid': str(result.get('orderId'))}}]}}}
        except Exception as e:
            logging.error(f"Error placing buy order for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_sell_order(self, asset: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Place a sell order."""
        try:
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            
            # Get current price to determine if we should use quantity or quoteOrderQty
            current_price = await self.get_current_price(asset)
            order_value = amount * current_price
            
            # Use quoteOrderQty for small amounts to avoid LOT_SIZE errors
            if order_value < 10.0:  # If order value is less than $10, use quoteOrderQty
                params = {
                    'symbol': symbol,
                    'side': 'SELL',
                    'type': 'MARKET',
                    'quoteOrderQty': str(round(order_value, 2))  # Use dollar amount
                }
                logging.info(f"Using quoteOrderQty for {asset}: ${order_value:.2f}")
            else:
                quantity = await self.round_size_async(asset, amount)
                params = {
                    'symbol': symbol,
                    'side': 'SELL',
                    'type': 'MARKET',
                    'quantity': str(quantity)
                }
                logging.info(f"Using quantity for {asset}: {quantity} (order value: ${order_value:.2f})")
            
            # Log the exact parameters being sent
            logging.info(f"Order parameters for {asset}: {params}")
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'filled': {'oid': str(result.get('orderId'))}}]}}}
        except Exception as e:
            logging.error(f"Error placing sell order for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_take_profit(self, asset: str, is_buy: bool, amount: float, tp_price: float) -> Dict[str, Any]:
        """Place a take profit order."""
        try:
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            quantity = await self.round_size_async(asset, amount)
            side = 'SELL' if is_buy else 'BUY'
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': str(quantity),
                'price': str(tp_price),
                'timeInForce': 'GTC'
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'resting': {'oid': str(result.get('orderId'))}}]}}}
        except Exception as e:
            logging.error(f"Error placing take profit for {asset}: {e}")
            return {'error': str(e)}
    
    async def place_stop_loss(self, asset: str, is_buy: bool, amount: float, sl_price: float) -> Dict[str, Any]:
        """Place a stop loss order."""
        try:
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            quantity = await self.round_size_async(asset, amount)
            side = 'SELL' if is_buy else 'BUY'
            
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'STOP_LOSS_LIMIT',
                'quantity': str(quantity),
                'price': str(sl_price),
                'stopPrice': str(sl_price),
                'timeInForce': 'GTC'
            }
            
            result = await self._make_request('POST', '/api/v3/order', params, signed=True)
            return {'response': {'data': {'statuses': [{'resting': {'oid': str(result.get('orderId'))}}]}}}
        except Exception as e:
            logging.error(f"Error placing stop loss for {asset}: {e}")
            return {'error': str(e)}
    
    async def cancel_order(self, asset: str, order_id: str) -> Dict[str, Any]:
        """Cancel a specific order."""
        try:
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
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
            # Clean asset name and format symbol properly - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
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
            # For spot trading, we need to get trades for all symbols
            # This is a simplified approach - in production you might want to get trades for specific symbols
            fills = await self._make_request('GET', '/api/v3/account', signed=True)
            
            # Get recent trades from account info
            normalized_fills = []
            
            # For spot trading, we don't have a direct "recent fills" endpoint
            # We'll return empty list for now - this would need to be implemented differently
            # based on your specific needs (e.g., track trades in a database)
            
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
        """Get open interest for an asset."""
        if not self.futures_enabled:
            return None
        
        try:
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            data = await self._make_request('GET', '/fapi/v1/openInterest', {'symbol': symbol}, use_futures=True)
            return float(data.get('openInterest', 0.0))
        except Exception as e:
            logging.error(f"Error getting open interest for {asset}: {e}")
            return None
    
    async def get_funding_rate(self, asset: str) -> Optional[float]:
        """Get funding rate for an asset."""
        if not self.futures_enabled:
            return None
        
        try:
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            data = await self._make_request('GET', '/fapi/v1/premiumIndex', {'symbol': symbol}, use_futures=True)
            return float(data.get('lastFundingRate', 0.0))
        except Exception as e:
            logging.error(f"Error getting funding rate for {asset}: {e}")
            return None
    
    async def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information including lot size rules."""
        try:
            exchange_info = await self._make_request('GET', '/api/v3/exchangeInfo')
            symbols = exchange_info.get('symbols', [])
            
            for symbol_info in symbols:
                if symbol_info.get('symbol') == symbol:
                    return symbol_info
            return {}
        except Exception as e:
            logging.error(f"Error getting symbol info for {symbol}: {e}")
            return {}
    
    def round_size(self, asset: str, amount: float) -> float:
        """Round amount to asset's precision using hardcoded rules."""
        # Clean asset name
        clean_asset = asset.strip().strip('"').strip("'").upper()
        
        # Use the same precision fix logic as the async version
        return self._apply_precision_fix(clean_asset, amount)
    
    async def round_size_async(self, asset: str, amount: float) -> float:
        """Round amount to asset's precision using live symbol info."""
        try:
            # Clean asset name
            clean_asset = asset.strip().strip('"').strip("'").upper()
            symbol = f"{clean_asset}USDT"
            
            # Get symbol info
            symbol_info = await self.get_symbol_info(symbol)
            
            if symbol_info:
                # Extract lot size filter
                lot_size_filter = None
                for filter_info in symbol_info.get('filters', []):
                    if filter_info.get('filterType') == 'LOT_SIZE':
                        lot_size_filter = filter_info
                        break
                
                if lot_size_filter:
                    step_size = float(lot_size_filter.get('stepSize', '0.00001'))
                    min_qty = float(lot_size_filter.get('minQty', '0.00001'))
                    
                    # Round to the appropriate step size
                    rounded = round(amount / step_size) * step_size
                    rounded = max(rounded, min_qty)
                else:
                    # Fallback to hardcoded precision
                    rounded = self._apply_precision_fix(clean_asset, amount)
            else:
                # Fallback to hardcoded precision if symbol info not available
                rounded = self._apply_precision_fix(clean_asset, amount)
            
            return rounded
            
        except Exception as e:
            logging.error(f"Error rounding size for {asset}: {e}")
            # Fallback to hardcoded precision
            return self._apply_precision_fix(clean_asset, amount)
    
    def _apply_precision_fix(self, clean_asset: str, amount: float) -> float:
        """Apply precision fix based on asset type."""
        # Fallback to hardcoded step sizes for major assets
        step_sizes = {
            'BTC': 0.00001,   # 5 decimal places
            'ETH': 0.0001,    # 4 decimal places
            'SOL': 0.001,     # 3 decimal places
            'BNB': 0.001,     # 3 decimal places
            'ZEC': 0.001,     # 3 decimal places
            'XRP': 0.1,       # 1 decimal place
            'DOGE': 1.0,      # 0 decimal places
            'EIGEN': 0.01,    # 2 decimal places
        }
        
        step_size = step_sizes.get(clean_asset, 0.00001)
        
        # Round to the appropriate step size
        rounded = round(amount / step_size) * step_size
        
        # Additional precision fix: round to the appropriate number of decimal places
        if clean_asset == 'BTC':
            # BTC: 5 decimal places
            rounded = round(rounded, 5)
        elif clean_asset == 'ETH':
            # ETH: 4 decimal places
            rounded = round(rounded, 4)
        elif clean_asset in ['SOL', 'BNB', 'ZEC']:
            # SOL, BNB, ZEC: 3 decimal places
            rounded = round(rounded, 3)
        elif clean_asset == 'XRP':
            # XRP: 1 decimal place
            rounded = round(rounded, 1)
        elif clean_asset == 'DOGE':
            # DOGE: 0 decimal places
            rounded = round(rounded, 0)
        elif clean_asset == 'EIGEN':
            # EIGEN: 2 decimal places
            rounded = round(rounded, 2)
        else:
            # Default: 8 decimal places
            rounded = round(rounded, 8)
        
        return max(rounded, step_size)
    
    # Futures-specific methods
    async def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """Set leverage for a futures symbol."""
        if not self.futures_enabled:
            return {'error': 'Futures trading not enabled'}
        
        try:
            params = {
                'symbol': symbol,
                'leverage': leverage
            }
            result = await self._make_request('POST', '/fapi/v1/leverage', params, signed=True, use_futures=True)
            return result
        except Exception as e:
            logging.error(f"Error setting leverage for {symbol}: {e}")
            return {'error': str(e)}
    
    async def set_margin_type(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        """Set margin type for a futures symbol."""
        if not self.futures_enabled:
            return {'error': 'Futures trading not enabled'}
        
        try:
            params = {
                'symbol': symbol,
                'marginType': margin_type
            }
            result = await self._make_request('POST', '/fapi/v1/marginType', params, signed=True, use_futures=True)
            return result
        except Exception as e:
            logging.error(f"Error setting margin type for {symbol}: {e}")
            return {'error': str(e)}
    
    async def get_position_info(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get position information for futures."""
        if not self.futures_enabled:
            return []
        
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            result = await self._make_request('GET', '/fapi/v2/positionRisk', params, signed=True, use_futures=True)
            return result if isinstance(result, list) else []
        except Exception as e:
            logging.error(f"Error getting position info: {e}")
            return []
    
    async def get_futures_account_info(self) -> Dict[str, Any]:
        """Get futures account information."""
        if not self.futures_enabled:
            return {'error': 'Futures trading not enabled'}
        
        try:
            result = await self._make_request('GET', '/fapi/v2/account', signed=True, use_futures=True)
            return result
        except Exception as e:
            logging.error(f"Error getting futures account info: {e}")
            return {'error': str(e)}
