#!/usr/bin/env python3
"""
Test script to verify Binance futures setup
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_futures_setup():
    """Test the futures setup."""
    print("Testing Binance Futures Setup")
    print("=" * 50)
    
    try:
        from trading.binance_api import BinanceAPI
        
        # Initialize the API
        api = BinanceAPI()
        
        print(f"Futures Enabled: {api.futures_enabled}")
        print(f"Futures Leverage: {api.futures_leverage}")
        print(f"Futures Margin Type: {api.futures_margin_type}")
        print(f"Futures Base URL: {api.futures_base_url}")
        print()
        
        if not api.futures_enabled:
            print("❌ Futures trading is not enabled!")
            print("To enable futures trading, set BINANCE_FUTURES_ENABLED=true in your .env file")
            return
        
        print("Testing futures-specific methods...")
        print()
        
        # Test getting funding rate
        print("Testing funding rate for BTC...")
        try:
            funding_rate = await api.get_funding_rate("BTC")
            if funding_rate is not None:
                print(f"✅ BTC Funding Rate: {funding_rate:.6f}")
            else:
                print("❌ Failed to get funding rate")
        except Exception as e:
            print(f"❌ Error getting funding rate: {e}")
        
        print()
        
        # Test getting open interest
        print("Testing open interest for BTC...")
        try:
            open_interest = await api.get_open_interest("BTC")
            if open_interest is not None:
                print(f"✅ BTC Open Interest: {open_interest:,.2f}")
            else:
                print("❌ Failed to get open interest")
        except Exception as e:
            print(f"❌ Error getting open interest: {e}")
        
        print()
        
        # Test getting futures account info
        print("Testing futures account info...")
        try:
            account_info = await api.get_futures_account_info()
            if 'error' not in account_info:
                print("✅ Futures account info retrieved successfully")
                print(f"   Total Wallet Balance: {account_info.get('totalWalletBalance', 'N/A')}")
                print(f"   Available Balance: {account_info.get('availableBalance', 'N/A')}")
            else:
                print(f"❌ Error getting futures account info: {account_info.get('error')}")
        except Exception as e:
            print(f"❌ Error getting futures account info: {e}")
        
        print()
        
        # Test getting position info
        print("Testing position info...")
        try:
            positions = await api.get_position_info()
            if positions:
                print(f"✅ Found {len(positions)} positions")
                for pos in positions[:3]:  # Show first 3 positions
                    symbol = pos.get('symbol', 'Unknown')
                    size = pos.get('positionAmt', '0')
                    entry_price = pos.get('entryPrice', '0')
                    print(f"   {symbol}: {size} @ {entry_price}")
            else:
                print("✅ No open positions found")
        except Exception as e:
            print(f"❌ Error getting position info: {e}")
        
        print()
        print("🎉 Futures setup test completed!")
        
    except Exception as e:
        print(f"❌ Error initializing API: {e}")
        print("Make sure you have BINANCE_API_KEY and BINANCE_SECRET_KEY in your .env file")

if __name__ == "__main__":
    asyncio.run(test_futures_setup())
