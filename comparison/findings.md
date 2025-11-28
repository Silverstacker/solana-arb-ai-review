# AI Review Comparison

This document compares findings from different AI reviewers.

## Review Sessions

| Date | Gemini | ChatGPT | xAI | Focus Area |
|------|--------|---------|-----|------------|
| 2025-11-28 | ✅ Done | ⏳ Pending | ✅ Done | Full Code Review |

---

## Critical Issues Found

### Issue 1: Cross-Platform Borrow Cost Not Scaled by LTV

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | CRITICAL | Borrow cost should be `borrow_apy * (ltv/100)` |
| ChatGPT | ⏳ | - | - |
| xAI | ⚠️ Disputed | CRITICAL | Claims our fix is still wrong by 1/100 factor |

**Status:** ✅ FIXED in commit `b11ca61` - Need to verify xAI's claim

**Note:** xAI may be confused about how we store LTV (as 50, not 0.50). Our formula `ltv/100` converts 50 → 0.50, which is correct.

### Issue 2: Division by Zero Risk (LTV ≈ 100%)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | LTV near 100% causes infinite leverage |
| ChatGPT | ⏳ | - | - |
| xAI | ❌ No | - | Did not mention |

**Status:** ✅ FIXED in commit `1b5b79c` (capped at 98%)

### Issue 3: Hardcoded LTV/APY Constants

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | HIGH | Biggest implementation risk |
| ChatGPT | ⏳ | - | - |
| xAI | ✅ Yes | HIGH | Oracle lag, parameter changes |

**Status:** ⏳ GitHub Issue #1 created

### Issue 4: Code Duplication (max_leverage)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | Same logic in rate.py and loop.py |
| ChatGPT | ⏳ | - | - |
| xAI | ❌ No | - | Focused on execution risks |

**Status:** ✅ FIXED in commit `1b5b79c`

### Issue 5: Silent Failures (empty dict returns)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | Should include error messages |
| ChatGPT | ⏳ | - | - |
| xAI | ❌ No | - | Did not mention |

**Status:** ✅ FIXED in commit `db6f28e`

### Issue 6: Same-Asset Borrowing Restriction (NEW)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ❌ No | - | - |
| ChatGPT | ⏳ | - | - |
| xAI | ✅ Yes | CRITICAL | Kamino blocks borrowing same asset as collateral |

**Status:** 🔴 GitHub Issue #3 - MUST VERIFY ON KAMINO UI

### Issue 7: Reserve Factor Missing (NEW)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ❌ No | - | - |
| ChatGPT | ⏳ | - | - |
| xAI | ✅ Yes | MEDIUM | 10-20% of borrow interest goes to protocol |

**Status:** ⏳ GitHub Issue #4 created

### Issue 8: Utilization / Rate Slippage (NEW)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ❌ No | - | - |
| ChatGPT | ⏳ | - | - |
| xAI | ✅ Yes | HIGH | Large borrows push rate up significantly |

**Status:** ⏳ GitHub Issue #4 created

---

## Unique Insights by AI

### Gemini Only
- Code quality focus: type hints, error handling, DRY principle
- LTV should be per (Platform, Market, Token) not just Token
- Performance analysis: O(N) complexity is good

### ChatGPT Only
- (Pending review)

### xAI Only (Devil's Advocate)
- Same-asset borrowing may be blocked on Kamino
- Reserve factor (10-20%) not accounted for
- Utilization curves: rate changes with position size
- APY vs APR compounding errors (3-8%)
- MEV/frontrunning risks
- Vault borrow caps limit position sizes
- Liquidation cascade risks
- **Verdict:** "Would not trust with real money above $5-10k"

---

## Review Style Comparison

| Aspect | Gemini | xAI |
|--------|--------|-----|
| Focus | Code correctness | Real-world execution |
| Tone | Constructive | Adversarial |
| Found code bugs? | Yes (5) | No new code bugs |
| Found design issues? | Yes (1) | Yes (5+) |
| Execution risks? | Minimal | Extensive |
| Would trust scanner? | With fixes | Not yet |

---

## Consensus Items

Both AIs agreed on:
- Hardcoded constants are a risk
- Cross-platform logic needed attention

xAI uniquely challenged:
- Whether loops are even executable
- Real-world profitability after fees/slippage

---

## Action Items

### From Gemini
- [x] Fix cross-platform borrow cost scaling
- [x] Add MAX_SAFE_LTV cap
- [x] Extract shared calculate_max_leverage()
- [x] Add explicit error messages
- [ ] Add unit tests (Issue #2)
- [ ] Implement dynamic LTV fetching (Issue #1)

### From xAI
- [ ] 🔴 Verify same-asset borrowing on Kamino (Issue #3)
- [ ] Add reserve factor to calculations (Issue #4)
- [ ] Add utilization curve modeling (Issue #4)
- [ ] Add liquidation price calculator
- [ ] Consider position size limits

### Pending
- [ ] Run ChatGPT review
- [ ] Final comparison

---

## Reports

- [Gemini Report - 2025-11-28](../gemini/reports/01_code_review_20251128.md)
- ChatGPT Report - Pending
- [xAI Grok Report - 2025-11-28](../xai/reports/01_code_review_20251128.md)
