# AI Review Comparison

This document compares findings from different AI reviewers.

## Review Sessions

| Date | Gemini | ChatGPT | xAI | Focus Area |
|------|--------|---------|-----|------------|
| 2025-11-28 | ✅ Done | ⏳ Pending | ⏳ Pending | Full Code Review |

---

## Critical Issues Found

### Issue 1: Cross-Platform Borrow Cost Not Scaled by LTV

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | CRITICAL | Borrow cost should be `borrow_apy * (ltv/100)` |
| ChatGPT | ⏳ | - | - |
| xAI | ⏳ | - | - |

**Status:** ✅ FIXED in commit `b11ca61`

### Issue 2: Division by Zero Risk (LTV ≈ 100%)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | LTV near 100% causes infinite leverage |
| ChatGPT | ⏳ | - | - |
| xAI | ⏳ | - | - |

**Status:** ✅ FIXED in commit `1b5b79c` (capped at 98%)

### Issue 3: Hardcoded LTV/APY Constants

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | HIGH | Biggest implementation risk |
| ChatGPT | ⏳ | - | - |
| xAI | ⏳ | - | - |

**Status:** ⏳ GitHub Issue #1 created

### Issue 4: Code Duplication (max_leverage)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | Same logic in rate.py and loop.py |
| ChatGPT | ⏳ | - | - |
| xAI | ⏳ | - | - |

**Status:** ✅ FIXED in commit `1b5b79c`

### Issue 5: Silent Failures (empty dict returns)

| AI | Found? | Severity | Notes |
|----|--------|----------|-------|
| Gemini | ✅ Yes | MEDIUM | Should include error messages |
| ChatGPT | ⏳ | - | - |
| xAI | ⏳ | - | - |

**Status:** ✅ FIXED in commit `db6f28e`

---

## Unique Insights by AI

### Gemini Only
- Identified that single-platform formula is correct but cross-platform was wrong
- Suggested LTV should be per (Platform, Market, Token) not just Token
- Performance analysis: O(N) complexity is good, no changes needed

### ChatGPT Only
- (Pending review)

### xAI Only
- (Pending review)

---

## Consensus Items
(Issues all AIs agreed on - will update after all reviews)

---

## Action Items

- [x] Fix cross-platform borrow cost scaling
- [x] Add MAX_SAFE_LTV cap
- [x] Extract shared calculate_max_leverage()
- [x] Add explicit error messages
- [ ] Add unit tests (Issue #2)
- [ ] Implement dynamic LTV fetching (Issue #1)
- [ ] Run ChatGPT review
- [ ] Run xAI review
- [ ] Compare findings

---

## Reports

- [Gemini Report - 2025-11-28](../gemini/reports/01_code_review_20251128.md)
- ChatGPT Report - Pending
- xAI Report - Pending
