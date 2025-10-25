#!/usr/bin/env python3
"""
Simple test script to verify the precision fix logic
"""
import math

def round_size_simple(asset: str, amount: float) -> float:
    """Simple version of the rounding logic for testing."""
    # Clean asset name
    clean_asset = asset.strip().strip('"').strip("'").upper()
    
    # Fallback to hardcoded step sizes for major assets
    step_sizes = {
        'BTC': 0.00001,   # 5 decimal places
        'ETH': 0.0001,    # 4 decimal places
        'SOL': 0.001,     # 3 decimal places
        'BNB': 0.001,     # 3 decimal places
        'ZEC': 0.001,     # 3 decimal places
        'XRP': 0.1,       # 1 decimal place
        'DOGE': 1.0,      # 0 decimal places
        'EIGEN': 0.01,    # 2 decimal places
    }
    
    step_size = step_sizes.get(clean_asset, 0.00001)
    
    # Round to the appropriate step size
    rounded = round(amount / step_size) * step_size
    
    # Additional precision fix: round to the appropriate number of decimal places
    if clean_asset == 'BTC':
        # BTC: 5 decimal places
        rounded = round(rounded, 5)
    elif clean_asset == 'ETH':
        # ETH: 4 decimal places
        rounded = round(rounded, 4)
    elif clean_asset in ['SOL', 'BNB', 'ZEC']:
        # SOL, BNB, ZEC: 3 decimal places
        rounded = round(rounded, 3)
    elif clean_asset == 'XRP':
        # XRP: 1 decimal place
        rounded = round(rounded, 1)
    elif clean_asset == 'DOGE':
        # DOGE: 0 decimal places
        rounded = round(rounded, 0)
    elif clean_asset == 'EIGEN':
        # EIGEN: 2 decimal places
        rounded = round(rounded, 2)
    else:
        # Default: 8 decimal places
        rounded = round(rounded, 8)
    
    return max(rounded, step_size)

def test_precision_fix():
    """Test the precision fix for problematic quantities."""
    print("Testing Binance Precision Fix (Simple Version)...")
    print("=" * 60)
    
    # Test cases from the error logs
    test_cases = [
        ("BTC", 0.0018000000000000002, "BTC precision issue"),
        ("XRP", 38.610040000000005, "XRP precision issue"),
        ("SOL", 0.781, "SOL normal case"),
        ("BNB", 0.09, "BNB normal case"),
        ("ETH", 0.0509, "ETH normal case"),
    ]
    
    for asset, amount, description in test_cases:
        print(f"\nTesting {asset}: {description}")
        print(f"Original amount: {amount}")
        
        try:
            # Test the rounding function
            rounded_amount = round_size_simple(asset, amount)
            print(f"Rounded amount: {rounded_amount}")
            print(f"String representation: '{rounded_amount}'")
            
            # Check precision
            if '.' in str(rounded_amount):
                decimal_places = len(str(rounded_amount).split('.')[-1])
                print(f"Decimal places: {decimal_places}")
                
                # Check if precision is reasonable
                if decimal_places <= 8:
                    print(f"✅ Precision looks good for {asset}")
                else:
                    print(f"⚠️  Precision might still be too high for {asset}")
            else:
                print(f"✅ No decimal places for {asset}")
                
        except Exception as e:
            print(f"❌ Error testing {asset}: {e}")
    
    print("\n" + "=" * 60)
    print("Testing specific problematic cases...")
    
    # Test the exact problematic quantities from the logs
    problematic_cases = [
        ("BTC", 0.0018000000000000002),
        ("XRP", 38.610040000000005),
    ]
    
    for asset, amount in problematic_cases:
        print(f"\nFixing {asset} precision issue:")
        print(f"Before: {amount}")
        fixed = round_size_simple(asset, amount)
        print(f"After:  {fixed}")
        print(f"String: '{fixed}'")
        
        # Verify the fix
        if asset == "BTC":
            # BTC should have 5 decimal places max
            if len(str(fixed).split('.')[-1]) <= 5:
                print("✅ BTC precision fixed!")
            else:
                print("❌ BTC precision still too high")
        elif asset == "XRP":
            # XRP should have 1 decimal place max
            if len(str(fixed).split('.')[-1]) <= 1:
                print("✅ XRP precision fixed!")
            else:
                print("❌ XRP precision still too high")
    
    print("\n🎉 Precision fix test completed!")

if __name__ == "__main__":
    test_precision_fix()
