# How to Enable Binance Futures Trading

## Quick Setup Guide

### 1. Update Your .env File

Add these lines to your `.env` file:

```bash
# Enable Futures Trading
BINANCE_FUTURES_ENABLED=true
BINANCE_FUTURES_LEVERAGE=5.0
BINANCE_FUTURES_MARGIN_TYPE=ISOLATED

# Keep existing settings
TRADING_PLATFORM=binance
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=false
```

### 2. Binance Account Setup

1. **Log into Binance**: Go to [binance.com](https://binance.com)
2. **Open Futures Account**: 
   - Go to Derivatives → Futures
   - Click "Open Futures Account"
   - Complete the risk assessment quiz
3. **Transfer Funds**: 
   - Go to Futures → Transfer
   - Transfer USDT from Spot to Futures wallet
4. **Enable API Permissions**:
   - Go to Account → API Management
   - Edit your API key
   - Enable "Enable Futures" permission

### 3. Test the Setup

Run the test script to verify everything works:

```bash
python test_futures_setup.py
```

### 4. Configuration Options

| Setting | Description | Options |
|---------|-------------|---------|
| `BINANCE_FUTURES_ENABLED` | Enable/disable futures | `true` / `false` |
| `BINANCE_FUTURES_LEVERAGE` | Default leverage | `1.0` to `125.0` |
| `BINANCE_FUTURES_MARGIN_TYPE` | Margin type | `ISOLATED` / `CROSSED` |

### 5. Risk Management

**Important**: Futures trading involves significant risk due to leverage.

- **Start Small**: Begin with small position sizes
- **Use Stop Losses**: Always set stop losses
- **Monitor Positions**: Watch your positions closely
- **Manage Leverage**: Don't use excessive leverage

### 6. Features Available with Futures

✅ **Leverage Trading**: Trade with up to 125x leverage
✅ **Long/Short Positions**: Take both long and short positions
✅ **Funding Rates**: Access to funding rate data
✅ **Open Interest**: Monitor market sentiment
✅ **Position Management**: Advanced position controls
✅ **Margin Management**: Isolated or cross margin

### 7. Common Issues

#### "Futures account not opened"
- **Solution**: Complete the futures account setup and quiz on Binance

#### "Insufficient margin"
- **Solution**: Transfer more funds to your futures wallet

#### "Leverage too high"
- **Solution**: Reduce the `BINANCE_FUTURES_LEVERAGE` setting

#### "API permission denied"
- **Solution**: Enable "Enable Futures" in your API key settings

### 8. Testing with Testnet

For safe testing, use the testnet:

```bash
# In your .env file
BINANCE_TESTNET=true
BINANCE_FUTURES_ENABLED=true
```

### 9. Example Configuration

```bash
# Complete .env configuration for futures
TRADING_PLATFORM=binance
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=false

# Futures Configuration
BINANCE_FUTURES_ENABLED=true
BINANCE_FUTURES_LEVERAGE=5.0
BINANCE_FUTURES_MARGIN_TYPE=ISOLATED

# Risk Management
MAX_TOTAL_ALLOCATION=1000.0
MAX_SINGLE_POSITION=200.0
MAX_DAILY_LOSS=100.0
MAX_LEVERAGE=5.0
MIN_POSITION_SIZE=10.0
```

### 10. Next Steps

1. **Enable Futures**: Set `BINANCE_FUTURES_ENABLED=true`
2. **Configure API**: Enable futures permissions in Binance
3. **Test Setup**: Run `python test_futures_setup.py`
4. **Start Trading**: Run the trading agent with futures enabled
5. **Monitor Risk**: Watch positions and PnL closely

## Summary

Futures trading is now supported! Simply set `BINANCE_FUTURES_ENABLED=true` in your `.env` file and ensure your Binance account has futures enabled with proper API permissions.

**Remember**: Futures trading involves significant risk due to leverage. Always use proper risk management and start with small amounts.
