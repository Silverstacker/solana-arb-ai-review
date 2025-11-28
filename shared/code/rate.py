"""Rate entry data model - represents a single lending/borrowing rate."""
from dataclasses import dataclass, field
from typing import Optional


# Maximum safe LTV to prevent division issues near 100%
MAX_SAFE_LTV = 98.0


def calculate_max_leverage(ltv: float) -> float:
    """
    Calculate maximum leverage from LTV.
    Shared utility to avoid code duplication.
    
    Formula: max_leverage = 1 / (1 - LTV/100)
    
    Safety: Cap LTV at 98% to prevent extreme/infinite leverage.
    """
    if ltv <= 0:
        return 1.0
    # Cap at safe maximum to prevent division by near-zero
    safe_ltv = min(ltv, MAX_SAFE_LTV)
    return 1 / (1 - safe_ltv / 100)


@dataclass
class RateEntry:
    """Normalized rate entry from any platform."""
    platform: str           # 'kamino' | 'jupiter'
    market: str             # 'Main Market', 'Jupiter Earn', etc.
    token: str              # 'USDC', 'ONyc', etc.
    supply_apy: Optional[float] = None
    underlying_apy: Optional[float] = None
    borrow_apy: Optional[float] = None
    ltv: float = 0
    can_collateral: bool = False
    can_borrow: bool = False
    url: str = ""
    
    @property
    def total_supply_apy(self) -> float:
        """Combined supply + underlying APY."""
        supply = self.supply_apy or 0
        underlying = self.underlying_apy or 0
        return supply + underlying
    
    @property
    def max_leverage(self) -> float:
        """Maximum leverage based on LTV."""
        return calculate_max_leverage(self.ltv)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'platform': self.platform,
            'market': self.market,
            'token': self.token,
            'supply_apy': self.supply_apy,
            'underlying_apy': self.underlying_apy,
            'total_apy': self.total_supply_apy,
            'borrow_apy': self.borrow_apy,
            'ltv': self.ltv,
            'can_collateral': self.can_collateral,
            'url': self.url
        }


# Known yield-bearing tokens with underlying APY
# TODO: Fetch dynamically from protocol APIs (DeFiLlama, etc.)
# These are fallback values when scraping doesn't return underlying APY
KNOWN_UNDERLYING = {
    'ONyc': 13.35,
    'syrupUSDC': 5.86,
    'PST': 9.0,
    'eUSX': 4.5,
}

# Known LTV values by token
# TODO: Fetch dynamically from protocol APIs
# These are fallback values when scraping doesn't return LTV
KNOWN_LTV = {
    'ONyc': 50,
    'syrupUSDC': 88,
    'PST': 75,
    'eUSX': 75,
    'USDC': 80,
    'USDT': 80,
    'PYUSD': 80,
    'USDG': 80,
    'USDS': 80,
    'EURC': 0,
    'CASH': 0,
    'USX': 80,
}

# Tokens that can only supply (no borrowing)
SUPPLY_ONLY_TOKENS = {'syrupUSDC', 'ONyc', 'PST', 'eUSX', 'PT-eUSX-11MAR26', 'PT-USX-09FEB26'}
