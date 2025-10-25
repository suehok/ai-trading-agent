# Binance API Setup Guide

## Issues Fixed

The following issues have been resolved in the Binance API implementation:

### 1. Signature Generation
- **Problem**: HMAC signature was not being properly included in requests
- **Fix**: Added signature to request parameters and improved error handling

### 2. Symbol Formatting
- **Problem**: Extra quotes and malformed symbols (e.g., `"BTCUSDT"` instead of `BTCUSDT`)
- **Fix**: Added proper symbol cleaning and formatting

### 3. API Endpoint Issues
- **Problem**: Some endpoints returning 404 errors
- **Fix**: Improved error handling and request formatting

## Configuration

### Required Environment Variables

```bash
# Trading Platform
TRADING_PLATFORM=binance

# Binance API Credentials
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=false  # Set to true for testnet

# Risk Management (Optional)
MAX_TOTAL_ALLOCATION=1000.0
MAX_SINGLE_POSITION=500.0
MAX_DAILY_LOSS=100.0
MAX_LEVERAGE=5.0
MIN_POSITION_SIZE=10.0
```

### Getting Binance API Keys

1. **Create Binance Account**: Go to [binance.com](https://binance.com)
2. **Enable API**: Go to Account → API Management
3. **Create API Key**: 
   - Enable "Enable Spot & Margin Trading" for spot trading
   - Enable "Enable Futures" for futures trading
   - **Important**: Restrict IP addresses for security
4. **Copy Credentials**: Save your API Key and Secret Key

### Security Best Practices

- **IP Restrictions**: Always restrict API keys to specific IP addresses
- **Minimal Permissions**: Only enable required permissions
- **Regular Rotation**: Rotate API keys periodically
- **Testnet First**: Test with `BINANCE_TESTNET=true` before using mainnet

## Testing

Run the test script to verify your setup:

```bash
python test_binance_fix.py
```

## Common Issues

### 1. "Mandatory parameter 'signature' was not sent"
- **Cause**: API key/secret not configured or signature generation failed
- **Fix**: Check your `.env` file has correct `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`

### 2. "Illegal characters found in parameter 'symbol'"
- **Cause**: Symbol formatting issues
- **Fix**: Updated symbol cleaning in the API client

### 3. "404 Not Found" for open interest/funding
- **Cause**: Some assets may not have futures contracts
- **Fix**: The API now handles this gracefully and returns None

### 4. TAAPI Authentication Errors
- **Cause**: TAAPI API key format issues
- **Fix**: Ensure your TAAPI_API_KEY is the correct format (not a JWT token)

## Usage

Once configured, run the trading agent:

```bash
# Using Poetry
poetry run python src/main.py --assets BTC ETH --interval 1h

# Using Docker
docker run --rm -p 3000:3000 --env-file .env trading-agent
```

The agent will now use Binance as the trading platform with full risk management controls.
