"""Single-platform loop detection."""
from typing import List, Dict
from collections import defaultdict

from src.models.rate import RateEntry
from src.models.loop import Loop, LoopLeg


def find_single_platform_loops(rates: List[RateEntry]) -> List[Loop]:
    """
    Find all profitable loops within each platform/market.
    
    A loop requires:
    - Collateral token (can_collateral=True, has LTV)
    - Borrow token (can_borrow=True, has borrow_apy)
    - Same platform AND market
    - Collateral != Borrow (unless collateral has underlying yield)
    """
    loops = []
    
    # Group rates by (platform, market)
    grouped = group_by_market(rates)
    
    for (platform, market), market_rates in grouped.items():
        # Separate collateral and borrow options
        collaterals = [
            r for r in market_rates 
            if r.can_collateral and r.total_supply_apy > 0 and r.ltv > 0
        ]
        borrowables = [
            r for r in market_rates 
            if r.can_borrow and r.borrow_apy is not None
        ]
        
        # Find all valid collateral/borrow combinations
        for c in collaterals:
            for b in borrowables:
                # Skip same token unless it has underlying yield
                if c.token == b.token and not c.underlying_apy:
                    continue
                
                loop = create_loop(c, b)
                loops.append(loop)
    
    # Sort by best net APY descending
    return sorted(loops, key=lambda x: x.calculate_returns().get('best_net', 0), reverse=True)


def group_by_market(rates: List[RateEntry]) -> Dict[tuple, List[RateEntry]]:
    """Group rates by (platform, market)."""
    grouped = defaultdict(list)
    for rate in rates:
        key = (rate.platform, rate.market)
        grouped[key].append(rate)
    return grouped


def create_loop(collateral: RateEntry, borrow: RateEntry) -> Loop:
    """Create a single-leg loop from collateral and borrow rates."""
    leg = LoopLeg(
        platform=collateral.platform,
        market=collateral.market,
        deposit_token=collateral.token,
        borrow_token=borrow.token,
        supply_apy=collateral.supply_apy or 0,
        borrow_apy=borrow.borrow_apy,
        ltv=collateral.ltv,
        deposit_url=collateral.url,
        borrow_url=borrow.url
    )
    
    return Loop(
        legs=[leg],
        underlying_apy=collateral.underlying_apy
    )
