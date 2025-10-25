import asyncio
import logging
import aiohttp
from typing import Dict, List, Optional, Any
import time
from src.config_loader import CONFIG

class BinanceIndicators:
    """Binance-based technical indicators client using Binance's klines API."""
    
    def __init__(self):
        self.base_url = "https://api.binance.com"
        self.testnet = CONFIG.get("binance_testnet", "false").lower() == "true"
        
        if self.testnet:
            self.base_url = "https://testnet.binance.vision"
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Make HTTP request to Binance API."""
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(3):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=10) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            raise aiohttp.ClientError(f"HTTP {response.status}: {error_text}")
                        return await response.json()
            except Exception as e:
                if attempt == 2:  # Last attempt
                    raise e
                await asyncio.sleep(0.5 * (2 ** attempt))
                logging.warning(f"Binance indicators request failed (attempt {attempt + 1}/3): {e}")
        
        raise RuntimeError("Max retries exceeded")
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 100) -> List[List]:
        """Get klines data from Binance."""
        try:
            # Clean symbol format - remove quotes and extra characters
            clean_symbol = symbol.strip().strip('"').strip("'").replace("/", "").upper()
            if not clean_symbol.endswith("USDT"):
                clean_symbol = f"{clean_symbol}USDT"
            
            # Clean interval format - remove quotes and extra characters
            clean_interval = interval.strip().strip('"').strip("'")
            
            params = {
                'symbol': clean_symbol,
                'interval': clean_interval,
                'limit': limit
            }
            
            data = await self._make_request('/api/v3/klines', params)
            return data
        except Exception as e:
            logging.error(f"Error getting klines for {symbol}: {e}")
            return []
    
    def calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """Calculate Exponential Moving Average."""
        if len(prices) < period:
            return []
        
        ema_values = []
        multiplier = 2 / (period + 1)
        
        # First EMA is SMA
        sma = sum(prices[:period]) / period
        ema_values.append(sma)
        
        # Calculate subsequent EMAs
        for i in range(period, len(prices)):
            ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
            ema_values.append(ema)
        
        return ema_values
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index."""
        if len(prices) < period + 1:
            return []
        
        rsi_values = []
        gains = []
        losses = []
        
        # Calculate price changes
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        # Calculate initial averages
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        # Calculate RSI
        for i in range(period, len(gains)):
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            rsi_values.append(rsi)
            
            # Update averages
            avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
            avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period
        
        return rsi_values
    
    def calculate_macd(self, prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, List[float]]:
        """Calculate MACD (Moving Average Convergence Divergence)."""
        if len(prices) < slow_period:
            return {"macd": [], "signal": [], "histogram": []}
        
        # Calculate EMAs
        ema_fast = self.calculate_ema(prices, fast_period)
        ema_slow = self.calculate_ema(prices, slow_period)
        
        # Calculate MACD line
        macd_line = []
        min_length = min(len(ema_fast), len(ema_slow))
        
        for i in range(min_length):
            macd_line.append(ema_fast[i] - ema_slow[i])
        
        # Calculate signal line
        signal_line = self.calculate_ema(macd_line, signal_period)
        
        # Calculate histogram
        histogram = []
        min_signal_length = min(len(macd_line), len(signal_line))
        
        for i in range(min_signal_length):
            histogram.append(macd_line[i] - signal_line[i])
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram
        }
    
    def calculate_sma(self, prices: List[float], period: int) -> List[float]:
        """Calculate Simple Moving Average."""
        if len(prices) < period:
            return []
        
        sma_values = []
        for i in range(period - 1, len(prices)):
            sma = sum(prices[i - period + 1:i + 1]) / period
            sma_values.append(sma)
        
        return sma_values
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2) -> Dict[str, List[float]]:
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return {"upper": [], "middle": [], "lower": []}
        
        sma_values = self.calculate_sma(prices, period)
        upper_band = []
        lower_band = []
        
        for i in range(period - 1, len(prices)):
            # Calculate standard deviation
            period_prices = prices[i - period + 1:i + 1]
            mean = sum(period_prices) / len(period_prices)
            variance = sum((x - mean) ** 2 for x in period_prices) / len(period_prices)
            std = (variance ** 0.5)
            
            # Calculate bands
            middle = sma_values[i - period + 1]
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            upper_band.append(upper)
            lower_band.append(lower)
        
        return {
            "upper": upper_band,
            "middle": sma_values,
            "lower": lower_band
        }
    
    async def get_indicators(self, asset: str, interval: str) -> Dict[str, Any]:
        """Get technical indicators for an asset."""
        try:
            # Clean asset name and interval - remove quotes and extra characters
            clean_asset = asset.strip().strip('"').strip("'").upper()
            clean_interval = interval.strip().strip('"').strip("'")
            
            # Get klines data
            klines = await self.get_klines(f"{clean_asset}/USDT", clean_interval, limit=100)
            
            if not klines:
                return {"rsi": None, "macd": None, "sma": None, "ema": None, "bbands": None}
            
            # Extract close prices
            close_prices = [float(kline[4]) for kline in klines]  # Close price is at index 4
            
            # Calculate indicators
            rsi_14 = self.calculate_rsi(close_prices, 14)
            rsi_7 = self.calculate_rsi(close_prices, 7)
            macd_data = self.calculate_macd(close_prices)
            ema_20 = self.calculate_ema(close_prices, 20)
            sma_20 = self.calculate_sma(close_prices, 20)
            bbands = self.calculate_bollinger_bands(close_prices, 20)
            
            return {
                "rsi": rsi_14[-1] if rsi_14 else None,
                "rsi_7": rsi_7[-1] if rsi_7 else None,
                "macd": {
                    "valueMACD": macd_data["macd"][-1] if macd_data["macd"] else None,
                    "valueMACDSignal": macd_data["signal"][-1] if macd_data["signal"] else None,
                    "valueMACDHist": macd_data["histogram"][-1] if macd_data["histogram"] else None
                },
                "sma": sma_20[-1] if sma_20 else None,
                "ema": ema_20[-1] if ema_20 else None,
                "bbands": {
                    "upper": bbands["upper"][-1] if bbands["upper"] else None,
                    "middle": bbands["middle"][-1] if bbands["middle"] else None,
                    "lower": bbands["lower"][-1] if bbands["lower"] else None
                }
            }
        except Exception as e:
            logging.error(f"Error getting indicators for {asset}: {e}")
            return {"rsi": None, "macd": None, "sma": None, "ema": None, "bbands": None}
    
    async def fetch_series(self, indicator: str, symbol: str, interval: str, results: int = 10, params: Dict = None, value_key: str = "value") -> List[float]:
        """Fetch historical series of an indicator."""
        try:
            # Clean symbol and interval - remove quotes and extra characters
            clean_symbol = symbol.strip().strip('"').strip("'")
            clean_interval = interval.strip().strip('"').strip("'")
            
            # Get klines data
            klines = await self.get_klines(clean_symbol, clean_interval, limit=results * 2)  # Get more data for calculations
            
            if not klines:
                return []
            
            # Extract close prices
            close_prices = [float(kline[4]) for kline in klines]
            
            # Calculate indicator based on type
            if indicator.lower() == "ema":
                period = params.get("period", 20) if params else 20
                values = self.calculate_ema(close_prices, period)
            elif indicator.lower() == "rsi":
                period = params.get("period", 14) if params else 14
                values = self.calculate_rsi(close_prices, period)
            elif indicator.lower() == "macd":
                macd_data = self.calculate_macd(close_prices)
                values = macd_data.get("macd", [])
            elif indicator.lower() == "sma":
                period = params.get("period", 20) if params else 20
                values = self.calculate_sma(close_prices, period)
            else:
                return []
            
            # Return the last 'results' values
            return values[-results:] if len(values) >= results else values
            
        except Exception as e:
            logging.error(f"Error fetching series for {indicator}: {e}")
            return []
    
    async def fetch_value(self, indicator: str, symbol: str, interval: str, params: Dict = None, key: str = "value") -> Optional[float]:
        """Fetch single value of an indicator."""
        try:
            series = await self.fetch_series(indicator, symbol, interval, results=1, params=params, value_key=key)
            return series[0] if series else None
        except Exception as e:
            logging.error(f"Error fetching value for {indicator}: {e}")
            return None
    
    def get_historical_indicator(self, indicator: str, symbol: str, interval: str, results: int = 10, params: Dict = None) -> List[Dict[str, Any]]:
        """Get historical indicator data (synchronous wrapper)."""
        try:
            # Run async method synchronously
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, we need to handle this differently
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.fetch_series(indicator, symbol, interval, results, params))
                    values = future.result()
            else:
                values = asyncio.run(self.fetch_series(indicator, symbol, interval, results, params))
            
            # Format as expected by the existing code
            return [{"value": val} for val in values]
        except Exception as e:
            logging.error(f"Error getting historical indicator {indicator}: {e}")
            return []
