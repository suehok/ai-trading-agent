#!/usr/bin/env python3
"""
Test script to verify decision maker model validation works
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_decision_maker_validation():
    """Test decision maker model validation."""
    print("Testing Decision Maker Model Validation...")
    
    # Test the validation function directly
    from src.agent.decision_maker import _get_valid_model
    
    test_cases = [
        ("deepseek/deepseek-chat-v3.1", "x-ai/grok-4"),
        ("deepseek/deepseek-chat-v3", "x-ai/grok-4"),
        ("deepseek/deepseek-chat", "x-ai/grok-4"),
        ("x-ai/grok-4", "x-ai/grok-4"),
        ("openai/gpt-4", "openai/gpt-4"),
    ]
    
    for invalid_model, expected_fallback in test_cases:
        result = _get_valid_model(invalid_model)
        
        if result == expected_fallback:
            print(f"✅ {invalid_model} -> {result} (expected {expected_fallback})")
        else:
            print(f"❌ {invalid_model} -> {result} (expected {expected_fallback})")
    
    print("🎉 Decision maker model validation tests completed!")

if __name__ == "__main__":
    test_decision_maker_validation()
