#!/usr/bin/env python3
"""
Standalone test script to verify the Binance precision fix
"""
def apply_precision_fix(clean_asset: str, amount: float) -> float:
    """Apply precision fix based on asset type."""
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
    """Test the precision fix for the exact problematic quantities from the logs."""
    print("Testing Binance Precision Fix - Standalone Version")
    print("=" * 60)
    
    # Test cases from the actual error logs
    test_cases = [
        ("BTC", 0.0018000000000000002, "BTC precision issue from logs"),
        ("XRP", 38.610040000000005, "XRP precision issue from logs"),
        ("SOL", 0.781, "SOL normal case"),
        ("BNB", 0.09, "BNB normal case"),
        ("ETH", 0.0509, "ETH normal case"),
    ]
    
    print("Testing precision fix for problematic quantities...")
    print()
    
    for asset, amount, description in test_cases:
        print(f"Testing {asset}: {description}")
        print(f"Original amount: {amount}")
        
        try:
            # Test the precision fix
            fixed_amount = apply_precision_fix(asset, amount)
            print(f"Fixed amount: {fixed_amount}")
            print(f"String representation: '{fixed_amount}'")
            
            # Check if the fix is correct
            if asset == "BTC":
                # BTC should have max 5 decimal places
                decimal_places = len(str(fixed_amount).split('.')[-1]) if '.' in str(fixed_amount) else 0
                if decimal_places <= 5:
                    print("✅ BTC precision fixed!")
                else:
                    print(f"❌ BTC precision still too high: {decimal_places} decimal places")
            elif asset == "XRP":
                # XRP should have max 1 decimal place
                decimal_places = len(str(fixed_amount).split('.')[-1]) if '.' in str(fixed_amount) else 0
                if decimal_places <= 1:
                    print("✅ XRP precision fixed!")
                else:
                    print(f"❌ XRP precision still too high: {decimal_places} decimal places")
            else:
                # Other assets should have reasonable precision
                decimal_places = len(str(fixed_amount).split('.')[-1]) if '.' in str(fixed_amount) else 0
                if decimal_places <= 8:
                    print(f"✅ {asset} precision looks good!")
                else:
                    print(f"⚠️  {asset} precision might be too high: {decimal_places} decimal places")
            
        except Exception as e:
            print(f"❌ Error testing {asset}: {e}")
        
        print("-" * 40)
    
    print("\nTesting specific problematic cases from error logs...")
    print()
    
    # Test the exact problematic quantities
    problematic_cases = [
        ("BTC", 0.0018000000000000002),
        ("XRP", 38.610040000000005),
    ]
    
    for asset, amount in problematic_cases:
        print(f"Fixing {asset} precision issue:")
        print(f"Before: {amount}")
        print(f"String before: '{amount}'")
        
        fixed = apply_precision_fix(asset, amount)
        print(f"After:  {fixed}")
        print(f"String after:  '{fixed}'")
        
        # Verify the fix
        if asset == "BTC":
            # BTC should have 5 decimal places max
            decimal_places = len(str(fixed).split('.')[-1]) if '.' in str(fixed) else 0
            if decimal_places <= 5:
                print("✅ BTC precision fixed!")
            else:
                print(f"❌ BTC precision still too high: {decimal_places} decimal places")
        elif asset == "XRP":
            # XRP should have 1 decimal place max
            decimal_places = len(str(fixed).split('.')[-1]) if '.' in str(fixed) else 0
            if decimal_places <= 1:
                print("✅ XRP precision fixed!")
            else:
                print(f"❌ XRP precision still too high: {decimal_places} decimal places")
        
        print("-" * 40)
    
    print("\n🎉 Precision fix test completed!")
    print("\nThe fix should resolve the Binance API precision errors:")
    print("- BTC: 0.0018000000000000002 → 0.0018 (5 decimal places)")
    print("- XRP: 38.610040000000005 → 38.6 (1 decimal place)")
    print("- All other assets: Proper precision based on their requirements")

if __name__ == "__main__":
    test_precision_fix()
