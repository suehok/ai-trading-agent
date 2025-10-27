#!/usr/bin/env python3
"""
Simple Binance Account Check (no external dependencies)
- Check configuration
- Show what the script would do
"""

import os
import sys
from datetime import datetime, timezone

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_configuration():
    """Check Binance configuration"""
    print("Binance Account Check")
    print("=" * 40)
    
    try:
        from config_loader import CONFIG
        
        print("✅ Configuration loaded successfully")
        print(f"✅ Trading Platform: {CONFIG.get('trading_platform', 'NOT_SET')}")
        print(f"✅ Futures Enabled: {CONFIG.get('binance_futures_enabled', 'NOT_SET')}")
        print(f"✅ Testnet Mode: {CONFIG.get('binance_testnet', 'NOT_SET')}")
        print(f"✅ API Key: {'SET' if CONFIG.get('binance_api_key') else 'NOT_SET'}")
        print(f"✅ Secret Key: {'SET' if CONFIG.get('binance_secret_key') else 'NOT_SET'}")
        
        # Check if futures is enabled
        futures_enabled = CONFIG.get('binance_futures_enabled', 'false').lower() == 'true'
        platform = CONFIG.get('trading_platform', '').lower()
        
        if platform == 'binance' and futures_enabled:
            print("\n🎯 Futures trading is CONFIGURED")
            print("✅ Will use Binance Futures API")
            print("✅ Will apply 5x leverage")
            print("✅ Will use isolated margin")
        else:
            print("\n⚠️  Futures trading is NOT configured")
            if platform != 'binance':
                print(f"❌ Trading platform is '{platform}', not 'binance'")
            if not futures_enabled:
                print("❌ BINANCE_FUTURES_ENABLED is not 'true'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def show_balance_check_instructions():
    """Show instructions for checking balance"""
    print("\n=== Account Balance Check Instructions ===")
    print("\nTo check your Binance account balance and open orders:")
    
    print("\n1. **Manual Check via Binance Website:**")
    print("   - Go to https://binance.com")
    print("   - Login to your account")
    print("   - Go to 'Derivatives' → 'Futures'")
    print("   - Check your 'Futures Wallet' balance")
    print("   - Check 'Open Orders' tab for any pending orders")
    
    print("\n2. **API Check (requires dependencies):**")
    print("   - Install required packages: pip install aiohttp")
    print("   - Run: python3 check_binance_account.py")
    
    print("\n3. **Common Balance Issues:**")
    print("   - Insufficient funds in futures wallet")
    print("   - Funds locked in open orders")
    print("   - Need to transfer from spot to futures wallet")
    
    print("\n4. **Transfer Funds to Futures Wallet:**")
    print("   - Go to Binance → Futures → Transfer")
    print("   - Transfer USDT from Spot to Futures")
    print("   - Ensure sufficient balance for trading")

def show_order_cleanup_instructions():
    """Show instructions for order cleanup"""
    print("\n=== Order Cleanup Instructions ===")
    
    print("\n**To cancel old orders manually:**")
    print("1. Go to Binance → Futures → Open Orders")
    print("2. Look for orders older than 24 hours")
    print("3. Click 'Cancel' on each old order")
    print("4. This will free up locked funds")
    
    print("\n**To cancel all orders:**")
    print("1. Go to Binance → Futures → Open Orders")
    print("2. Click 'Cancel All' button")
    print("3. Confirm the cancellation")
    print("4. This will cancel all pending orders")
    
    print("\n**Why cancel old orders:**")
    print("- Old orders may have outdated prices")
    print("- They lock up funds that could be used for new trades")
    print("- They can cause 'insufficient balance' errors")
    print("- Fresh orders with current market prices are better")

def show_troubleshooting():
    """Show troubleshooting steps"""
    print("\n=== Troubleshooting 'Insufficient Balance' Error ===")
    
    print("\n**Common Causes:**")
    print("1. ❌ Low balance in futures wallet")
    print("2. ❌ Funds locked in open orders")
    print("3. ❌ Orders with outdated prices")
    print("4. ❌ Need to transfer funds from spot to futures")
    
    print("\n**Solutions:**")
    print("1. ✅ Check futures wallet balance")
    print("2. ✅ Cancel old/open orders")
    print("3. ✅ Transfer funds from spot to futures")
    print("4. ✅ Ensure sufficient margin for leverage")
    
    print("\n**Recommended Actions:**")
    print("1. 🔍 Check your Binance futures wallet balance")
    print("2. 🗑️  Cancel any orders older than 24 hours")
    print("3. 💰 Transfer USDT from spot to futures if needed")
    print("4. 🔄 Restart the trading agent")
    print("5. 📊 Monitor the first few trades carefully")

def main():
    """Main function"""
    print("Binance Account Diagnostic Tool")
    print("=" * 50)
    
    # Check configuration
    config_ok = check_configuration()
    
    if config_ok:
        show_balance_check_instructions()
        show_order_cleanup_instructions()
        show_troubleshooting()
        
        print("\n" + "=" * 50)
        print("✅ Diagnostic completed!")
        print("\n**Next Steps:**")
        print("1. Check your Binance futures wallet balance")
        print("2. Cancel any old orders (>24h)")
        print("3. Transfer funds if needed")
        print("4. Restart the trading agent")
        print("5. Monitor trading activity")
        
    else:
        print("\n❌ Configuration check failed!")
        print("Please check your .env file settings")
    
    return config_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
