#!/usr/bin/env python3
"""
Test script to verify symbol and interval cleaning fixes
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.indicators.binance_indicators import BinanceIndicators
from src.trading.binance_api import BinanceAPI

async def test_symbol_cleaning():
    """Test that symbols and intervals are properly cleaned."""
    print("Testing Symbol and Interval Cleaning...")
    
    try:
        # Test indicators client
        print("Testing Binance Indicators...")
        indicators = BinanceIndicators()
        
        # Test with quoted symbols and intervals
        test_cases = [
            ('"BTC"', '"5m"'),
            ("'ETH'", "'1h'"),
            ('"SOL"', '"4h"'),
            ('BTC', '5m'),  # Clean cases
            ('ETH', '1h')
        ]
        
        for asset, interval in test_cases:
            print(f"Testing asset: {asset}, interval: {interval}")
            
            # Test get_indicators
            try:
                result = await indicators.get_indicators(asset, interval)
                print(f"✅ get_indicators({asset}, {interval}) - Success")
            except Exception as e:
                print(f"❌ get_indicators({asset}, {interval}) - Error: {e}")
            
            # Test fetch_series
            try:
                series = await indicators.fetch_series("ema", f"{asset}/USDT", interval, results=5, params={"period": 20})
                print(f"✅ fetch_series(ema, {asset}/USDT, {interval}) - Success: {len(series)} values")
            except Exception as e:
                print(f"❌ fetch_series(ema, {asset}/USDT, {interval}) - Error: {e}")
        
        print("🎉 Symbol and interval cleaning tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_symbol_cleaning())
