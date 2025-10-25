#!/usr/bin/env python3
"""
Test script to verify interval parsing works correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import get_interval_seconds

def test_interval_parsing():
    """Test interval parsing with various formats."""
    print("Testing Interval Parsing...")
    
    test_cases = [
        ("5m", 300),  # 5 minutes = 300 seconds
        ("1h", 3600),  # 1 hour = 3600 seconds
        ("1d", 86400),  # 1 day = 86400 seconds
        ('"5m"', 300),  # With quotes
        ("'1h'", 3600),  # With single quotes
        ('"1d"', 86400),  # With quotes
        (" 5m ", 300),  # With spaces
        (' "5m" ', 300),  # With spaces and quotes
    ]
    
    for interval_str, expected_seconds in test_cases:
        try:
            result = get_interval_seconds(interval_str)
            if result == expected_seconds:
                print(f"✅ {interval_str} -> {result} seconds (expected {expected_seconds})")
            else:
                print(f"❌ {interval_str} -> {result} seconds (expected {expected_seconds})")
        except Exception as e:
            print(f"❌ {interval_str} -> Error: {e}")
    
    print("🎉 Interval parsing tests completed!")

if __name__ == "__main__":
    test_interval_parsing()
