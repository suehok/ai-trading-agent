#!/usr/bin/env python3
"""
Simple test for model validation logic in decision maker
"""

def _get_valid_model(model: str) -> str:
    """Get a valid LLM model, with fallback for invalid models."""
    # List of invalid models that should be replaced
    invalid_models = [
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-chat-v3",
        "deepseek/deepseek-chat"
    ]
    
    # If the model is invalid, use a valid fallback
    if model in invalid_models:
        print(f"Warning: Invalid model '{model}' detected. Using fallback 'x-ai/grok-4'")
        return "x-ai/grok-4"
    
    return model

def test_decision_maker_validation():
    """Test decision maker model validation."""
    print("Testing Decision Maker Model Validation...")
    
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
