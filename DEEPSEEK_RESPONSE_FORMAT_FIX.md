# DeepSeek API Response Format Fix

## Problem Solved ✅

The error `400 - {"error":{"message":"This response_format type is unavailable now","type":"invalid_request_error","param":null,"code":"invalid_request_error"}}` was occurring because:

1. **DeepSeek API Doesn't Support Structured Outputs**: DeepSeek API doesn't support the `response_format` parameter
2. **OpenRouter vs DeepSeek API Differences**: OpenRouter supports structured outputs, but DeepSeek API doesn't
3. **Provider-Agnostic Code**: The code was using `response_format` regardless of the provider

## Solution Implemented ✅

### **Provider-Aware Structured Outputs**

Made the structured output feature provider-aware to only use `response_format` when supported:

#### **1. Conditional Response Format Usage**
```python
# Only use structured outputs for providers that support it (OpenRouter)
if allow_structured and self.provider == "openrouter":
    data["response_format"] = {
        "type": "json_schema",
        "json_schema": {
            "name": "trade_decisions",
            "strict": True,
            "schema": _build_schema(),
        },
    }
```

#### **2. Provider-Specific Sanitizer Models**
```python
# Fast/cheap sanitizer model to normalize outputs on parse failures
if self.provider == "deepseek":
    self.sanitize_model = CONFIG.get("sanitize_model") or "deepseek-chat"
else:
    self.sanitize_model = CONFIG.get("sanitize_model") or "openai/gpt-3.5-turbo"
```

#### **3. Enhanced JSON Output Instructions**
```python
"Output contract\n"
"- Output STRICT JSON array (no Markdown, no extra text), one object per asset in the SAME ORDER as the provided assets list.\n"
"- Exact keys for each object: {asset, action, allocation_usd, tp_price, sl_price, exit_plan, rationale}\n"
"- CRITICAL: Return ONLY valid JSON array, no additional text or formatting.\n"
```

### **Provider-Specific Behavior**

| Feature | DeepSeek API | OpenRouter API |
|---------|-------------|----------------|
| **Structured Outputs** | ❌ Not Supported | ✅ Supported |
| **Response Format** | ❌ Not Used | ✅ Used |
| **JSON Schema** | ❌ Not Used | ✅ Used |
| **Sanitizer Model** | `deepseek-chat` | `openai/gpt-3.5-turbo` |
| **JSON Instructions** | ✅ Enhanced | ✅ Standard |

### **How It Works**

#### **DeepSeek API Flow:**
1. **No Response Format**: Skips `response_format` parameter entirely
2. **Enhanced Instructions**: Uses stronger JSON output instructions in system prompt
3. **Fallback Parsing**: Relies on JSON parsing and sanitizer for output normalization
4. **DeepSeek Sanitizer**: Uses `deepseek-chat` for output sanitization

#### **OpenRouter API Flow:**
1. **Response Format**: Uses `response_format` with JSON schema
2. **Structured Outputs**: Leverages structured output capabilities
3. **Standard Instructions**: Uses standard JSON output instructions
4. **OpenAI Sanitizer**: Uses `openai/gpt-3.5-turbo` for output sanitization

## Testing Results ✅

```bash
python3 test_deepseek_compatibility.py
```

**Results**: ✅ All test cases passed
- ✅ DeepSeek API correctly excludes response_format
- ✅ OpenRouter API correctly includes response_format
- ✅ Provider-specific sanitizer models work correctly
- ✅ Provider detection works correctly

## Expected Results

The trading agent will now:

- ✅ **No More "Response Format Unavailable" Errors**: DeepSeek API requests won't include unsupported parameters
- ✅ **Provider-Specific Optimization**: Each provider uses its optimal features
- ✅ **Backward Compatibility**: OpenRouter functionality remains unchanged
- ✅ **Enhanced JSON Parsing**: Better JSON output handling for DeepSeek API
- ✅ **Robust Error Handling**: Graceful fallback when structured outputs aren't supported

## Files Modified

### **`src/agent/decision_maker.py`**
- ✅ Added provider-aware structured output logic
- ✅ Updated sanitizer model selection based on provider
- ✅ Enhanced JSON output instructions for DeepSeek API
- ✅ Improved error handling for provider-specific features

### **Test Files**
- ✅ `test_deepseek_compatibility.py`: Comprehensive compatibility test

## Summary

**Complete Solution**: Provider-aware feature usage for optimal API compatibility

1. **Conditional Features**: Only use features supported by each provider
2. **Enhanced Instructions**: Stronger JSON output instructions for providers without structured outputs
3. **Provider-Specific Models**: Use appropriate models for each provider's capabilities
4. **Robust Fallbacks**: Graceful handling when advanced features aren't available
5. **Comprehensive Testing**: Verified compatibility with both providers

**The "Response Format Unavailable" error is now fixed!** 🎉

The system automatically adapts its behavior based on the provider:
- **DeepSeek API**: Uses enhanced JSON instructions and parsing
- **OpenRouter API**: Uses structured outputs and JSON schema

This ensures optimal performance and compatibility with both providers while preventing API errors.
