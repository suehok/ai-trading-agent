#!/usr/bin/env python3
"""
Test script to verify model validation works correctly
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_validation():
    """Test model validation with various invalid models."""
    print("Testing Model Validation...")
    
    # Test cases: (invalid_model, expected_fallback)
    test_cases = [
        ("deepseek/deepseek-chat-v3.1", "x-ai/grok-4"),
        ("deepseek/deepseek-chat-v3", "x-ai/grok-4"),
        ("deepseek/deepseek-chat", "x-ai/grok-4"),
        ("x-ai/grok-4", "x-ai/grok-4"),  # Valid model should remain unchanged
        ("openai/gpt-4", "openai/gpt-4"),  # Other valid model should remain unchanged
    ]
    
    for invalid_model, expected_fallback in test_cases:
        # Set environment variable
        os.environ["LLM_MODEL"] = invalid_model
        
        # Import and test the validation function
        from src.config_loader import _get_valid_model
        result = _get_valid_model()
        
        if result == expected_fallback:
            print(f"✅ {invalid_model} -> {result} (expected {expected_fallback})")
        else:
            print(f"❌ {invalid_model} -> {result} (expected {expected_fallback})")
    
    # Test with no environment variable (should use default)
    if "LLM_MODEL" in os.environ:
        del os.environ["LLM_MODEL"]
    
    from src.config_loader import _get_valid_model
    result = _get_valid_model()
    if result == "x-ai/grok-4":
        print(f"✅ No env var -> {result} (expected x-ai/grok-4)")
    else:
        print(f"❌ No env var -> {result} (expected x-ai/grok-4)")
    
    print("🎉 Model validation tests completed!")

if __name__ == "__main__":
    test_model_validation()
