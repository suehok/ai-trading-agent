# DeepSeek API Integration Guide

## Overview

The trading agent now supports direct integration with DeepSeek API, allowing you to use DeepSeek models without going through OpenRouter. This provides better performance, lower latency, and potentially lower costs.

## Configuration

### Environment Variables

To use DeepSeek API directly, set the following environment variables in your `.env` file:

```bash
# DeepSeek API Configuration
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

### Available Models

DeepSeek API supports the following models:

- `deepseek-chat` - DeepSeek-V3 model (recommended)
- `deepseek-reasoner` - DeepSeek-R1 model (for complex reasoning)
- `deepseek-chat-v3` - Alternative DeepSeek-V3 model

### Switching Between Providers

You can easily switch between DeepSeek API and OpenRouter by changing the `LLM_PROVIDER` setting:

#### For DeepSeek API:
```bash
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key_here
LLM_MODEL=deepseek-chat
```

#### For OpenRouter:
```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_MODEL=deepseek/deepseek-chat-v3.1
```

## Getting DeepSeek API Key

1. Visit [DeepSeek API](https://platform.deepseek.com/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Testing the Integration

Run the test script to verify your DeepSeek API integration:

```bash
python test_deepseek_api.py
```

This will test:
- Configuration validation
- TradingAgent initialization
- Model validation
- Actual API requests

## Benefits of Direct DeepSeek API

1. **Lower Latency**: Direct API calls without OpenRouter overhead
2. **Better Reliability**: Fewer points of failure
3. **Cost Efficiency**: Potentially lower costs than OpenRouter
4. **Latest Models**: Access to newest DeepSeek models immediately
5. **Better Support**: Direct support from DeepSeek team

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `DEEPSEEK_API_KEY` is set in your `.env` file
2. **Invalid Model**: Use `deepseek-chat` or `deepseek-reasoner` for DeepSeek API
3. **Network Issues**: Check your internet connection and firewall settings
4. **Rate Limits**: DeepSeek has rate limits; implement retry logic if needed

### Error Messages

- `DEEPSEEK_API_KEY is required when LLM_PROVIDER=deepseek`: Set your DeepSeek API key
- `Invalid model 'model_name' detected`: Use a valid DeepSeek model name
- `API request failed: 401`: Check your API key
- `API request failed: 429`: Rate limit exceeded, wait and retry

## Migration from OpenRouter

If you're currently using OpenRouter with DeepSeek models, migration is simple:

1. Get a DeepSeek API key
2. Update your `.env` file:
   ```bash
   LLM_PROVIDER=deepseek
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   LLM_MODEL=deepseek-chat
   ```
3. Remove or comment out OpenRouter settings
4. Test the integration

## Performance Comparison

| Provider | Latency | Cost | Reliability | Model Access |
|----------|---------|------|-------------|--------------|
| DeepSeek API | Low | Low | High | Latest |
| OpenRouter | Medium | Medium | Medium | Cached |

## Support

For issues with DeepSeek API integration:
1. Check the test script output
2. Review the logs in `llm_requests.log`
3. Verify your API key and configuration
4. Contact DeepSeek support for API-specific issues
