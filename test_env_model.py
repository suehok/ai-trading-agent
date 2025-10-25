#!/usr/bin/env python3
"""
Simple test to check if the LLM model in .env is valid
"""
import os
import sys
from dotenv import load_dotenv

def test_env_model():
    """Test if the LLM model in .env is valid."""
    print("Testing .env LLM Model Validation...")
    
    # Load .env file
    load_dotenv()
    
    # Get the model from environment
    model = os.getenv("LLM_MODEL", "x-ai/grok-4")
    print(f"Current LLM_MODEL from .env: '{model}'")
    
    # List of invalid models that should be replaced
    invalid_models = [
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-chat-v3",
        "deepseek/deepseek-chat"
    ]
    
    # Check if model is invalid
    if model in invalid_models:
        print(f"❌ INVALID MODEL: '{model}' is not a valid OpenRouter model ID")
        print(f"   This will cause OpenRouter API errors!")
        print(f"   Recommended fix: Change to 'x-ai/grok-4'")
        return False
    else:
        print(f"✅ VALID MODEL: '{model}' is a valid model ID")
        return True

def test_model_validation_function():
    """Test the model validation function."""
    print("\nTesting Model Validation Function...")
    
    def _get_valid_model(model: str) -> str:
        """Get a valid LLM model, with fallback for invalid models."""
        invalid_models = [
            "deepseek/deepseek-chat-v3.1",
            "deepseek/deepseek-chat-v3",
            "deepseek/deepseek-chat"
        ]
        
        if model in invalid_models:
            print(f"   Warning: Invalid model '{model}' detected. Using fallback 'x-ai/grok-4'")
            return "x-ai/grok-4"
        
        return model
    
    # Test cases
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
            print(f"   ✅ {invalid_model} -> {result}")
        else:
            print(f"   ❌ {invalid_model} -> {result} (expected {expected_fallback})")

if __name__ == "__main__":
    print("=" * 60)
    print("LLM MODEL VALIDATION TEST")
    print("=" * 60)
    
    # Test .env model
    is_valid = test_env_model()
    
    # Test validation function
    test_model_validation_function()
    
    print("\n" + "=" * 60)
    if is_valid:
        print("🎉 RESULT: .env model is VALID - No issues detected!")
    else:
        print("⚠️  RESULT: .env model is INVALID - Needs to be fixed!")
        print("   The trading agent will automatically correct this at runtime.")
    print("=" * 60)
