# Gemini Full Code Review Prompt

## Instructions for Use

1. Open Google AI Studio (aistudio.google.com) or Gemini Advanced
2. Upload ALL files from `shared/code/` folder
3. Also upload `shared/context.md` for background
4. Copy the PROMPT section below and paste it
5. Save Gemini's response to `gemini/reports/01_code_review_YYYYMMDD.md`

---

## PROMPT (copy everything below this line)

You are a senior Python developer specializing in DeFi and financial systems. I'm building a Solana stablecoin arbitrage scanner and need a thorough code review.

**I've attached the complete codebase and a context document explaining the project.**

## Your Task

Provide a comprehensive code review covering:

### 1. BUGS & ERRORS
- Logic errors that would produce incorrect results
- Edge cases that aren't handled
- Potential runtime exceptions
- Off-by-one errors
- Division by zero risks
- Null/None handling issues

### 2. CODE QUALITY
- Code structure and organization
- Naming conventions
- Code duplication
- Function complexity (too long, doing too much)
- Missing type hints
- Inconsistent patterns

### 3. ERROR HANDLING
- Missing try/except blocks
- Silent failures
- Poor error messages
- Unhandled network errors
- Timeout issues

### 4. SECURITY CONCERNS
- Hardcoded values that shouldn't be
- Injection vulnerabilities
- Data validation issues

### 5. PERFORMANCE
- Inefficient algorithms
- Unnecessary loops
- Memory issues
- Blocking operations

## Output Format

For each issue found, provide:

```
### [SEVERITY: CRITICAL/HIGH/MEDIUM/LOW] - Brief Title

**File:** filename.py
**Line(s):** XX-YY (approximate is fine)
**Issue:** Description of the problem
**Impact:** What goes wrong if not fixed
**Fix:** Suggested solution with code example if helpful
```

## Priority Focus

Please pay special attention to:

1. **loop.py** - The leverage and APY calculations. Is the math correct?
2. **cross_platform.py** - The cross-platform arbitrage logic. Does it correctly calculate 2-leg returns?
3. **loop_finder.py** - The loop detection algorithm. Does it find all valid opportunities?
4. **kamino/scraper.py** - Web scraping reliability. What happens when pages change?

## Questions to Answer

At the end of your review, please also answer:

1. Are the leverage calculations mathematically correct?
2. Is the cross-platform formula `Net = leg1_supply + (leg2_supply × LTV1/100) - leg1_borrow` right?
3. What's the biggest risk in this codebase?
4. What would you prioritize fixing first?

Be thorough. I'd rather have too many findings than miss something important.
