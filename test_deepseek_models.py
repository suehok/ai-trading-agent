#!/usr/bin/env python3
"""
Test script to check available DeepSeek models on OpenRouter
"""
import os
import json
import subprocess

def test_deepseek_models():
    """Test various DeepSeek model identifiers on OpenRouter."""
    print("Testing DeepSeek Models on OpenRouter...")
    
    # Get API key from .env file
    api_key = ""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test different DeepSeek model formats
    deepseek_models = [
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-chat-v3",
        "deepseek/deepseek-chat",
        "deepseek/deepseek-chat-v2",
        "deepseek/deepseek-coder",
        "deepseek/deepseek-coder-v2",
        "deepseek/deepseek-llm",
        "deepseek/deepseek-llm-v2"
    ]
    
    print(f"\n🧪 Testing {len(deepseek_models)} DeepSeek model variants...")
    
    for model in deepseek_models:
        print(f"\n📤 Testing model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        curl_command = f'''curl -s -w "\\n%{{http_code}}" \\
        -X POST "https://openrouter.ai/api/v1/chat/completions" \\
        -H "Authorization: Bearer {api_key}" \\
        -H "Content-Type: application/json" \\
        -d '{json.dumps(payload)}' \\
        --max-time 30'''
        
        try:
            result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=35)
            
            if result.returncode == 0:
                response_lines = result.stdout.strip().split('\n')
                status_code = response_lines[-1]
                response_body = '\n'.join(response_lines[:-1])
                
                if status_code == "200":
                    print(f"   ✅ {model}: VALID - Works!")
                    try:
                        response_data = json.loads(response_body)
                        if 'choices' in response_data and len(response_data['choices']) > 0:
                            content = response_data['choices'][0].get('message', {}).get('content', '')
                            print(f"      Response: {content[:50]}...")
                    except:
                        pass
                else:
                    print(f"   ❌ {model}: INVALID ({status_code})")
                    if "not a valid model ID" in response_body:
                        print(f"      Error: Model ID not recognized")
                    else:
                        print(f"      Error: {response_body[:100]}...")
            else:
                print(f"   ❌ {model}: Request failed")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {model}: Timeout")
        except Exception as e:
            print(f"   ❌ {model}: Error - {e}")

def test_alternative_models():
    """Test some alternative models that might work."""
    print("\n🧪 Testing alternative models...")
    
    api_key = ""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not api_key:
        return
    
    # Test some known working models
    alternative_models = [
        "x-ai/grok-4",
        "openai/gpt-4",
        "anthropic/claude-3.5-sonnet",
        "meta-llama/llama-3.1-8b-instruct"
    ]
    
    for model in alternative_models:
        print(f"\n📤 Testing alternative: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }
        
        curl_command = f'''curl -s -w "\\n%{{http_code}}" \\
        -X POST "https://openrouter.ai/api/v1/chat/completions" \\
        -H "Authorization: Bearer {api_key}" \\
        -H "Content-Type: application/json" \\
        -d '{json.dumps(payload)}' \\
        --max-time 15'''
        
        try:
            result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=20)
            
            if result.returncode == 0:
                response_lines = result.stdout.strip().split('\n')
                status_code = response_lines[-1]
                
                if status_code == "200":
                    print(f"   ✅ {model}: Works!")
                else:
                    print(f"   ❌ {model}: Failed ({status_code})")
            else:
                print(f"   ❌ {model}: Request failed")
                
        except Exception as e:
            print(f"   ❌ {model}: Error - {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("DEEPSEEK MODELS TEST ON OPENROUTER")
    print("=" * 70)
    
    test_deepseek_models()
    test_alternative_models()
    
    print("\n" + "=" * 70)
    print("🎉 DeepSeek models test completed!")
    print("=" * 70)
