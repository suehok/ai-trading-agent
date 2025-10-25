#!/usr/bin/env python3
"""
Test script to diagnose Binance LOT_SIZE errors
"""
import os
import json

def test_binance_lot_size():
    """Test Binance lot size requirements."""
    print("Testing Binance LOT_SIZE Requirements...")
    
    # Get API key from .env file
    api_key = ""
    secret_key = ""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("BINANCE_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("BINANCE_SECRET_KEY="):
                    secret_key = line.split("=", 1)[1].strip().strip('"').strip("'")
    
    if not api_key or not secret_key:
        print("❌ No Binance API keys found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test getting exchange info for different symbols
    symbols_to_test = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ZECUSDT"]
    
    for symbol in symbols_to_test:
        print(f"\n📤 Testing symbol: {symbol}")
        
        # Get exchange info using curl
        curl_command = f'''curl -s \\
        -X GET "https://api.binance.com/api/v3/exchangeInfo" \\
        -H "X-MBX-APIKEY: {api_key}"'''
        
        import subprocess
        try:
            result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    if 'symbols' in data:
                        # Find the symbol info
                        symbol_info = None
                        for s in data['symbols']:
                            if s['symbol'] == symbol:
                                symbol_info = s
                                break
                        
                        if symbol_info:
                            print(f"   ✅ Found symbol info for {symbol}")
                            
                            # Extract lot size filters
                            lot_size_filter = None
                            for filter_info in symbol_info.get('filters', []):
                                if filter_info['filterType'] == 'LOT_SIZE':
                                    lot_size_filter = filter_info
                                    break
                            
                            if lot_size_filter:
                                min_qty = float(lot_size_filter['minQty'])
                                max_qty = float(lot_size_filter['maxQty'])
                                step_size = float(lot_size_filter['stepSize'])
                                
                                print(f"      Min Quantity: {min_qty}")
                                print(f"      Max Quantity: {max_qty}")
                                print(f"      Step Size: {step_size}")
                                
                                # Calculate minimum order value
                                if 'price' in symbol_info:
                                    price = float(symbol_info['price'])
                                    min_value = min_qty * price
                                    print(f"      Min Order Value: ${min_value:.2f}")
                                
                                # Test with problematic amounts from logs
                                test_amounts = [0.0018, 0.0509, 1.0443, 0.1802]
                                for amount in test_amounts:
                                    if amount >= min_qty:
                                        print(f"      ✅ Amount {amount} is valid (>= {min_qty})")
                                    else:
                                        print(f"      ❌ Amount {amount} is too small (need >= {min_qty})")
                                        # Calculate minimum valid amount
                                        min_valid = ((min_qty // step_size) + 1) * step_size
                                        print(f"         Minimum valid amount: {min_valid}")
                            else:
                                print(f"   ⚠️  No LOT_SIZE filter found for {symbol}")
                        else:
                            print(f"   ❌ Symbol {symbol} not found in exchange info")
                    else:
                        print(f"   ❌ No symbols data in response")
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    print(f"   Response: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Request failed with return code {result.returncode}")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Request timed out")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_minimum_order_values():
    """Test minimum order values for different symbols."""
    print("\n🧪 Testing Minimum Order Values...")
    
    # Typical minimum order values for major cryptocurrencies
    min_order_values = {
        "BTCUSDT": 10.0,  # $10 minimum
        "ETHUSDT": 10.0,  # $10 minimum
        "SOLUSDT": 5.0,   # $5 minimum
        "BNBUSDT": 10.0,  # $10 minimum
        "ZECUSDT": 10.0   # $10 minimum
    }
    
    # Current prices (approximate)
    current_prices = {
        "BTCUSDT": 111282.7,
        "ETHUSDT": 3928.97,
        "SOLUSDT": 191.52,
        "BNBUSDT": 1110.1,
        "ZECUSDT": 25.0  # Approximate
    }
    
    print("Symbol | Min Order Value | Current Price | Min Quantity")
    print("-" * 60)
    
    for symbol, min_value in min_order_values.items():
        if symbol in current_prices:
            price = current_prices[symbol]
            min_qty = min_value / price
            print(f"{symbol:8} | ${min_value:13.2f} | ${price:11.2f} | {min_qty:.6f}")

if __name__ == "__main__":
    print("=" * 70)
    print("BINANCE LOT_SIZE DIAGNOSTIC TEST")
    print("=" * 70)
    
    test_binance_lot_size()
    test_minimum_order_values()
    
    print("\n" + "=" * 70)
    print("🎉 Binance LOT_SIZE diagnostic test completed!")
    print("=" * 70)
