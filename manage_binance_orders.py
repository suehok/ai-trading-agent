#!/usr/bin/env python3
"""
Binance Order Management Script
- Check for open orders
- Cancel orders older than 1 day
- Check account balance
"""

import asyncio
import sys
import os
from datetime import datetime, timezone, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def get_open_orders_with_timestamps(api):
    """Get open orders with timestamp information"""
    try:
        # Use futures endpoint if futures is enabled
        if api.futures_enabled:
            endpoint = '/fapi/v1/openOrders'
            use_futures = True
        else:
            endpoint = '/api/v3/openOrders'
            use_futures = False
        
        orders = await api._make_request('GET', endpoint, signed=True, use_futures=use_futures)
        
        # Add timestamp parsing
        for order in orders:
            if 'time' in order:
                # Convert timestamp to datetime
                timestamp_ms = int(order['time'])
                order['order_time'] = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            else:
                order['order_time'] = None
        
        return orders
    except Exception as e:
        print(f"❌ Error getting open orders: {e}")
        return []

async def check_account_balance(api):
    """Check account balance"""
    try:
        if api.futures_enabled:
            # Get futures account info
            account_info = await api._make_request('GET', '/fapi/v2/account', signed=True, use_futures=True)
            
            print("=== Futures Account Balance ===")
            if 'assets' in account_info:
                for asset in account_info['assets']:
                    balance = float(asset.get('walletBalance', 0))
                    if balance > 0:
                        print(f"✅ {asset.get('asset', 'Unknown')}: {balance:.4f}")
            
            if 'totalWalletBalance' in account_info:
                total_balance = float(account_info['totalWalletBalance'])
                print(f"💰 Total Wallet Balance: {total_balance:.4f} USDT")
            
            return account_info
        else:
            # Get spot account info
            account_info = await api._make_request('GET', '/api/v3/account', signed=True)
            
            print("=== Spot Account Balance ===")
            if 'balances' in account_info:
                for balance in account_info['balances']:
                    free = float(balance.get('free', 0))
                    locked = float(balance.get('locked', 0))
                    total = free + locked
                    if total > 0:
                        print(f"✅ {balance.get('asset', 'Unknown')}: {total:.4f} (Free: {free:.4f}, Locked: {locked:.4f})")
            
            return account_info
    except Exception as e:
        print(f"❌ Error checking account balance: {e}")
        return None

async def cancel_old_orders(api, max_age_hours=24):
    """Cancel orders older than specified hours"""
    try:
        orders = await get_open_orders_with_timestamps(api)
        
        if not orders:
            print("✅ No open orders found")
            return
        
        print(f"\n=== Open Orders ({len(orders)} found) ===")
        
        now = datetime.now(timezone.utc)
        old_orders = []
        
        for order in orders:
            symbol = order.get('symbol', 'Unknown')
            order_id = order.get('orderId', 'Unknown')
            side = order.get('side', 'Unknown')
            quantity = order.get('origQty', 0)
            price = order.get('price', 0)
            order_time = order.get('order_time')
            
            print(f"📋 Order {order_id}: {side} {quantity} {symbol} @ {price}")
            
            if order_time:
                age = now - order_time
                age_hours = age.total_seconds() / 3600
                print(f"   ⏰ Age: {age_hours:.1f} hours")
                
                if age_hours > max_age_hours:
                    old_orders.append(order)
                    print(f"   ⚠️  OLD ORDER (> {max_age_hours}h)")
                else:
                    print(f"   ✅ Recent order (< {max_age_hours}h)")
            else:
                print(f"   ❓ No timestamp available")
        
        if old_orders:
            print(f"\n🗑️  Found {len(old_orders)} old orders to cancel:")
            
            for order in old_orders:
                symbol = order.get('symbol', 'Unknown')
                order_id = order.get('orderId', 'Unknown')
                
                try:
                    if api.futures_enabled:
                        endpoint = '/fapi/v1/order'
                        use_futures = True
                    else:
                        endpoint = '/api/v3/order'
                        use_futures = False
                    
                    params = {
                        'symbol': symbol,
                        'orderId': order_id
                    }
                    
                    result = await api._make_request('DELETE', endpoint, params, signed=True, use_futures=use_futures)
                    print(f"✅ Cancelled order {order_id} for {symbol}")
                    
                except Exception as e:
                    print(f"❌ Failed to cancel order {order_id}: {e}")
            
            print(f"\n🎉 Cancelled {len(old_orders)} old orders")
        else:
            print(f"\n✅ No orders older than {max_age_hours} hours found")
            
    except Exception as e:
        print(f"❌ Error processing orders: {e}")

async def main():
    """Main function"""
    print("Binance Order Management Tool")
    print("=" * 50)
    
    try:
        from trading.binance_api import BinanceAPI
        from config_loader import CONFIG
        
        # Initialize API
        api = BinanceAPI()
        
        print(f"✅ Binance API initialized")
        print(f"✅ Testnet Mode: {api.testnet}")
        print(f"✅ Futures Enabled: {api.futures_enabled}")
        print(f"✅ Base URL: {api.base_url}")
        if api.futures_enabled:
            print(f"✅ Futures Base URL: {api.futures_base_url}")
        
        # Check account balance
        print("\n" + "=" * 50)
        await check_account_balance(api)
        
        # Check and cancel old orders
        print("\n" + "=" * 50)
        await cancel_old_orders(api, max_age_hours=24)
        
        print("\n" + "=" * 50)
        print("✅ Order management completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
