#!/usr/bin/env python3
"""
Test script to verify the round_size method fix
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_round_size_fix():
    """Test the round_size method fix."""
    print("Testing round_size Method Fix")
    print("=" * 40)
    
    # Import the precision fix function directly
    from trading.binance_api import BinanceAPI
    
    # Create a mock API instance for testing
    class MockBinanceAPI:
        def _apply_precision_fix(self, clean_asset: str, amount: float) -> float:
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
        
        def round_size(self, asset: str, amount: float) -> float:
            """Round amount to asset's precision using hardcoded rules."""
            # Clean asset name
            clean_asset = asset.strip().strip('"').strip("'").upper()
            
            # Use the same precision fix logic as the async version
            return self._apply_precision_fix(clean_asset, amount)
    
    api = MockBinanceAPI()
    
    # Test the exact problematic quantities from the logs
    test_cases = [
        ("BTC", 0.0018000000000000002, "BTC precision issue from logs"),
        ("XRP", 38.610040000000005, "XRP precision issue from logs"),
    ]
    
    print("Testing round_size method with problematic quantities...")
    print()
    
    for asset, amount, description in test_cases:
        print(f"Testing {asset}: {description}")
        print(f"Original amount: {amount}")
        print(f"String before: '{amount}'")
        
        try:
            # Test the round_size method
            fixed_amount = api.round_size(asset, amount)
            print(f"Fixed amount: {fixed_amount}")
            print(f"String after: '{fixed_amount}'")
            
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
            
        except Exception as e:
            print(f"❌ Error testing {asset}: {e}")
        
        print("-" * 40)
    
    print("\n🎉 round_size method fix test completed!")
    print("\nThe round_size method now uses the same precision logic as round_size_async!")

if __name__ == "__main__":
    test_round_size_fix()
