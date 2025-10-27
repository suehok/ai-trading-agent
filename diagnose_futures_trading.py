#!/usr/bin/env python3
"""
Simple Binance Futures Configuration Check (no external dependencies)
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_environment_variables():
    """Check environment variables"""
    print("=== Environment Variables Check ===")
    
    futures_vars = [
        'TRADING_PLATFORM',
        'BINANCE_TESTNET',
        'BINANCE_FUTURES_ENABLED',
        'BINANCE_FUTURES_LEVERAGE',
        'BINANCE_FUTURES_MARGIN_TYPE',
        'BINANCE_API_KEY',
        'BINANCE_SECRET_KEY'
    ]
    
    for var in futures_vars:
        value = os.getenv(var, 'NOT_SET')
        if 'KEY' in var and value != 'NOT_SET':
            value = f"{value[:10]}..." if len(value) > 10 else "***"
        print(f"{var}: {value}")
    
    return True

def check_configuration():
    """Check the loaded configuration"""
    print("\n=== Configuration Check ===")
    
    try:
        from config_loader import CONFIG
        
        config_items = {
            'trading_platform': CONFIG.get('trading_platform', 'NOT_SET'),
            'binance_testnet': CONFIG.get('binance_testnet', 'NOT_SET'),
            'binance_futures_enabled': CONFIG.get('binance_futures_enabled', 'NOT_SET'),
            'binance_futures_leverage': CONFIG.get('binance_futures_leverage', 'NOT_SET'),
            'binance_futures_margin_type': CONFIG.get('binance_futures_margin_type', 'NOT_SET'),
            'binance_api_key': CONFIG.get('binance_api_key', 'NOT_SET'),
            'binance_secret_key': CONFIG.get('binance_secret_key', 'NOT_SET')
        }
        
        for key, value in config_items.items():
            if 'api_key' in key and value != 'NOT_SET':
                value = f"{value[:10]}..." if len(value) > 10 else "***"
            print(f"{key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def check_trading_platform():
    """Check which trading platform is being used"""
    print("\n=== Trading Platform Check ===")
    
    try:
        from config_loader import CONFIG
        
        platform = CONFIG.get('trading_platform', 'hyperliquid').lower()
        print(f"Selected Platform: {platform}")
        
        if platform == 'binance':
            print("✅ Using Binance for trading")
            futures_enabled = CONFIG.get('binance_futures_enabled', 'false').lower() == 'true'
            print(f"Futures Trading: {'✅ ENABLED' if futures_enabled else '❌ DISABLED'}")
            
            if not futures_enabled:
                print("\n🔧 To enable futures trading:")
                print("1. Set BINANCE_FUTURES_ENABLED=true in your .env file")
                print("2. Restart the trading agent")
        else:
            print(f"❌ Using {platform} for trading (not Binance)")
            print("\n🔧 To use Binance futures:")
            print("1. Set TRADING_PLATFORM=binance in your .env file")
            print("2. Set BINANCE_FUTURES_ENABLED=true")
            print("3. Restart the trading agent")
        
        return platform == 'binance'
    except Exception as e:
        print(f"❌ Error checking trading platform: {e}")
        return False

def check_binance_api_initialization():
    """Check if Binance API can be initialized"""
    print("\n=== Binance API Initialization Check ===")
    
    try:
        from trading.binance_api import BinanceAPI
        from config_loader import CONFIG
        
        api = BinanceAPI()
        print(f"✅ Binance API initialized successfully")
        print(f"✅ Trading Platform: {CONFIG.get('trading_platform', 'NOT_SET')}")
        print(f"✅ Futures Enabled: {api.futures_enabled}")
        print(f"✅ Futures Leverage: {api.futures_leverage}")
        print(f"✅ Futures Margin Type: {api.futures_margin_type}")
        print(f"✅ Testnet Mode: {api.testnet}")
        print(f"✅ Base URL: {api.base_url}")
        print(f"✅ Futures Base URL: {api.futures_base_url}")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing Binance API: {e}")
        return False

def check_futures_requirements():
    """Check if all requirements for futures trading are met"""
    print("\n=== Futures Trading Requirements Check ===")
    
    try:
        from config_loader import CONFIG
        
        requirements = {
            'TRADING_PLATFORM=binance': CONFIG.get('trading_platform', '').lower() == 'binance',
            'BINANCE_FUTURES_ENABLED=true': CONFIG.get('binance_futures_enabled', 'false').lower() == 'true',
            'BINANCE_API_KEY set': bool(CONFIG.get('binance_api_key')),
            'BINANCE_SECRET_KEY set': bool(CONFIG.get('binance_secret_key')),
        }
        
        all_met = True
        for requirement, met in requirements.items():
            status = "✅" if met else "❌"
            print(f"{status} {requirement}")
            if not met:
                all_met = False
        
        if not all_met:
            print("\n🔧 Missing Requirements:")
            if not requirements['TRADING_PLATFORM=binance']:
                print("- Set TRADING_PLATFORM=binance")
            if not requirements['BINANCE_FUTURES_ENABLED=true']:
                print("- Set BINANCE_FUTURES_ENABLED=true")
            if not requirements['BINANCE_API_KEY set']:
                print("- Set BINANCE_API_KEY=your_api_key")
            if not requirements['BINANCE_SECRET_KEY set']:
                print("- Set BINANCE_SECRET_KEY=your_secret_key")
        
        return all_met
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("Binance Futures Trading Diagnostic")
    print("=" * 50)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Configuration", check_configuration),
        ("Trading Platform", check_trading_platform),
        ("Binance API Initialization", check_binance_api_initialization),
        ("Futures Requirements", check_futures_requirements),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed with exception: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("Diagnostic Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Futures trading should be working.")
        print("\nIf futures trading is still not working, check:")
        print("1. Binance account has futures enabled")
        print("2. API key has 'Enable Futures' permission")
        print("3. Sufficient funds in futures wallet")
        print("4. No API restrictions or IP whitelist issues")
        print("5. Restart the trading agent after configuration changes")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Update your .env file with correct settings")
        print("2. Enable futures in your Binance account")
        print("3. Enable futures permission in your API key")
        print("4. Transfer funds to your futures wallet")
        print("5. Restart the trading agent")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
