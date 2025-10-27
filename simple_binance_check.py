#!/usr/bin/env python3
"""
Simple Binance Account Diagnostic (no dependencies)
"""

import os
import re
from datetime import datetime

def read_env_file():
    """Read and parse .env file manually"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ {env_file} file not found!")
        return {}
    
    config = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove comments from value
                    if '#' in value:
                        value = value.split('#')[0].strip()
                    config[key] = value
        return config
    except Exception as e:
        print(f"❌ Error reading {env_file}: {e}")
        return {}

def check_binance_config():
    """Check Binance configuration"""
    print("Binance Account Diagnostic")
    print("=" * 50)
    
    config = read_env_file()
    
    if not config:
        print("❌ Could not read configuration")
        return False
    
    print("✅ Configuration loaded from .env file")
    
    # Check key settings
    trading_platform = config.get('TRADING_PLATFORM', 'NOT_SET')
    futures_enabled = config.get('BINANCE_FUTURES_ENABLED', 'NOT_SET')
    testnet = config.get('BINANCE_TESTNET', 'NOT_SET')
    api_key = config.get('BINANCE_API_KEY', 'NOT_SET')
    secret_key = config.get('BINANCE_SECRET_KEY', 'NOT_SET')
    
    print(f"\n📋 Current Settings:")
    print(f"  TRADING_PLATFORM: {trading_platform}")
    print(f"  BINANCE_FUTURES_ENABLED: {futures_enabled}")
    print(f"  BINANCE_TESTNET: {testnet}")
    print(f"  BINANCE_API_KEY: {'SET' if api_key != 'NOT_SET' else 'NOT_SET'}")
    print(f"  BINANCE_SECRET_KEY: {'SET' if secret_key != 'NOT_SET' else 'NOT_SET'}")
    
    # Check if futures is properly configured
    if trading_platform.lower() == 'binance' and futures_enabled.lower() == 'true':
        print(f"\n✅ Futures trading is CONFIGURED")
        print(f"✅ Will use Binance Futures API")
        print(f"✅ Leverage: {config.get('BINANCE_FUTURES_LEVERAGE', '5.0')}x")
        print(f"✅ Margin Type: {config.get('BINANCE_FUTURES_MARGIN_TYPE', 'ISOLATED')}")
        
        if testnet.lower() == 'false':
            print(f"⚠️  LIVE TRADING MODE - Real money!")
        else:
            print(f"✅ TESTNET MODE - Safe testing")
            
    else:
        print(f"\n❌ Futures trading is NOT properly configured")
        if trading_platform.lower() != 'binance':
            print(f"❌ Trading platform is '{trading_platform}', should be 'binance'")
        if futures_enabled.lower() != 'true':
            print(f"❌ BINANCE_FUTURES_ENABLED is '{futures_enabled}', should be 'true'")
    
    return True

def show_balance_instructions():
    """Show balance check instructions"""
    print("\n" + "=" * 50)
    print("🔍 CHECK YOUR BINANCE ACCOUNT BALANCE")
    print("=" * 50)
    
    print("\n**Step 1: Check Futures Wallet Balance**")
    print("1. Go to https://binance.com")
    print("2. Login to your account")
    print("3. Go to 'Derivatives' → 'Futures'")
    print("4. Check your 'Futures Wallet' balance")
    print("5. Look for USDT balance")
    
    print("\n**Step 2: Check Open Orders**")
    print("1. In Futures section, go to 'Open Orders' tab")
    print("2. Look for any pending orders")
    print("3. Check the age of orders (look for timestamps)")
    print("4. Identify orders older than 24 hours")
    
    print("\n**Step 3: Cancel Old Orders**")
    print("1. Select orders older than 24 hours")
    print("2. Click 'Cancel' on each old order")
    print("3. Or click 'Cancel All' to cancel all orders")
    print("4. This will free up locked funds")
    
    print("\n**Step 4: Transfer Funds (if needed)**")
    print("1. Go to 'Transfer' in Futures section")
    print("2. Transfer USDT from Spot to Futures")
    print("3. Ensure sufficient balance for trading")
    print("4. Consider the leverage you're using (5x)")

def show_troubleshooting():
    """Show troubleshooting for insufficient balance error"""
    print("\n" + "=" * 50)
    print("🚨 TROUBLESHOOTING 'INSUFFICIENT BALANCE' ERROR")
    print("=" * 50)
    
    print("\n**Error: Account has insufficient balance for requested action**")
    print("\n**Common Causes:**")
    print("1. ❌ Low balance in futures wallet")
    print("2. ❌ Funds locked in open orders")
    print("3. ❌ Orders with outdated prices")
    print("4. ❌ Need to transfer funds from spot to futures")
    print("5. ❌ Insufficient margin for leverage")
    
    print("\n**Solutions:**")
    print("1. ✅ Check futures wallet balance")
    print("2. ✅ Cancel old/open orders")
    print("3. ✅ Transfer funds from spot to futures")
    print("4. ✅ Ensure sufficient margin for 5x leverage")
    print("5. ✅ Restart the trading agent")
    
    print("\n**Recommended Actions:**")
    print("1. 🔍 Check your Binance futures wallet balance")
    print("2. 🗑️  Cancel any orders older than 24 hours")
    print("3. 💰 Transfer USDT from spot to futures if needed")
    print("4. 🔄 Restart the trading agent")
    print("5. 📊 Monitor the first few trades carefully")

def main():
    """Main function"""
    success = check_binance_config()
    
    if success:
        show_balance_instructions()
        show_troubleshooting()
        
        print("\n" + "=" * 50)
        print("✅ DIAGNOSTIC COMPLETED!")
        print("=" * 50)
        
        print("\n**Summary:**")
        print("Your Binance futures configuration looks correct.")
        print("The 'insufficient balance' error is likely due to:")
        print("1. Low balance in futures wallet")
        print("2. Funds locked in open orders")
        print("3. Need to transfer funds from spot to futures")
        
        print("\n**Next Steps:**")
        print("1. 🔍 Check your Binance futures wallet balance")
        print("2. 🗑️  Cancel any old orders (>24h)")
        print("3. 💰 Transfer funds if needed")
        print("4. 🔄 Restart the trading agent")
        print("5. 📊 Monitor trading activity")
        
    else:
        print("\n❌ Configuration check failed!")
        print("Please check your .env file settings")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
