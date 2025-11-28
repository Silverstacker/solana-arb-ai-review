# Solana Stablecoin Arbitrage Scanner - Project Context

## Overview

This system scans Solana DeFi lending protocols to find profitable stablecoin arbitrage opportunities through "loop" strategies.

## What is a Loop Strategy?

A loop exploits interest rate differentials:

1. **Deposit** a stablecoin as collateral (earn supply APY)
2. **Borrow** against it (pay borrow APY)
3. **Re-deposit** borrowed funds (earn more supply APY)
4. **Repeat** until max leverage reached

**Example**: 
- Deposit ONyc earning 13.35% underlying APY
- Borrow USDC at 3.14% APY
- With 50% LTV, max leverage is 2x
- Net APY = (13.35% × 2) - (3.14% × 1) = 23.56% (theoretical)
- Safe leverage (90% of max): Net ≈ 21.5%

## Key Concepts

### LTV (Loan-to-Value)
- Determines how much you can borrow against collateral
- 80% LTV = borrow $80 for every $100 deposited
- Max leverage = 1 / (1 - LTV)
  - 50% LTV → 2x max
  - 80% LTV → 5x max
  - 88% LTV → 8.33x max

### Yield-Bearing Stablecoins
Some tokens have "underlying APY" - yield earned just by holding:
- **ONyc** (OnRe): 13.35% underlying
- **syrupUSDC** (Maple): 5.86% underlying
- **PST** (Huma): 9.0% underlying
- **eUSX** (Solstice): 4.5% underlying

### Cross-Platform Arbitrage
2-leg strategy across different platforms:
1. Deposit collateral on Platform A → Borrow asset X
2. Deposit asset X on Platform B (earn-only)

Net = leg1_supply + (leg2_supply × leg1_LTV/100) - leg1_borrow

## Platforms Scanned

### Kamino Finance (5 markets)
- **Main Market**: General stablecoins (USDC, USDT, PYUSD, etc.)
- **OnRe Market**: ONyc collateral only
- **Maple Market**: syrupUSDC collateral only
- **Huma Market**: PST collateral only
- **Solstice Market**: eUSX collateral only

### Jupiter Lend
- **Earn**: Simple deposits
- **Multiply**: Pre-calculated loop strategies

## Architecture

```
src/
├── models/
│   ├── rate.py      # RateEntry dataclass
│   └── loop.py      # Loop, LoopLeg dataclasses
├── datasources/
│   ├── kamino/scraper.py   # Playwright scraper
│   └── jupiter/scraper.py  # Playwright scraper
├── engine/
│   ├── loop_finder.py      # Single-platform loops
│   └── cross_platform.py   # Multi-platform arbitrage
└── cli.py           # Entry point
```

## Key Files to Review

1. **loop.py** - Loop math and leverage calculations
2. **cross_platform.py** - Cross-platform arbitrage logic
3. **loop_finder.py** - Loop detection algorithm
4. **kamino/scraper.py** - Web scraping logic

## Known Concerns

- Leverage calculations may have edge cases
- Cross-platform math needs verification
- Scraper reliability (web pages change)
- Rate limiting / timeout handling

## Output Format

JSON with:
- `opportunities[]` - Single-platform loops
- `cross_platform[]` - Multi-platform paths
- `lending_rates[]` - All supply rates
- `borrow_rates[]` - All borrow rates
