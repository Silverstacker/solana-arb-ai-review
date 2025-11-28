"""Cross-platform arbitrage detection.

This module finds multi-leg arbitrage opportunities across different platforms.

Key insight: You can only borrow from the same platform where your collateral is deposited.
But once you have borrowed funds, you can deposit them anywhere.

Example 2-leg cross-platform loop:
1. Deposit ONyc on Kamino (OnRe Market) -> Borrow USDC from Kamino
2. Deposit USDC on Jupiter Earn

Net APY = ONyc_supply + (USDC_jupiter_supply * ONyc_LTV/100) - USDC_kamino_borrow
"""
from typing import List, Dict, Set
from collections import defaultdict

from src.models.rate import RateEntry
from src.models.loop import Loop, LoopLeg


def find_cross_platform_loops(rates: List[RateEntry]) -> List[Loop]:
    """
    Find 2-leg cross-platform arbitrage opportunities.
    
    Strategy:
    - Leg 1: Deposit collateral on Platform A, borrow asset X from Platform A
    - Leg 2: Deposit asset X on Platform B (earn-only deposit)
    
    Net = leg1_supply + (leg2_supply * leg1_ltv/100) - leg1_borrow
    """
    loops = []
    
    # Build lookup tables
    deposit_by_token = build_deposit_lookup(rates)  # token -> [RateEntry]
    borrow_by_market = build_borrow_lookup(rates)   # (platform, market) -> {token: RateEntry}
    
    # For each potential first leg (collateral with borrowing capability)
    for rate in rates:
        if not rate.can_collateral or rate.ltv <= 0:
            continue
        
        # What tokens can we borrow from this market?
        market_key = (rate.platform, rate.market)
        available_borrows = borrow_by_market.get(market_key, {})
        
        for borrow_token, borrow_rate in available_borrows.items():
            # Skip if same token without underlying yield
            if borrow_token == rate.token and not rate.underlying_apy:
                continue
            
            # Where can we deposit the borrowed token on a DIFFERENT platform?
            deposit_options = deposit_by_token.get(borrow_token, [])
            
            for deposit_rate in deposit_options:
                # Must be different platform for cross-platform
                if deposit_rate.platform == rate.platform:
                    continue
                
                # Create cross-platform loop
                loop = create_cross_platform_loop(
                    collateral_rate=rate,
                    borrow_rate=borrow_rate,
                    deposit_rate=deposit_rate
                )
                
                # Only include if profitable
                returns = loop.calculate_returns()
                if returns.get('best_net', 0) > 0:
                    loops.append(loop)
    
    # Sort by best net APY descending
    return sorted(loops, key=lambda x: x.calculate_returns().get('best_net', 0), reverse=True)


def build_deposit_lookup(rates: List[RateEntry]) -> Dict[str, List[RateEntry]]:
    """
    Build lookup: token -> list of deposit options.
    Includes both collateral-capable and earn-only deposits.
    """
    lookup = defaultdict(list)
    for rate in rates:
        if rate.total_supply_apy > 0:
            lookup[rate.token].append(rate)
    return lookup


def build_borrow_lookup(rates: List[RateEntry]) -> Dict[tuple, Dict[str, RateEntry]]:
    """
    Build lookup: (platform, market) -> {token: RateEntry}.
    Only includes tokens that can be borrowed.
    """
    lookup = defaultdict(dict)
    for rate in rates:
        if rate.can_borrow and rate.borrow_apy is not None:
            key = (rate.platform, rate.market)
            lookup[key][rate.token] = rate
    return lookup


def create_cross_platform_loop(
    collateral_rate: RateEntry,
    borrow_rate: RateEntry,
    deposit_rate: RateEntry
) -> Loop:
    """
    Create a 2-leg cross-platform loop.
    
    Leg 1: Deposit collateral -> Borrow
    Leg 2: Deposit borrowed asset on different platform
    """
    leg1 = LoopLeg(
        platform=collateral_rate.platform,
        market=collateral_rate.market,
        deposit_token=collateral_rate.token,
        borrow_token=borrow_rate.token,
        supply_apy=collateral_rate.supply_apy or 0,
        borrow_apy=borrow_rate.borrow_apy,
        ltv=collateral_rate.ltv,
        deposit_url=collateral_rate.url,
        borrow_url=borrow_rate.url
    )
    
    leg2 = LoopLeg(
        platform=deposit_rate.platform,
        market=deposit_rate.market,
        deposit_token=deposit_rate.token,
        borrow_token='',  # No borrow on leg 2
        supply_apy=deposit_rate.supply_apy or 0,
        borrow_apy=0,
        ltv=0,  # Not using as collateral
        deposit_url=deposit_rate.url,
        borrow_url=''
    )
    
    return Loop(
        legs=[leg1, leg2],
        underlying_apy=collateral_rate.underlying_apy
    )


def find_3leg_loops(rates: List[RateEntry]) -> List[Loop]:
    """
    Find 3-leg arbitrage loops (more complex, lower returns typically).
    
    Example:
    1. Deposit A on Platform1 -> Borrow B
    2. Deposit B on Platform2 -> Borrow C
    3. Swap C back to A (or deposit for yield)
    
    This is more advanced and requires careful analysis of:
    - Multiple LTV layers compounding
    - Swap costs/slippage
    - Health factor complexity
    
    TODO: Implement after 2-leg loops are validated.
    """
    pass  # Future implementation
