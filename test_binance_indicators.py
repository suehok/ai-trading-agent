#!/usr/bin/env python3
"""
Test script for Binance indicators
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.indicators.binance_indicators import BinanceIndicators

async def test_binance_indicators():
    """Test Binance indicators functionality."""
    print("Testing Binance Indicators...")
    
    try:
        # Initialize indicators client
        indicators = BinanceIndicators()
        print("✅ Binance Indicators initialized")
        
        # Test getting klines data
        print("Testing get_klines...")
        klines = await indicators.get_klines("BTCUSDT", "5m", limit=20)
        print(f"✅ Got {len(klines)} klines for BTCUSDT")
        
        # Test getting indicators
        print("Testing get_indicators...")
        indicators_data = await indicators.get_indicators("BTC", "5m")
        print(f"✅ Got indicators: RSI={indicators_data.get('rsi')}, EMA={indicators_data.get('ema')}")
        
        # Test fetching series
        print("Testing fetch_series...")
        ema_series = await indicators.fetch_series("ema", "BTC/USDT", "5m", results=5, params={"period": 20})
        print(f"✅ Got EMA series: {len(ema_series)} values")
        
        # Test fetching single value
        print("Testing fetch_value...")
        rsi_value = await indicators.fetch_value("rsi", "BTC/USDT", "5m", params={"period": 14})
        print(f"✅ Got RSI value: {rsi_value}")
        
        print("🎉 All Binance indicators tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_binance_indicators())
