# Gemini Math Verification Prompt

## Instructions for Use

1. Open Google AI Studio or Gemini Advanced
2. Upload these files from `shared/code/`:
   - `loop.py`
   - `cross_platform.py`
   - `loop_finder.py`
3. Also upload `shared/context.md`
4. Copy the PROMPT section below and paste it
5. Save response to `gemini/reports/02_math_verification_YYYYMMDD.md`

---

## PROMPT (copy everything below this line)

You are a quantitative analyst verifying the mathematical correctness of a DeFi arbitrage calculation system.

**I've attached the key calculation files and project context.**

## Background

This system calculates "loop" strategy returns for Solana lending protocols.

**Single-Platform Loop Formula (from the code):**
```
Net APY = (Supply_APY × Leverage) - (Borrow_APY × (Leverage - 1))

Where:
- Leverage is limited by LTV (Loan-to-Value)
- Max_Leverage = 1 / (1 - LTV/100)
- Actual_Leverage = min(Target_Leverage, Max_Leverage × 0.9)  # 90% safety buffer
```

**Cross-Platform Loop Formula (from the code):**
```
Leg 1: Deposit token A on Platform1, earn Supply1 APY, borrow token B paying Borrow1 APY
Leg 2: Deposit token B on Platform2, earn Supply2 APY (no borrowing)

Net APY = Supply1 + (Supply2 × LTV1/100) - Borrow1
```

## Your Task

### 1. VERIFY THE FORMULAS ARE CORRECT

Please analyze whether these formulas accurately model the financial returns:

- Is the single-platform loop formula mathematically correct?
- Is the leverage calculation correct?
- Is the cross-platform formula accurate?
- Are there any mathematical errors in the implementation?

### 2. WORK THROUGH THESE EXAMPLES BY HAND

Calculate each scenario manually and compare to what the code would produce:

**Scenario A: ONyc → USDC Loop (OnRe Market)**
- ONyc underlying APY: 13.35%
- ONyc supply APY: 0%
- USDC borrow APY: 3.14%
- ONyc LTV: 50%
- Question: What is the net APY at 2x leverage?

**Scenario B: syrupUSDC → USDC Loop (Maple Market)**
- syrupUSDC underlying APY: 5.86%
- syrupUSDC supply APY: ~6% (varies)
- USDC borrow APY: ~4%
- syrupUSDC LTV: 88%
- Question: What is the net APY at 4x and 8x leverage?

**Scenario C: Cross-Platform (Kamino → Jupiter)**
- Deposit ONyc on Kamino OnRe Market (13.35% underlying, 0% supply)
- Borrow USDC from Kamino at 3.14%
- Deposit USDC on Jupiter Earn at 5.82%
- ONyc LTV: 50%
- Question: What is the net APY?

### 3. CHECK EDGE CASES

Test these edge cases mathematically:

- What happens when LTV = 0?
- What happens when LTV = 100?
- What happens when LTV approaches 100 (e.g., 99%)?
- What if borrow APY > supply APY (negative spread)?
- What if leverage = 1 (no loop, just holding)?

### 4. IDENTIFY MISSING FACTORS

What real-world factors does this model NOT account for?

- Compounding frequency?
- Liquidation risk/costs?
- Gas/transaction fees?
- Rate volatility/changes?
- Slippage?
- Protocol fees?
- Health factor degradation?

## Output Format

```
## 1. Formula Analysis

### Single-Platform Loop
[Is it correct? Show your reasoning]

### Cross-Platform Loop
[Is it correct? Show your reasoning]

## 2. Worked Examples

### Scenario A: ONyc → USDC
Step 1: ...
Step 2: ...
Final: Net APY = X%
Code would produce: Y%
Match: Yes/No

### Scenario B: syrupUSDC → USDC
[Same format]

### Scenario C: Cross-Platform
[Same format]

## 3. Edge Cases

| Case | Expected Behavior | Actual Behavior | Issue? |
|------|-------------------|-----------------|--------|
| LTV = 0 | ... | ... | ... |
| LTV = 100 | ... | ... | ... |
[etc.]

## 4. Missing Factors

[List what's not modeled and potential impact]

## 5. Recommendations

[List any corrections or improvements needed]
```
