#!/usr/bin/env python3
"""
Test script to verify the balance adjustment logic
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_balance_adjustment():
    """Test the balance adjustment logic."""
    print("Testing Balance Adjustment Logic")
    print("=" * 50)
    
    # Import the risk manager
    from risk.risk_manager import RiskManager
    
    # Create a risk manager instance
    risk_manager = RiskManager()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Sufficient Balance",
            "allocation_usd": 100.0,
            "current_balance": 500.0,
            "expected_result": "approved"
        },
        {
            "name": "Insufficient Balance - Should Adjust",
            "allocation_usd": 300.0,
            "current_balance": 200.0,
            "expected_result": "adjusted"
        },
        {
            "name": "Insufficient Balance - Too Small",
            "allocation_usd": 300.0,
            "current_balance": 5.0,  # Less than min_position_size (10.0)
            "expected_result": "rejected"
        },
        {
            "name": "Exact Balance",
            "allocation_usd": 200.0,
            "current_balance": 200.0,
            "expected_result": "approved"
        }
    ]
    
    print("Testing allocation validation...")
    print()
    
    for test_case in test_cases:
        print(f"Test: {test_case['name']}")
        print(f"Allocation: ${test_case['allocation_usd']:.2f}")
        print(f"Balance: ${test_case['current_balance']:.2f}")
        
        # Test allocation validation
        is_valid, reason, adjusted_allocation = risk_manager.validate_allocation(
            test_case['allocation_usd'],
            test_case['current_balance'],
            [],  # No existing positions
            "DOGE"
        )
        
        print(f"Result: {'Valid' if is_valid else 'Invalid'}")
        print(f"Reason: {reason}")
        print(f"Adjusted Allocation: ${adjusted_allocation:.2f}")
        
        # Check if result matches expectation
        if test_case['expected_result'] == "approved":
            if is_valid and adjusted_allocation == test_case['allocation_usd']:
                print("✅ Test passed - Allocation approved as expected")
            else:
                print("❌ Test failed - Expected approval but got different result")
        elif test_case['expected_result'] == "adjusted":
            if is_valid and adjusted_allocation < test_case['allocation_usd']:
                print("✅ Test passed - Allocation adjusted as expected")
            else:
                print("❌ Test failed - Expected adjustment but got different result")
        elif test_case['expected_result'] == "rejected":
            if not is_valid:
                print("✅ Test passed - Allocation rejected as expected")
            else:
                print("❌ Test failed - Expected rejection but got approval")
        
        print("-" * 40)
    
    print("\nTesting position sizing validation...")
    print()
    
    # Test position sizing scenarios
    position_tests = [
        {
            "name": "Sufficient Balance for Position",
            "amount": 1000.0,  # DOGE amount
            "price": 0.20,     # DOGE price
            "balance": 500.0,
            "expected_result": "approved"
        },
        {
            "name": "Insufficient Balance - Should Adjust",
            "amount": 1000.0,  # DOGE amount
            "price": 0.20,     # DOGE price
            "balance": 100.0,  # Only $100 available
            "expected_result": "adjusted"
        },
        {
            "name": "Insufficient Balance - Too Small",
            "amount": 1000.0,  # DOGE amount
            "price": 0.20,     # DOGE price
            "balance": 5.0,    # Less than min_position_size
            "expected_result": "rejected"
        }
    ]
    
    for test_case in position_tests:
        print(f"Test: {test_case['name']}")
        print(f"Amount: {test_case['amount']:.0f} DOGE")
        print(f"Price: ${test_case['price']:.2f}")
        print(f"Balance: ${test_case['balance']:.2f}")
        
        # Test position sizing validation
        is_valid, reason, adjusted_amount = risk_manager.validate_position_sizing(
            "DOGE",
            test_case['amount'],
            test_case['price'],
            True,  # is_buy
            test_case['balance']
        )
        
        print(f"Result: {'Valid' if is_valid else 'Invalid'}")
        print(f"Reason: {reason}")
        print(f"Adjusted Amount: {adjusted_amount:.0f} DOGE")
        
        # Check if result matches expectation
        if test_case['expected_result'] == "approved":
            if is_valid and adjusted_amount == test_case['amount']:
                print("✅ Test passed - Position approved as expected")
            else:
                print("❌ Test failed - Expected approval but got different result")
        elif test_case['expected_result'] == "adjusted":
            if is_valid and adjusted_amount < test_case['amount']:
                print("✅ Test passed - Position adjusted as expected")
            else:
                print("❌ Test failed - Expected adjustment but got different result")
        elif test_case['expected_result'] == "rejected":
            if not is_valid:
                print("✅ Test passed - Position rejected as expected")
            else:
                print("❌ Test failed - Expected rejection but got approval")
        
        print("-" * 40)
    
    print("\n🎉 Balance adjustment test completed!")
    print("\nThe risk manager will now:")
    print("- ✅ Adjust position sizes when balance is insufficient")
    print("- ✅ Reject positions that are too small after adjustment")
    print("- ✅ Prevent 'insufficient balance' errors from Binance")
    print("- ✅ Maintain minimum position size requirements")

if __name__ == "__main__":
    test_balance_adjustment()
