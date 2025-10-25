#!/bin/bash
# Test OpenRouter API using curl

echo "============================================================"
echo "OPENROUTER API DIAGNOSTIC TEST (using curl)"
echo "============================================================"

# Get API key from .env file
API_KEY=""
if [ -f ".env" ]; then
    API_KEY=$(grep "OPENROUTER_API_KEY=" .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

if [ -z "$API_KEY" ]; then
    echo "❌ No OpenRouter API key found in .env file!"
    exit 1
fi

echo "✅ API Key found: ${API_KEY:0:10}..."

# Test with minimal request
echo ""
echo "🧪 Testing OpenRouter API with x-ai/grok-4..."
echo "⏳ Making request..."

start_time=$(date +%s)

response=$(curl -s -w "\n%{http_code}" \
    -X POST "https://openrouter.ai/api/v1/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "x-ai/grok-4",
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }' \
    --max-time 30)

end_time=$(date +%s)
duration=$((end_time - start_time))

echo "⏱️  Request completed in ${duration} seconds"

# Extract status code and response body
status_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

echo "📊 Status Code: $status_code"

if [ "$status_code" = "200" ]; then
    echo "✅ Request successful!"
    echo "📝 Response: $response_body"
else
    echo "❌ Request failed with status $status_code"
    echo "📝 Error response: $response_body"
fi

echo ""
echo "🧪 Testing with alternative model (openai/gpt-4)..."

response2=$(curl -s -w "\n%{http_code}" \
    -X POST "https://openrouter.ai/api/v1/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "openai/gpt-4",
        "messages": [
            {"role": "user", "content": "Hi"}
        ],
        "max_tokens": 5
    }' \
    --max-time 15)

status_code2=$(echo "$response2" | tail -n1)
response_body2=$(echo "$response2" | head -n -1)

echo "📊 Status Code: $status_code2"
if [ "$status_code2" = "200" ]; then
    echo "✅ Alternative model works!"
else
    echo "❌ Alternative model also failed: $response_body2"
fi

echo ""
echo "============================================================"
if [ "$status_code" = "200" ]; then
    echo "🎉 OpenRouter API is working correctly!"
else
    echo "⚠️  OpenRouter API has issues - check the diagnostics above"
fi
echo "============================================================"
