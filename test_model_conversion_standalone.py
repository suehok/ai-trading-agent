#!/usr/bin/env python3
"""
Standalone test for model conversion logic (no external dependencies)
"""

def _get_valid_model(model: str) -> str:
    """Get a valid LLM model, with fallback for invalid models."""
    # Clean the model string (remove extra spaces and quotes)
    clean_model = model.strip().strip('"').strip("'")
    
    # Convert OpenRouter model format to DeepSeek API format if needed
    if clean_model.startswith("deepseek/deepseek-chat"):
        # Convert OpenRouter format to DeepSeek API format
        if clean_model == "deepseek/deepseek-chat-v3.1":
            return "deepseek-chat"
        elif clean_model == "deepseek/deepseek-chat-v3":
            return "deepseek-chat"
        elif clean_model == "deepseek/deepseek-chat":
            return "deepseek-chat"
    
    # List of invalid models that should be replaced
    invalid_models = [
        "deepseek/deepseek-chat-v2",  # OpenRouter invalid
        "deepseek/deepseek-coder",    # OpenRouter invalid
        "deepseek/deepseek-coder-v2", # OpenRouter invalid
        "deepseek/deepseek-llm",      # OpenRouter invalid
        "deepseek/deepseek-llm-v2",   # OpenRouter invalid
        "deepseek-chat-v2",           # DeepSeek API invalid
        "deepseek-coder",             # DeepSeek API invalid
        "deepseek-coder-v2",          # DeepSeek API invalid
        "deepseek-llm",               # DeepSeek API invalid
        "deepseek-llm-v2"             # DeepSeek API invalid
    ]
    
    # If the model is invalid, use a valid fallback
    if clean_model in invalid_models:
        print(f"Warning: Invalid model '{model}' (cleaned: '{clean_model}') detected. Using fallback 'deepseek-chat'")
        return "deepseek-chat"
    
    return clean_model

def test_model_conversion():
    """Test model conversion logic"""
    print("=== Testing Model Conversion Logic ===")
    
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

def main():
    """Run all tests"""
    print("Model Conversion Test (Standalone)")
    print("=" * 50)
    
    result = test_model_conversion()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    if result:
        print("✅ Model Conversion: PASSED")
        print("\n🎉 Model conversion is working correctly!")
        print("\nThe system will now automatically convert:")
        print("- 'deepseek/deepseek-chat-v3.1' -> 'deepseek-chat'")
        print("- 'deepseek/deepseek-chat-v3' -> 'deepseek-chat'")
        print("- 'deepseek/deepseek-chat' -> 'deepseek-chat'")
        print("\nThis should fix the 'Model Not Exist' error!")
    else:
        print("❌ Model Conversion: FAILED")
        print("Please check the model conversion logic.")
    
    return result

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
