#!/usr/bin/env python3
"""
Simple Binance Order Cleanup Script
- Check account balance
- List open orders
- Cancel old orders
"""

import asyncio
import sys
import os
from datetime import datetime, timezone, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def check_balance_and_orders():
    """Check balance and manage orders"""
    try:
        from trading.binance_api import BinanceAPI
        from config_loader import CONFIG
        
        api = BinanceAPI()
        
        print("Binance Account Check")
        print("=" * 40)
        print(f"✅ API initialized")
        print(f"✅ Futures enabled: {api.futures_enabled}")
        print(f"✅ Testnet: {api.testnet}")
        
        # Check balance
        print("\n=== Account Balance ===")
        try:
            if api.futures_enabled:
                # Futures account
                account = await api._make_request('GET', '/fapi/v2/account', signed=True, use_futures=True)
                
                if 'assets' in account:
                    total_balance = 0
                    for asset in account['assets']:
                        balance = float(asset.get('walletBalance', 0))
                        if balance > 0:
                            print(f"💰 {asset.get('asset', 'Unknown')}: {balance:.4f}")
                            if asset.get('asset') == 'USDT':
                                total_balance = balance
                    
                    print(f"\n💵 Total USDT Balance: {total_balance:.4f}")
                    
                    if total_balance < 10:
                        print("⚠️  Low balance! Consider adding funds to futures wallet")
                    else:
                        print("✅ Sufficient balance for trading")
                
            else:
                # Spot account
                account = await api._make_request('GET', '/api/v3/account', signed=True)
                
                if 'balances' in account:
                    for balance in account['balances']:
                        free = float(balance.get('free', 0))
                        locked = float(balance.get('locked', 0))
                        total = free + locked
                        if total > 0:
                            print(f"💰 {balance.get('asset', 'Unknown')}: {total:.4f} (Free: {free:.4f}, Locked: {locked:.4f})")
                            
        except Exception as e:
            print(f"❌ Error checking balance: {e}")
        
        # Check open orders
        print("\n=== Open Orders ===")
        try:
            if api.futures_enabled:
                orders = await api._make_request('GET', '/fapi/v1/openOrders', signed=True, use_futures=True)
            else:
                orders = await api._make_request('GET', '/api/v3/openOrders', signed=True)
            
            if not orders:
                print("✅ No open orders")
            else:
                print(f"📋 Found {len(orders)} open orders:")
                
                now = datetime.now(timezone.utc)
                old_orders = []
                
                for order in orders:
                    symbol = order.get('symbol', 'Unknown')
                    order_id = order.get('orderId', 'Unknown')
                    side = order.get('side', 'Unknown')
                    quantity = order.get('origQty', 0)
                    price = order.get('price', 0)
                    status = order.get('status', 'Unknown')
                    
                    # Check order age
                    if 'time' in order:
                        timestamp_ms = int(order['time'])
                        order_time = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
                        age = now - order_time
                        age_hours = age.total_seconds() / 3600
                        
                        print(f"  📋 {order_id}: {side} {quantity} {symbol} @ {price} (Age: {age_hours:.1f}h)")
                        
                        if age_hours > 24:  # Older than 1 day
                            old_orders.append(order)
                            print(f"    ⚠️  OLD ORDER (> 24h)")
                        else:
                            print(f"    ✅ Recent order")
                    else:
                        print(f"  📋 {order_id}: {side} {quantity} {symbol} @ {price}")
                
                # Cancel old orders
                if old_orders:
                    print(f"\n🗑️  Cancelling {len(old_orders)} old orders...")
                    
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
                            print(f"  ✅ Cancelled order {order_id} for {symbol}")
                            
                        except Exception as e:
                            print(f"  ❌ Failed to cancel order {order_id}: {e}")
                    
                    print(f"\n🎉 Cancelled {len(old_orders)} old orders")
                else:
                    print("\n✅ No old orders to cancel")
                    
        except Exception as e:
            print(f"❌ Error checking orders: {e}")
        
        print("\n" + "=" * 40)
        print("✅ Account check completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main function"""
    success = await check_balance_and_orders()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
