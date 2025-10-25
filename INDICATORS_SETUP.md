# Technical Indicators Setup Guide

## Problem Solved

The TAAPI authentication errors were caused by an invalid API key format. The system now supports two indicator providers:

1. **TAAPI** (external service) - for Hyperliquid platform
2. **Binance Indicators** (built-in) - for Binance platform

## Configuration Options

### Option 1: Use Binance Indicators (Recommended for Binance)

When using `TRADING_PLATFORM=binance`, the system automatically uses Binance's built-in indicators:

```bash
# .env configuration
TRADING_PLATFORM=binance
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

# TAAPI_API_KEY is not required
```

**Advantages:**
- ✅ No external API dependencies
- ✅ No rate limits or costs
- ✅ Always available
- ✅ Real-time data from Binance

### Option 2: Use TAAPI (For Hyperliquid)

When using `TRADING_PLATFORM=hyperliquid`, the system uses TAAPI:

```bash
# .env configuration
TRADING_PLATFORM=hyperliquid
HYPERLIQUID_PRIVATE_KEY=your_private_key
TAAPI_API_KEY=your_correct_taapi_key  # Must be a valid API key, not JWT token

# Binance credentials not required
```

## Fixed Issues

### 1. TAAPI Authentication
- **Problem**: JWT token was being used instead of API key
- **Solution**: System now validates API key format and provides clear error messages

### 2. Platform-Specific Indicators
- **Problem**: Same indicator client for all platforms
- **Solution**: Automatic selection based on trading platform

### 3. Missing Indicators
- **Problem**: Some indicators not available in Binance
- **Solution**: Graceful fallback and clear error messages

## Testing

### Test Binance Indicators
```bash
python test_binance_indicators.py
```

### Test TAAPI (if configured)
```bash
python test_binance_fix.py  # This will test the overall system
```

## Supported Indicators

### Binance Indicators
- ✅ EMA (Exponential Moving Average)
- ✅ RSI (Relative Strength Index)
- ✅ MACD (Moving Average Convergence Divergence)
- ✅ SMA (Simple Moving Average)
- ✅ Bollinger Bands
- ❌ ATR (Average True Range) - Not implemented yet

### TAAPI Indicators
- ✅ All indicators supported by TAAPI
- ✅ ATR, ADX, and other advanced indicators
- ❌ Requires valid API key
- ❌ Rate limits apply

## Migration Guide

### From TAAPI to Binance Indicators

1. **Update your .env file:**
   ```bash
   TRADING_PLATFORM=binance
   # Remove or comment out TAAPI_API_KEY
   ```

2. **Test the setup:**
   ```bash
   python test_binance_indicators.py
   ```

3. **Run the trading agent:**
   ```bash
   python src/main.py --assets BTC ETH --interval 1h
   ```

### From Binance to TAAPI

1. **Get a valid TAAPI API key:**
   - Go to [taapi.io](https://taapi.io/)
   - Sign up and get a proper API key (not JWT token)

2. **Update your .env file:**
   ```bash
   TRADING_PLATFORM=hyperliquid
   TAAPI_API_KEY=your_valid_taapi_key
   ```

3. **Test the setup:**
   ```bash
   python test_binance_fix.py
   ```

## Error Handling

The system now handles indicator failures gracefully:

- **Missing indicators**: Returns "N/A" instead of crashing
- **API failures**: Logs errors and continues trading
- **Invalid data**: Validates data before using

## Performance

### Binance Indicators
- **Speed**: Fast (no external API calls for indicators)
- **Reliability**: High (uses Binance's own data)
- **Cost**: Free

### TAAPI
- **Speed**: Slower (external API calls)
- **Reliability**: Depends on TAAPI service
- **Cost**: Requires paid subscription for high usage

## Recommendation

**For Binance trading**: Use Binance indicators (automatic)
**For Hyperliquid trading**: Use TAAPI (requires valid API key)

The system will automatically choose the appropriate indicator provider based on your trading platform configuration.
