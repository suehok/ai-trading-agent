#!/usr/bin/env python3
"""
Test script to diagnose OpenRouter API issues
"""
import requests
import json
import time
import os

def test_openrouter_connection():
    """Test OpenRouter API connection with minimal request."""
    print("Testing OpenRouter API Connection...")
    
    # Load API key from environment or .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Try to read from .env file
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    
    if not api_key:
        print("❌ No OpenRouter API key found!")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test with minimal request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Minimal payload
    payload = {
        "model": "x-ai/grok-4",
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }
    
    print(f"📤 Sending request to: {url}")
    print(f"📤 Model: {payload['model']}")
    print(f"📤 Messages: {len(payload['messages'])} message(s)")
    
    try:
        print("⏳ Making request...")
        start_time = time.time()
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Request completed in {duration:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            try:
                data = response.json()
                print(f"📝 Response: {data.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
                return True
            except json.JSONDecodeError:
                print("⚠️  Response is not valid JSON")
                print(f"📝 Raw response: {response.text[:200]}...")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"📝 Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet connection")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_alternative_models():
    """Test with alternative models to see if it's model-specific."""
    print("\nTesting Alternative Models...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not api_key:
        print("❌ No API key found")
        return
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Test different models
    models_to_test = [
        "x-ai/grok-4",
        "openai/gpt-4",
        "anthropic/claude-3.5-sonnet",
        "meta-llama/llama-3.1-8b-instruct"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Testing model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }
        
        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                print(f"   ✅ {model}: Success ({duration:.2f}s)")
            else:
                print(f"   ❌ {model}: Failed ({response.status_code}) - {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ {model}: Timeout")
        except Exception as e:
            print(f"   ❌ {model}: Error - {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("OPENROUTER API DIAGNOSTIC TEST")
    print("=" * 60)
    
    # Test basic connection
    success = test_openrouter_connection()
    
    if not success:
        print("\n🔍 Testing alternative models...")
        test_alternative_models()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 OpenRouter API is working correctly!")
    else:
        print("⚠️  OpenRouter API has issues - check the diagnostics above")
    print("=" * 60)
