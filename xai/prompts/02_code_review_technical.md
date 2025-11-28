# xAI Grok Code Review Prompt - Technical Focus

## Instructions for Use

1. Open Grok (x.ai or via X/Twitter)
2. Upload the same files as before:
   - `shared/context.md`
   - `shared/code/rate.py`
   - `shared/code/loop.py`
   - `shared/code/loop_finder.py`
   - `shared/code/cross_platform.py`
3. Copy the PROMPT section below and paste it
4. Save response to `xai/reports/02_code_review_technical_YYYYMMDD.md`

---

## PROMPT (copy everything below this line)

I need a detailed **technical code review** of this Python codebase. Focus on the actual code, not business strategy.

**I've shared 4 Python files for a Solana DeFi arbitrage scanner.**

## Review Each File

### 1. rate.py - Data Model
- Is `calculate_max_leverage()` mathematically correct?
- Is the MAX_SAFE_LTV cap (98%) the right choice?
- Are there any edge cases in the properties?
- Type safety issues?

### 2. loop.py - Core Calculations
- Is the single-platform formula correct? `Net = (supply * leverage) - (borrow * (leverage - 1))`
- Is the cross-platform formula correct? `Net = supply1 + (supply2 * ltv/100) - (borrow * ltv/100)`
- Does `make_error_return()` handle all failure cases?
- Any bugs in `_calc_single_platform()` or `_calc_cross_platform()`?

### 3. loop_finder.py - Loop Detection
- Is the algorithm correct for finding valid loops?
- Are all edge cases handled?
- Any performance issues with the nested loops?

### 4. cross_platform.py - Cross-Platform Detection  
- Is the matching logic correct?
- Are there any bugs in how legs are combined?
- Edge cases with the defaultdict lookups?

## Specific Questions

1. **Math verification:** Work through a concrete example:
   - Deposit ONyc (13.35% underlying, 0% supply APY, 50% LTV)
   - Borrow USDC at 3.14%
   - Deposit USDC on Jupiter at 5.82%
   - What should the net APY be? Does the code calculate this correctly?

2. **Edge cases:** What happens if:
   - LTV is 0?
   - LTV is exactly 100?
   - Supply APY is negative?
   - Borrow APY is 0?
   - A token appears in multiple markets?

3. **Bug hunting:** Look for:
   - Off-by-one errors
   - Division by zero
   - None/null handling
   - Type mismatches
   - Logic errors

## Output Format

Structure your response as:

```
## File: rate.py
### Issues Found
[List any bugs or concerns]
### Code Quality
[Assessment]

## File: loop.py
### Issues Found
[List any bugs or concerns]  
### Math Verification
[Work through the ONyc example step by step]

## File: loop_finder.py
### Issues Found
[List any bugs or concerns]

## File: cross_platform.py
### Issues Found
[List any bugs or concerns]

## Summary
### Critical Bugs
[Must fix]
### Medium Issues
[Should fix]
### Minor Issues
[Nice to fix]
### What's Done Well
[Positive feedback]
```

Be thorough. Check every function.
