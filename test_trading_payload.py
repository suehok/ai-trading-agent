#!/usr/bin/env python3
"""
Test script to diagnose the trading agent's OpenRouter payload
"""
import os
import json
import time

def test_trading_payload():
    """Test the exact payload that the trading agent sends."""
    print("Testing Trading Agent Payload...")
    
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
    
    # Simulate a typical trading agent payload
    payload = {
        "model": "x-ai/grok-4",
        "messages": [
            {
                "role": "system",
                "content": "You are a rigorous QUANTITATIVE TRADER and interdisciplinary MATHEMATICIAN-ENGINEER optimizing risk-adjusted returns for perpetual futures under real execution, margin, and funding constraints.\nYou will receive market + account context for SEVERAL assets, including:\n- assets = [\"BTC\", \"ETH\", \"SOL\", \"BNB\", \"ZEC\", \"EIGEN\"]\n- per-asset intraday (5m) and higher-timeframe (4h) metrics\n- Active Trades with Exit Plans\n- Account state (balance, positions, risk metrics)\n\nFor EACH asset, decide: BUY, SELL, or HOLD with precise reasoning.\n\nReturn ONLY a JSON array of objects:\n[{\"asset\": \"BTC\", \"action\": \"BUY\", \"reasoning\": \"...\"}, ...]\n\nBe concise but thorough in reasoning."
            },
            {
                "role": "user", 
                "content": "Market data for BTC, ETH, SOL, BNB, ZEC, EIGEN with technical indicators and account state."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.1
    }
    
    print(f"📤 Payload size: {len(json.dumps(payload))} characters")
    print(f"📤 Messages: {len(payload['messages'])} message(s)")
    print(f"📤 Model: {payload['model']}")
    print(f"📤 Max tokens: {payload['max_tokens']}")
    
    # Test with curl
    print("\n🧪 Testing with curl...")
    
    curl_command = f'''curl -s -w "\\n%{{http_code}}" \\
    -X POST "https://openrouter.ai/api/v1/chat/completions" \\
    -H "Authorization: Bearer {api_key}" \\
    -H "Content-Type: application/json" \\
    -d '{json.dumps(payload)}' \\
    --max-time 60'''
    
    print("⏳ Making request...")
    start_time = time.time()
    
    import subprocess
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=70)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Request completed in {duration:.2f} seconds")
        
        if result.returncode == 0:
            response_lines = result.stdout.strip().split('\n')
            status_code = response_lines[-1]
            response_body = '\n'.join(response_lines[:-1])
            
            print(f"📊 Status Code: {status_code}")
            
            if status_code == "200":
                print("✅ Request successful!")
                try:
                    response_data = json.loads(response_body)
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0].get('message', {}).get('content', '')
                        print(f"📝 Response content: {content[:200]}...")
                    else:
                        print(f"📝 Full response: {response_body[:200]}...")
                except json.JSONDecodeError:
                    print(f"📝 Raw response: {response_body[:200]}...")
            else:
                print(f"❌ Request failed with status {status_code}")
                print(f"📝 Error response: {response_body}")
        else:
            print(f"❌ Curl command failed with return code {result.returncode}")
            print(f"📝 Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Request timed out after 70 seconds")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_simplified_payload():
    """Test with a simplified payload to isolate the issue."""
    print("\n🧪 Testing with simplified payload...")
    
    # Get API key
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
    
    # Simplified payload
    simple_payload = {
        "model": "x-ai/grok-4",
        "messages": [
            {"role": "user", "content": "Hello, respond with just 'Hi'"}
        ],
        "max_tokens": 10
    }
    
    curl_command = f'''curl -s -w "\\n%{{http_code}}" \\
    -X POST "https://openrouter.ai/api/v1/chat/completions" \\
    -H "Authorization: Bearer {api_key}" \\
    -H "Content-Type: application/json" \\
    -d '{json.dumps(simple_payload)}' \\
    --max-time 30'''
    
    print("⏳ Making simplified request...")
    start_time = time.time()
    
    import subprocess
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True, timeout=35)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Request completed in {duration:.2f} seconds")
        
        if result.returncode == 0:
            response_lines = result.stdout.strip().split('\n')
            status_code = response_lines[-1]
            response_body = '\n'.join(response_lines[:-1])
            
            print(f"📊 Status Code: {status_code}")
            if status_code == "200":
                print("✅ Simplified request successful!")
                print(f"📝 Response: {response_body[:100]}...")
            else:
                print(f"❌ Simplified request failed: {response_body}")
        else:
            print(f"❌ Simplified request failed with return code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("❌ Simplified request timed out")
    except Exception as e:
        print(f"❌ Simplified request error: {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("TRADING AGENT PAYLOAD DIAGNOSTIC TEST")
    print("=" * 70)
    
    test_trading_payload()
    test_simplified_payload()
    
    print("\n" + "=" * 70)
    print("🎉 Payload diagnostic test completed!")
    print("=" * 70)
