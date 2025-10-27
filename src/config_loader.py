import os
from dotenv import load_dotenv

load_dotenv()

def _get_env(name: str, default: str | None = None, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def _get_valid_model() -> str:
    """Get a valid LLM model, with fallback for invalid models."""
    model = _get_env("LLM_MODEL", "deepseek-chat")
    
    # List of invalid models that should be replaced
    # For OpenRouter: deepseek/deepseek-chat-v2, deepseek/deepseek-coder, etc. are invalid
    # For DeepSeek API: deepseek-chat-v2, deepseek-coder, etc. are invalid
    invalid_models = [
        "deepseek/deepseek-chat-v2",  # OpenRouter invalid
        "deepseek/deepseek-coder",    # OpenRouter invalid
        "deepseek/deepseek-coder-v2", # OpenRouter invalid
        "deepseek/deepseek-llm",      # OpenRouter invalid
        "deepseek/deepseek-llm-v2",   # OpenRouter invalid
        "deepseek-chat-v2",           # DeepSeek API invalid
        "deepseek-coder",             # DeepSeek API invalid
        "deepseek-coder-v2",          # DeepSeek API invalid
        "deepseek-llm",               # DeepSeek API invalid
        "deepseek-llm-v2"             # DeepSeek API invalid
    ]
    
    # If the model is invalid, use a valid fallback
    if model in invalid_models:
        print(f"Warning: Invalid model '{model}' detected. Using fallback 'deepseek-chat'")
        return "deepseek-chat"
    
    return model

CONFIG = {
    "taapi_api_key": _get_env("TAAPI_API_KEY"),  # Optional when using Binance indicators
    "hyperliquid_private_key": _get_env("HYPERLIQUID_PRIVATE_KEY") or _get_env("LIGHTER_PRIVATE_KEY"),
    "mnemonic": _get_env("MNEMONIC"),
    # Hyperliquid network/base URL overrides
    "hyperliquid_base_url": _get_env("HYPERLIQUID_BASE_URL"),
    "hyperliquid_network": _get_env("HYPERLIQUID_NETWORK", "mainnet"),
    # Binance API credentials
    "binance_api_key": _get_env("BINANCE_API_KEY"),
    "binance_secret_key": _get_env("BINANCE_SECRET_KEY"),
    "binance_testnet": _get_env("BINANCE_TESTNET", "false"),
    # Binance Futures Configuration
    "binance_futures_enabled": _get_env("BINANCE_FUTURES_ENABLED", "false"),
    "binance_futures_leverage": _get_env("BINANCE_FUTURES_LEVERAGE", "5.0"),
    "binance_futures_margin_type": _get_env("BINANCE_FUTURES_MARGIN_TYPE", "ISOLATED"),
    # Trading platform selection
    "trading_platform": _get_env("TRADING_PLATFORM", "hyperliquid"),  # "hyperliquid" or "binance"
    # LLM Configuration
    "llm_provider": _get_env("LLM_PROVIDER", "deepseek"),  # "openrouter" or "deepseek"
    # OpenRouter Configuration (when LLM_PROVIDER="openrouter")
    "openrouter_api_key": _get_env("OPENROUTER_API_KEY"),
    "openrouter_base_url": _get_env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    "openrouter_referer": _get_env("OPENROUTER_REFERER"),
    "openrouter_app_title": _get_env("OPENROUTER_APP_TITLE", "trading-agent"),
    # DeepSeek API Configuration (when LLM_PROVIDER="deepseek")
    "deepseek_api_key": _get_env("DEEPSEEK_API_KEY"),
    "deepseek_base_url": _get_env("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    "llm_model": _get_valid_model(),
    # Runtime controls via env
    "assets": _get_env("ASSETS"),  # e.g., "BTC ETH SOL" or "BTC,ETH,SOL"
    "interval": _get_env("INTERVAL"),  # e.g., "5m", "1h"
    # API server
    "api_host": _get_env("API_HOST", "0.0.0.0"),
    "api_port": _get_env("APP_PORT") or _get_env("API_PORT") or "3000",
    # Risk Management Settings
    "max_total_allocation": _get_env("MAX_TOTAL_ALLOCATION", "1000.0"),
    "max_single_position": _get_env("MAX_SINGLE_POSITION", "500.0"),
    "max_daily_loss": _get_env("MAX_DAILY_LOSS", "100.0"),
    "max_leverage": _get_env("MAX_LEVERAGE", "5.0"),
    "min_position_size": _get_env("MIN_POSITION_SIZE", "10.0"),
    "max_consecutive_losses": _get_env("MAX_CONSECUTIVE_LOSSES", "3"),
}
