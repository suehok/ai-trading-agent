#!/usr/bin/env python3
"""
Test script to verify model conversion from OpenRouter format to DeepSeek API format
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_model_conversion():
    """Test model conversion logic"""
    print("=== Testing Model Conversion Logic ===")
    
    try:
        from agent.decision_maker import _get_valid_model
        print("✅ Model validation function imported successfully")
    except Exception as e:
        print(f"❌ Failed to import model validation: {e}")
        return False
    
    # Test cases for model conversion
    test_cases = [
        # OpenRouter format -> DeepSeek API format
        ("deepseek/deepseek-chat-v3.1", "deepseek-chat"),
        ("deepseek/deepseek-chat-v3", "deepseek-chat"),
        ("deepseek/deepseek-chat", "deepseek-chat"),
        
        # DeepSeek API format (should remain unchanged)
        ("deepseek-chat", "deepseek-chat"),
        ("deepseek-reasoner", "deepseek-reasoner"),
        
        # Invalid models -> fallback
        ("deepseek-chat-v2", "deepseek-chat"),
        ("deepseek-coder", "deepseek-chat"),
        ("deepseek/deepseek-chat-v2", "deepseek-chat"),
        
        # Other models (should remain unchanged)
        ("openai/gpt-4", "openai/gpt-4"),
        ("x-ai/grok-4", "x-ai/grok-4"),
    ]
    
    all_passed = True
    for input_model, expected_output in test_cases:
        result = _get_valid_model(input_model)
        if result == expected_output:
            print(f"✅ '{input_model}' -> '{result}'")
        else:
            print(f"❌ '{input_model}' -> '{result}' (expected '{expected_output}')")
            all_passed = False
    
    return all_passed

def test_config_model_conversion():
    """Test configuration-level model conversion"""
    print("\n=== Testing Configuration Model Conversion ===")
    
    try:
        from config_loader import _get_valid_model
        print("✅ Config model validation function imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config model validation: {e}")
        return False
    
    # Test cases for configuration model conversion
    test_cases = [
        # OpenRouter format -> DeepSeek API format
        ("deepseek/deepseek-chat-v3.1", "deepseek-chat"),
        ("deepseek/deepseek-chat-v3", "deepseek-chat"),
        ("deepseek/deepseek-chat", "deepseek-chat"),
        
        # DeepSeek API format (should remain unchanged)
        ("deepseek-chat", "deepseek-chat"),
        ("deepseek-reasoner", "deepseek-reasoner"),
        
        # Invalid models -> fallback
        ("deepseek-chat-v2", "deepseek-chat"),
        ("deepseek-coder", "deepseek-chat"),
        ("deepseek/deepseek-chat-v2", "deepseek-chat"),
    ]
    
    all_passed = True
    for input_model, expected_output in test_cases:
        result = _get_valid_model(input_model)
        if result == expected_output:
            print(f"✅ '{input_model}' -> '{result}'")
        else:
            print(f"❌ '{input_model}' -> '{result}' (expected '{expected_output}')")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("Model Conversion Test")
    print("=" * 50)
    
    tests = [
        ("Decision Maker Model Conversion", test_model_conversion),
        ("Config Model Conversion", test_config_model_conversion),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Model conversion is working correctly.")
        print("\nThe system will now automatically convert:")
        print("- 'deepseek/deepseek-chat-v3.1' -> 'deepseek-chat'")
        print("- 'deepseek/deepseek-chat-v3' -> 'deepseek-chat'")
        print("- 'deepseek/deepseek-chat' -> 'deepseek-chat'")
        print("\nThis should fix the 'Model Not Exist' error!")
    else:
        print("❌ Some tests failed. Please check the model conversion logic.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
