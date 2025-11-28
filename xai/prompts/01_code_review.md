# xAI Grok Code Review Prompt

## Instructions for Use

1. Open Grok (x.ai or via X/Twitter)
2. Upload or paste the code files:
   - `shared/context.md`
   - `shared/code/rate.py`
   - `shared/code/loop.py`
   - `shared/code/loop_finder.py`
   - `shared/code/cross_platform.py`
3. Copy the PROMPT section below and paste it
4. Save response to `xai/reports/01_code_review_YYYYMMDD.md`

---

## PROMPT (copy everything below this line)

I need you to be brutally honest and contrarian. I'm building a Solana DeFi arbitrage scanner and I want you to find flaws that other reviewers might miss.

**I've shared the codebase and context.**

## What This Does

This scanner finds "loop" arbitrage opportunities:
1. Deposit stablecoin as collateral
2. Borrow against it
3. Re-deposit borrowed funds
4. Repeat for leveraged returns

It calculates net APY using:
- **Single-platform:** `Net = (supply * leverage) - (borrow * (leverage - 1))`
- **Cross-platform:** `Net = supply1 + (supply2 * LTV/100) - (borrow * LTV/100)`

## Your Mission

Be the devil's advocate. Challenge everything:

### 1. Attack the Math
- Are these formulas actually correct for how DeFi lending works?
- What assumptions are being made that might not hold?
- Are there compounding effects being ignored?
- Is the leverage calculation accurate for recursive loops?

### 2. Find Hidden Bugs
- Edge cases that would crash or give wrong results
- Race conditions or timing issues
- Data validation gaps

### 3. Challenge the Strategy
- Why might this arbitrage NOT work in practice?
- What are the execution risks?
- What could go wrong between "scanner says profitable" and "actually making money"?

### 4. Real-World Problems
- Gas/transaction costs
- Slippage
- Rate changes during execution
- Liquidation cascades
- Protocol risks

### 5. What's Missing?
- What would a sophisticated DeFi trader want that this doesn't have?
- What data sources are we not using?
- What strategies are we not detecting?

## Previous Findings

Gemini found that we weren't scaling borrow costs by LTV for cross-platform loops. That's fixed now. What else might be wrong?

## Output Format

Be direct. No fluff. Structure as:

```
## Critical Flaws
[Things that are definitely wrong]

## Questionable Assumptions  
[Things that might be wrong]

## Missing Pieces
[What's not accounted for]

## Attack Vectors
[How this could fail in production]

## Verdict
[Overall assessment - would you trust this to trade real money?]
```

Don't hold back. I'd rather know the problems now.
