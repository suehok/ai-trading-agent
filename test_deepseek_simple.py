#!/usr/bin/env python3
"""
Simple test script for DeepSeek API integration (no external dependencies)
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_configuration():
    """Test configuration without external dependencies"""
    print("=== Testing DeepSeek API Configuration ===")
    
    # Check if we can import the config
    try:
        from config_loader import CONFIG
        print("✅ Config loader imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config loader: {e}")
        return False
    
    # Check provider setting
    provider = CONFIG.get("llm_provider", "deepseek")
    print(f"✅ LLM Provider: {provider}")
    
    # Check model setting
    model = CONFIG.get("llm_model", "deepseek-chat")
    print(f"✅ LLM Model: {model}")
    
    # Check base URL
    base_url = CONFIG.get("deepseek_base_url", "https://api.deepseek.com")
    print(f"✅ DeepSeek Base URL: {base_url}")
    
    # Check if API key is configured (don't print the actual key)
    api_key = CONFIG.get("deepseek_api_key")
    if api_key:
        print(f"✅ DeepSeek API Key: {api_key[:10]}...")
    else:
        print("⚠️  DeepSeek API Key not configured (set DEEPSEEK_API_KEY)")
    
    return True

def test_model_validation():
    """Test model validation for DeepSeek models"""
    print("\n=== Testing Model Validation ===")
    
    try:
        from agent.decision_maker import _get_valid_model
        print("✅ Model validation function imported successfully")
    except Exception as e:
        print(f"❌ Failed to import model validation: {e}")
        return False
    
    test_cases = [
        ("deepseek-chat", "deepseek-chat"),  # Valid DeepSeek model
        ("deepseek-chat-v3", "deepseek-chat-v3"),  # Valid DeepSeek model
        ("deepseek-reasoner", "deepseek-reasoner"),  # Valid DeepSeek model
        ("deepseek-chat-v2", "deepseek-chat"),  # Invalid -> fallback
        ("deepseek-coder", "deepseek-chat"),  # Invalid -> fallback
        ("deepseek/deepseek-chat", "deepseek/deepseek-chat"),  # Valid OpenRouter model
        ("deepseek/deepseek-chat-v3.1", "deepseek/deepseek-chat-v3.1"),  # Valid OpenRouter model
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

def test_trading_agent_initialization():
    """Test TradingAgent initialization with DeepSeek"""
    print("\n=== Testing TradingAgent Initialization ===")
    
    try:
        from agent.decision_maker import TradingAgent
        print("✅ TradingAgent class imported successfully")
    except Exception as e:
        print(f"❌ Failed to import TradingAgent: {e}")
        return False
    
    # Test initialization (this might fail if API key is not set, which is expected)
    try:
        agent = TradingAgent()
        print(f"✅ TradingAgent initialized successfully")
        print(f"✅ Provider: {agent.provider}")
        print(f"✅ Model: {agent.model}")
        print(f"✅ Base URL: {agent.base_url}")
        
        return True
    except RuntimeError as e:
        if "DEEPSEEK_API_KEY is required" in str(e):
            print("⚠️  TradingAgent initialization requires DEEPSEEK_API_KEY")
            print("   This is expected if the API key is not set")
            return True  # This is expected behavior
        else:
            print(f"❌ TradingAgent initialization failed: {e}")
            return False
    except Exception as e:
        print(f"❌ TradingAgent initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("DeepSeek API Integration Test (Simple)")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Model Validation", test_model_validation),
        ("Agent Initialization", test_trading_agent_initialization),
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
        print("🎉 All tests passed! DeepSeek API integration is configured correctly.")
        print("\nTo complete the setup:")
        print("1. Get a DeepSeek API key from https://platform.deepseek.com/")
        print("2. Set DEEPSEEK_API_KEY in your .env file")
        print("3. Run the full test with: python test_deepseek_api.py")
    else:
        print("❌ Some tests failed. Please check the configuration and try again.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
