# ChatGPT Code Review Prompt

## Instructions for Use

1. Open ChatGPT (chat.openai.com) - GPT-4 recommended
2. Upload these files:
   - `shared/context.md`
   - `shared/code/rate.py`
   - `shared/code/loop.py`
   - `shared/code/loop_finder.py`
   - `shared/code/cross_platform.py`
3. Copy the PROMPT section below and paste it
4. Save response to `chatgpt/reports/01_code_review_YYYYMMDD.md`

---

## PROMPT (copy everything below this line)

You are a senior Python developer and DeFi expert. I'm building a Solana stablecoin arbitrage scanner that finds "loop" opportunities - strategies that exploit interest rate differentials between lending and borrowing.

**I've attached the codebase and a context document.**

## Background

This scanner:
1. Scrapes lending rates from Kamino Finance and Jupiter Lend
2. Finds single-platform loops (deposit → borrow → re-deposit)
3. Finds cross-platform arbitrage (deposit on Platform A → borrow → deposit on Platform B)
4. Calculates net APY at various leverage levels

## Your Task

Please review this code for:

### 1. Mathematical Correctness
- Is the single-platform formula correct? `Net = (supply * leverage) - (borrow * (leverage - 1))`
- Is the cross-platform formula correct? `Net = supply1 + (supply2 * LTV/100) - (borrow * LTV/100)`
- Are there any edge cases in the leverage calculations?

### 2. Code Quality
- Architecture and design patterns
- Error handling
- Type safety
- Potential bugs

### 3. DeFi-Specific Concerns
- Are we modeling the financial mechanics correctly?
- What real-world factors might we be missing?
- Any liquidation risks not accounted for?

### 4. Suggestions
- What would you improve?
- Any optimizations?
- Missing features?

## Output Format

Please structure your response as:

```
## Summary
[High-level assessment]

## Mathematical Review
[Analysis of formulas]

## Code Issues Found
### [SEVERITY] - Title
**File:** ...
**Issue:** ...
**Fix:** ...

## DeFi Considerations
[Real-world factors]

## Recommendations
[Prioritized list]
```

## Context

A previous review (Gemini) found that the cross-platform borrow cost wasn't being scaled by LTV - this has been fixed. Please verify the fix is correct and look for any other issues.

The fixed formula is now:
```python
cost_leg1 = leg1.borrow_apy * (leg1.ltv / 100)
```

Is this mathematically correct?
