#!/usr/bin/env python3
"""
Quick test script to verify Binance API fixes
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.trading.binance_api import BinanceAPI
from src.config_loader import CONFIG

async def test_binance_api():
    """Test basic Binance API functionality."""
    print("Testing Binance API...")
    
    # Check if API keys are configured
    if not CONFIG.get("binance_api_key") or not CONFIG.get("binance_secret_key"):
        print("❌ Binance API keys not configured")
        print("Please set BINANCE_API_KEY and BINANCE_SECRET_KEY in your .env file")
        return False
    
    try:
        # Initialize API
        api = BinanceAPI()
        print("✅ Binance API initialized")
        
        # Test getting current price (no auth required)
        print("Testing get_current_price...")
        price = await api.get_current_price("BTC")
        print(f"✅ BTC price: ${price}")
        
        # Test getting user state (requires auth)
        print("Testing get_user_state...")
        state = await api.get_user_state()
        print(f"✅ User state: Balance ${state.get('balance', 0):.2f}")
        
        # Test getting open orders (requires auth)
        print("Testing get_open_orders...")
        orders = await api.get_open_orders()
        print(f"✅ Open orders: {len(orders)}")
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_binance_api())
