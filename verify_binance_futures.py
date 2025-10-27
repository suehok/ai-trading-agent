#!/usr/bin/env python3
"""
Verify Binance Futures Configuration Setup
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_configuration():
    """Check the Binance futures configuration"""
    print("=== Binance Futures Configuration Check ===")
    
    try:
        from config_loader import CONFIG
        from trading.binance_api import BinanceAPI
        
        # Check configuration values
        config_items = {
            'BINANCE_TESTNET': CONFIG.get('binance_testnet', 'NOT_SET'),
            'BINANCE_FUTURES_ENABLED': CONFIG.get('binance_futures_enabled', 'NOT_SET'),
            'BINANCE_FUTURES_LEVERAGE': CONFIG.get('binance_futures_leverage', 'NOT_SET'),
            'BINANCE_FUTURES_MARGIN_TYPE': CONFIG.get('binance_futures_margin_type', 'NOT_SET'),
        }
        
        for key, value in config_items.items():
            print(f"{key}: {value}")
        
        # Try to initialize Binance API
        try:
            api = BinanceAPI()
            
            print(f"\n✅ Binance API initialized successfully")
            print(f"✅ Testnet Mode: {api.testnet}")
            print(f"✅ Futures Enabled: {api.futures_enabled}")
            print(f"✅ Futures Leverage: {api.futures_leverage}x")
            print(f"✅ Futures Margin Type: {api.futures_margin_type}")
            print(f"✅ Spot Base URL: {api.base_url}")
            print(f"✅ Futures Base URL: {api.futures_base_url}")
            
            # Check if futures will be used
            if api.futures_enabled:
                print("\n🎯 Futures trading is CONFIGURED and will be used!")
                print(f"   - Leverage: {api.futures_leverage}x")
                print(f"   - Margin Type: {api.futures_margin_type}")
                print(f"   - Futures API Endpoint: {api.futures_base_url}")
            else:
                print("\n⚠️  Futures trading is NOT enabled")
                print("   Set BINANCE_FUTURES_ENABLED=true to enable")
            
            return True
            
        except ValueError as e:
            print(f"\n❌ Binance API initialization failed: {e}")
            print("\nRequired environment variables:")
            print("  - BINANCE_API_KEY")
            print("  - BINANCE_SECRET_KEY")
            return False
            
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def main():
    """Run the configuration check"""
    print("Binance Futures Configuration Verification")
    print("=" * 50)
    
    success = check_configuration()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Configuration check completed!")
        print("\nYour Binance futures settings:")
        print("  - Testnet: " + os.getenv('BINANCE_TESTNET', 'false'))
        print("  - Futures Enabled: " + os.getenv('BINANCE_FUTURES_ENABLED', 'false'))
        print("  - Leverage: " + os.getenv('BINANCE_FUTURES_LEVERAGE', '5.0') + 'x')
        print("  - Margin Type: " + os.getenv('BINANCE_FUTURES_MARGIN_TYPE', 'ISOLATED'))
    else:
        print("❌ Configuration check failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
