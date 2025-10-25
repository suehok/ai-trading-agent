# Binance Futures Trading Setup Guide

## Overview

This guide explains how to enable and configure Binance futures trading in the AI trading agent.

## Prerequisites

### 1. Binance Account Setup
- **Create Account**: Sign up at [binance.com](https://binance.com)
- **Complete KYC**: Verify your identity (required for futures)
- **Enable Futures**: Go to Derivatives → Futures and open a futures account
- **Complete Quiz**: Pass the futures trading risk assessment quiz

### 2. API Key Configuration
- **Enable Futures Permission**: In API Management, enable "Enable Futures"
- **Security**: Restrict IP addresses and use minimal required permissions
- **Testnet**: Use `BINANCE_TESTNET=true` for testing

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Trading Platform
TRADING_PLATFORM=binance

# Binance API Credentials
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
BINANCE_TESTNET=false  # Set to true for testnet

# Futures Trading Configuration
BINANCE_FUTURES_ENABLED=true
BINANCE_FUTURES_LEVERAGE=5.0  # Default leverage (1-125x)
BINANCE_FUTURES_MARGIN_TYPE=ISOLATED  # ISOLATED or CROSSED

# Risk Management
MAX_TOTAL_ALLOCATION=1000.0
MAX_SINGLE_POSITION=500.0
MAX_DAILY_LOSS=100.0
MAX_LEVERAGE=5.0
MIN_POSITION_SIZE=10.0
```

### API Key Permissions Required

In Binance API Management, enable:
- ✅ **Enable Spot & Margin Trading** (for spot trading)
- ✅ **Enable Futures** (for futures trading)
- ✅ **Enable Reading** (for account info)

## Implementation Changes Needed

### 1. Update Binance API Class

The current implementation uses spot endpoints. For futures, we need to:

```python
# Current (Spot)
self.base_url = "https://api.binance.com"

# Futures
self.futures_base_url = "https://fapi.binance.com"  # Futures API
self.futures_ws_url = "wss://fstream.binance.com/ws"  # Futures WebSocket
```

### 2. Futures-Specific Endpoints

| Feature | Spot Endpoint | Futures Endpoint |
|---------|---------------|------------------|
| Account Info | `/api/v3/account` | `/fapi/v2/account` |
| Place Order | `/api/v3/order` | `/fapi/v1/order` |
| Open Orders | `/api/v3/openOrders` | `/fapi/v1/openOrders` |
| Position Info | N/A | `/fapi/v2/positionRisk` |
| Funding Rate | N/A | `/fapi/v1/premiumIndex` |
| Open Interest | N/A | `/fapi/v1/openInterest` |

### 3. Futures-Specific Features

- **Leverage**: Set leverage per symbol
- **Margin Type**: ISOLATED or CROSSED
- **Position Management**: Long/Short positions
- **Funding Rates**: Pay/receive funding
- **Open Interest**: Available for analysis

## Code Modifications Required

### 1. Add Futures Configuration

```python
# In config_loader.py
CONFIG = {
    # ... existing config ...
    "binance_futures_enabled": _get_env("BINANCE_FUTURES_ENABLED", "false"),
    "binance_futures_leverage": _get_env("BINANCE_FUTURES_LEVERAGE", "5.0"),
    "binance_futures_margin_type": _get_env("BINANCE_FUTURES_MARGIN_TYPE", "ISOLATED"),
}
```

### 2. Update BinanceAPI Class

```python
class BinanceAPI(BaseTradingAPI):
    def __init__(self):
        # ... existing init ...
        self.futures_enabled = CONFIG.get("binance_futures_enabled", "false").lower() == "true"
        self.futures_leverage = float(CONFIG.get("binance_futures_leverage", "5.0"))
        self.futures_margin_type = CONFIG.get("binance_futures_margin_type", "ISOLATED")
        
        if self.futures_enabled:
            self.futures_base_url = "https://fapi.binance.com"
            self.futures_ws_url = "wss://fstream.binance.com/ws"
```

### 3. Implement Futures Methods

```python
async def set_leverage(self, symbol: str, leverage: int):
    """Set leverage for a futures symbol."""
    params = {
        'symbol': symbol,
        'leverage': leverage
    }
    return await self._make_request('POST', '/fapi/v1/leverage', params, signed=True)

async def set_margin_type(self, symbol: str, margin_type: str):
    """Set margin type for a futures symbol."""
    params = {
        'symbol': symbol,
        'marginType': margin_type
    }
    return await self._make_request('POST', '/fapi/v1/marginType', params, signed=True)

async def get_position_info(self, symbol: str = None):
    """Get position information for futures."""
    params = {}
    if symbol:
        params['symbol'] = symbol
    return await self._make_request('GET', '/fapi/v2/positionRisk', params, signed=True)
```

## Testing Futures Setup

### 1. Test API Connection

```bash
python test_binance_futures.py
```

### 2. Test Order Placement

```bash
# Test with small amounts first
python test_futures_orders.py --symbol BTCUSDT --amount 0.001
```

### 3. Monitor Positions

```bash
# Check open positions
python test_futures_positions.py
```

## Risk Management for Futures

### 1. Leverage Limits
- **Default**: 5x leverage
- **Maximum**: 125x (varies by symbol)
- **Risk**: Higher leverage = higher risk

### 2. Margin Requirements
- **Initial Margin**: Required to open position
- **Maintenance Margin**: Required to keep position
- **Liquidation**: Position closed if margin insufficient

### 3. Position Sizing
- **Isolated Margin**: Risk limited to position
- **Cross Margin**: Risk across all positions
- **Stop Loss**: Essential for risk management

## Common Issues

### 1. "Futures account not opened"
- **Solution**: Complete futures account setup and quiz

### 2. "Insufficient margin"
- **Solution**: Transfer funds to futures wallet

### 3. "Leverage too high"
- **Solution**: Reduce leverage or increase margin

### 4. "Symbol not found"
- **Solution**: Use correct futures symbol format (e.g., BTCUSDT)

## Security Considerations

### 1. API Key Security
- **IP Restrictions**: Limit to your IP addresses
- **Minimal Permissions**: Only enable required features
- **Regular Rotation**: Change keys periodically

### 2. Risk Management
- **Position Limits**: Set maximum position sizes
- **Stop Losses**: Always use stop losses
- **Leverage Limits**: Don't use excessive leverage

### 3. Testing
- **Testnet First**: Test with testnet before mainnet
- **Small Amounts**: Start with small position sizes
- **Monitor Closely**: Watch positions and PnL

## Next Steps

1. **Enable Futures**: Complete Binance futures setup
2. **Configure API**: Add futures permissions to API key
3. **Update Code**: Implement futures endpoints
4. **Test Thoroughly**: Use testnet for testing
5. **Start Small**: Begin with small position sizes
6. **Monitor Risk**: Watch leverage and margin requirements

## Summary

Futures trading offers more features than spot trading but requires careful risk management. The implementation needs to be updated to use futures endpoints and handle leverage, margin, and position management features.

**Important**: Futures trading involves significant risk due to leverage. Always use proper risk management and start with small amounts.
