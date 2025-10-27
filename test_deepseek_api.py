#!/usr/bin/env python3
"""
Test script for DeepSeek API integration
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config_loader import CONFIG
from agent.decision_maker import TradingAgent

def test_deepseek_configuration():
    """Test DeepSeek API configuration"""
    print("=== Testing DeepSeek API Configuration ===")
    
    # Check if DeepSeek API key is set
    deepseek_api_key = CONFIG.get("deepseek_api_key")
    if not deepseek_api_key:
        print("❌ DEEPSEEK_API_KEY not found in environment variables")
        print("Please set DEEPSEEK_API_KEY in your .env file")
        return False
    
    print(f"✅ DEEPSEEK_API_KEY found: {deepseek_api_key[:10]}...")
    
    # Check provider setting
    provider = CONFIG.get("llm_provider", "deepseek")
    print(f"✅ LLM Provider: {provider}")
    
    # Check model setting
    model = CONFIG.get("llm_model", "deepseek-chat")
    print(f"✅ LLM Model: {model}")
    
    # Check base URL
    base_url = CONFIG.get("deepseek_base_url", "https://api.deepseek.com")
    print(f"✅ DeepSeek Base URL: {base_url}")
    
    return True

def test_trading_agent_initialization():
    """Test TradingAgent initialization with DeepSeek"""
    print("\n=== Testing TradingAgent Initialization ===")
    
    try:
        agent = TradingAgent()
        print(f"✅ TradingAgent initialized successfully")
        print(f"✅ Provider: {agent.provider}")
        print(f"✅ Model: {agent.model}")
        print(f"✅ Base URL: {agent.base_url}")
        print(f"✅ API Key: {agent.api_key[:10]}...")
        
        return True
    except Exception as e:
        print(f"❌ TradingAgent initialization failed: {e}")
        return False

def test_model_validation():
    """Test model validation for DeepSeek models"""
    print("\n=== Testing Model Validation ===")
    
    from agent.decision_maker import _get_valid_model
    
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

def test_api_request():
    """Test actual API request to DeepSeek"""
    print("\n=== Testing DeepSeek API Request ===")
    
    try:
        agent = TradingAgent()
        
        # Simple test request
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Please respond with 'Hello from DeepSeek!'"}
        ]
        
        payload = {
            "model": agent.model,
            "messages": test_messages,
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        headers = {
            "Authorization": f"Bearer {agent.api_key}",
            "Content-Type": "application/json",
        }
        
        import requests
        print(f"Making request to: {agent.base_url}")
        print(f"Using model: {agent.model}")
        
        response = requests.post(agent.base_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ API request successful!")
            print(f"✅ Response: {content}")
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API request failed with exception: {e}")
        return False

def main():
    """Run all tests"""
    print("DeepSeek API Integration Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    tests = [
        ("Configuration", test_deepseek_configuration),
        ("Agent Initialization", test_trading_agent_initialization),
        ("Model Validation", test_model_validation),
        ("API Request", test_api_request),
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
        print("🎉 All tests passed! DeepSeek API integration is working correctly.")
    else:
        print("❌ Some tests failed. Please check the configuration and try again.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
