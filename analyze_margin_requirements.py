#!/usr/bin/env python3
"""
Binance Futures Margin Analysis
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def analyze_margin_requirements():
    """Analyze margin requirements for 15x leverage"""
    print("Binance Futures Margin Analysis")
    print("=" * 50)
    
    print("\n📊 Current Order Attempts:")
    orders = [
        ("BTC", 0.001, 114752.04, 100.04),
        ("ETH", 0.024, 4154.73, 100.22),
        ("SOL", 0.5, 199.72, 100.19),
        ("XRP", 37.7, 2.66, 100.23)
    ]
    
    total_notional = 0
    total_margin_required = 0
    
    print(f"{'Asset':<6} {'Quantity':<8} {'Price':<10} {'Notional':<10} {'Margin (15x)':<12}")
    print("-" * 60)
    
    for asset, qty, price, notional in orders:
        margin_required = notional / 15.0  # 15x leverage
        total_notional += notional
        total_margin_required += margin_required
        
        print(f"{asset:<6} {qty:<8} ${price:<9.2f} ${notional:<9.2f} ${margin_required:<11.2f}")
    
    print("-" * 60)
    print(f"{'TOTAL':<6} {'':<8} {'':<10} ${total_notional:<9.2f} ${total_margin_required:<11.2f}")
    
    print(f"\n💰 Margin Requirements:")
    print(f"   Total Notional Value: ${total_notional:.2f}")
    print(f"   Required Margin (15x): ${total_margin_required:.2f}")
    print(f"   Recommended Buffer: ${total_margin_required * 1.5:.2f}")
    
    return total_margin_required

def show_solutions():
    """Show solutions for margin issues"""
    print(f"\n🔧 Solutions for 'Margin is insufficient' Error:")
    
    print(f"\n1. 💰 **Add More Funds to Futures Wallet**")
    print(f"   - Transfer USDT from Spot to Futures")
    print(f"   - Minimum needed: ~$7-10 USDT")
    print(f"   - Recommended: $20-50 USDT for safety")
    
    print(f"\n2. 📉 **Reduce Position Sizes**")
    print(f"   - Lower MAX_SINGLE_POSITION in .env")
    print(f"   - Current: $100.0")
    print(f"   - Suggested: $50.0 or $25.0")
    
    print(f"\n3. 🔄 **Reduce Leverage**")
    print(f"   - Lower BINANCE_FUTURES_LEVERAGE")
    print(f"   - Current: 15.0x")
    print(f"   - Suggested: 5.0x or 10.0x")
    
    print(f"\n4. 🗑️ **Cancel Old Orders**")
    print(f"   - Check for locked funds in open orders")
    print(f"   - Cancel orders older than 24 hours")
    print(f"   - This frees up margin")

def show_quick_fix():
    """Show quick fix options"""
    print(f"\n⚡ Quick Fix Options:")
    
    print(f"\n**Option A: Add Funds (Recommended)**")
    print(f"1. Go to Binance → Futures → Transfer")
    print(f"2. Transfer $20-50 USDT from Spot to Futures")
    print(f"3. Restart trading agent")
    
    print(f"\n**Option B: Reduce Position Size**")
    print(f"1. Edit .env file:")
    print(f"   MAX_SINGLE_POSITION=50.0")
    print(f"2. Restart trading agent")
    
    print(f"\n**Option C: Reduce Leverage**")
    print(f"1. Edit .env file:")
    print(f"   BINANCE_FUTURES_LEVERAGE=5.0")
    print(f"   MAX_LEVERAGE=5.0")
    print(f"2. Restart trading agent")

def show_margin_calculation():
    """Show margin calculation details"""
    print(f"\n📐 Margin Calculation Details:")
    
    print(f"\n**For 15x Leverage:**")
    print(f"- Notional Value = Quantity × Price")
    print(f"- Required Margin = Notional Value ÷ Leverage")
    print(f"- Example: $100 order ÷ 15 = $6.67 margin needed")
    
    print(f"\n**For 5x Leverage:**")
    print(f"- Same $100 order ÷ 5 = $20 margin needed")
    print(f"- Higher margin requirement but safer")
    
    print(f"\n**Current Issue:**")
    print(f"- Orders need ~$6.67 margin each")
    print(f"- Total for 4 orders: ~$26.67")
    print(f"- Your futures wallet likely has <$10")

def main():
    """Main function"""
    margin_required = analyze_margin_requirements()
    
    show_solutions()
    show_quick_fix()
    show_margin_calculation()
    
    print(f"\n" + "=" * 50)
    print(f"🎯 **RECOMMENDED ACTION:**")
    print(f"=" * 50)
    print(f"1. 💰 Transfer $30-50 USDT to futures wallet")
    print(f"2. 🔄 Restart trading agent")
    print(f"3. 📊 Monitor first trades")
    print(f"4. ⚠️  Consider reducing leverage to 5x-10x for safety")
    
    print(f"\n💡 **Why This Happens:**")
    print(f"- 15x leverage requires only 1/15th margin")
    print(f"- But you still need sufficient funds in futures wallet")
    print(f"- Each $100 order needs ~$6.67 margin")
    print(f"- Multiple orders need proportionally more margin")
    
    return True

if __name__ == "__main__":
    main()
