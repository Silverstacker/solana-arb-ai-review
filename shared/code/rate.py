"""Rate entry data model - represents a single lending/borrowing rate."""
from dataclasses import dataclass, field
from typing import Optional


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
        if self.ltv <= 0 or self.ltv >= 100:
            return 1.0
        return 1 / (1 - self.ltv / 100)
    
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
KNOWN_UNDERLYING = {
    'ONyc': 13.35,
    'syrupUSDC': 5.86,
    'PST': 9.0,
    'eUSX': 4.5,
}

# Known LTV values by token
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
