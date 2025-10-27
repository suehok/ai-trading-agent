#!/usr/bin/env python3
"""
Check .env file contents and help set up Binance futures trading
"""

import os

def check_env_file():
    """Check the contents of the .env file"""
    print("=== .env File Contents Check ===")
    
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ {env_file} file not found!")
        return False
    
    print(f"✅ {env_file} file exists")
    
    # Read the file
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        print(f"\n📄 Contents of {env_file}:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        # Check for key variables
        futures_vars = [
            'TRADING_PLATFORM',
            'BINANCE_TESTNET',
            'BINANCE_FUTURES_ENABLED',
            'BINANCE_FUTURES_LEVERAGE',
            'BINANCE_FUTURES_MARGIN_TYPE',
            'BINANCE_API_KEY',
            'BINANCE_SECRET_KEY'
        ]
        
        print(f"\n🔍 Checking for required variables:")
        found_vars = []
        missing_vars = []
        
        for var in futures_vars:
            if var in content:
                found_vars.append(var)
                print(f"✅ {var}: Found")
            else:
                missing_vars.append(var)
                print(f"❌ {var}: Missing")
        
        if missing_vars:
            print(f"\n🔧 Missing variables: {', '.join(missing_vars)}")
            return False
        else:
            print(f"\n✅ All required variables found!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading {env_file}: {e}")
        return False

def create_env_template():
    """Create a template .env file with Binance futures settings"""
    print("\n=== Creating .env Template ===")
    
    template = """# Trading Platform Configuration
TRADING_PLATFORM=binance

# Binance API Credentials (REQUIRED - Replace with your actual keys)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET_KEY=your_binance_secret_key_here

# Binance Futures Configuration
BINANCE_TESTNET=false
BINANCE_FUTURES_ENABLED=true
BINANCE_FUTURES_LEVERAGE=5.0
BINANCE_FUTURES_MARGIN_TYPE=ISOLATED

# Risk Management Settings
MAX_TOTAL_ALLOCATION=1000.0
MAX_SINGLE_POSITION=500.0
MAX_DAILY_LOSS=100.0
MAX_LEVERAGE=5.0
MIN_POSITION_SIZE=10.0

# Assets and Interval
ASSETS=BTC ETH SOL
INTERVAL=1h

# LLM Configuration
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key_here
LLM_MODEL=deepseek-chat
"""
    
    try:
        with open(".env.template", "w") as f:
            f.write(template)
        print("✅ Created .env.template file")
        print("\n📝 To use this template:")
        print("1. Copy .env.template to .env")
        print("2. Replace 'your_binance_api_key_here' with your actual Binance API key")
        print("3. Replace 'your_binance_secret_key_here' with your actual Binance secret key")
        print("4. Replace 'your_deepseek_api_key_here' with your actual DeepSeek API key")
        print("5. Restart the trading agent")
        return True
    except Exception as e:
        print(f"❌ Error creating template: {e}")
        return False

def main():
    """Run the diagnostic"""
    print("Binance Futures .env File Diagnostic")
    print("=" * 50)
    
    # Check current .env file
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n🔧 Creating template .env file...")
        create_env_template()
        
        print("\n" + "=" * 50)
        print("Next Steps:")
        print("=" * 50)
        print("1. Edit your .env file with the correct values")
        print("2. Set TRADING_PLATFORM=binance")
        print("3. Set BINANCE_FUTURES_ENABLED=true")
        print("4. Add your Binance API credentials")
        print("5. Restart the trading agent")
        print("\n⚠️  Make sure to:")
        print("- Enable futures in your Binance account")
        print("- Enable 'Enable Futures' permission in your API key")
        print("- Transfer funds to your futures wallet")
    else:
        print("\n✅ .env file looks correct!")
        print("\nIf futures trading is still not working:")
        print("1. Restart the trading agent")
        print("2. Check Binance account setup")
        print("3. Verify API key permissions")
        print("4. Ensure sufficient funds in futures wallet")

if __name__ == "__main__":
    main()
