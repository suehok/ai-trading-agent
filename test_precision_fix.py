#!/usr/bin/env python3
"""
Test script to verify the Binance precision fix
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trading.binance_api import BinanceAPI

async def test_precision_fix():
    """Test the precision fix for problematic quantities."""
    print("Testing Binance Precision Fix...")
    print("=" * 50)
    
    try:
        # Initialize the API
        api = BinanceAPI()
        
        # Test cases from the error logs
        test_cases = [
            ("BTC", 0.0018000000000000002, "BTC precision issue"),
            ("XRP", 38.610040000000005, "XRP precision issue"),
            ("SOL", 0.781, "SOL normal case"),
            ("BNB", 0.09, "BNB normal case"),
        ]
        
        for asset, amount, description in test_cases:
            print(f"\nTesting {asset}: {description}")
            print(f"Original amount: {amount}")
            
            try:
                # Test the new async rounding function
                rounded_amount = await api.round_size_async(asset, amount)
                print(f"Rounded amount: {rounded_amount}")
                print(f"String representation: '{rounded_amount}'")
                
                # Check if the rounded amount has reasonable precision
                if len(str(rounded_amount).split('.')[-1]) <= 8:
                    print(f"✅ Precision looks good for {asset}")
                else:
                    print(f"⚠️  Precision might still be too high for {asset}")
                    
            except Exception as e:
                print(f"❌ Error testing {asset}: {e}")
        
        print("\n" + "=" * 50)
        print("Testing symbol info retrieval...")
        
        # Test getting symbol info for problematic symbols
        symbols_to_test = ["BTCUSDT", "XRPUSDT", "SOLUSDT", "BNBUSDT"]
        
        for symbol in symbols_to_test:
            try:
                symbol_info = await api.get_symbol_info(symbol)
                if symbol_info:
                    print(f"✅ Got symbol info for {symbol}")
                    
                    # Extract lot size filter
                    lot_size_filter = None
                    for filter_info in symbol_info.get('filters', []):
                        if filter_info.get('filterType') == 'LOT_SIZE':
                            lot_size_filter = filter_info
                            break
                    
                    if lot_size_filter:
                        step_size = float(lot_size_filter.get('stepSize', '0.00001'))
                        min_qty = float(lot_size_filter.get('minQty', '0.00001'))
                        print(f"   Step Size: {step_size}")
                        print(f"   Min Quantity: {min_qty}")
                    else:
                        print(f"   ⚠️  No LOT_SIZE filter found")
                else:
                    print(f"❌ No symbol info for {symbol}")
                    
            except Exception as e:
                print(f"❌ Error getting symbol info for {symbol}: {e}")
        
        print("\n🎉 Precision fix test completed!")
        
    except Exception as e:
        print(f"❌ Error initializing API: {e}")
        print("Make sure you have BINANCE_API_KEY and BINANCE_SECRET_KEY in your .env file")

if __name__ == "__main__":
    asyncio.run(test_precision_fix())
