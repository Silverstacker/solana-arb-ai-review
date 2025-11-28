"""Loop and LoopLeg data models for arbitrage opportunities."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class LoopLeg:
    """Single leg of a loop strategy."""
    platform: str
    market: str
    deposit_token: str
    borrow_token: str
    supply_apy: float
    borrow_apy: float
    ltv: float
    deposit_url: str = ""
    borrow_url: str = ""
    
    @property
    def spread(self) -> float:
        return self.supply_apy - self.borrow_apy
    
    @property
    def max_leverage(self) -> float:
        if self.ltv <= 0 or self.ltv >= 100:
            return 1.0
        return 1 / (1 - self.ltv / 100)


@dataclass
class Loop:
    """Complete loop strategy (single or multi-leg)."""
    legs: List[LoopLeg]
    underlying_apy: Optional[float] = None
    
    @property
    def num_legs(self) -> int:
        return len(self.legs)
    
    @property
    def is_cross_platform(self) -> bool:
        if len(self.legs) < 2:
            return False
        platforms = {leg.platform for leg in self.legs}
        return len(platforms) > 1
    
    @property
    def collateral(self) -> str:
        return self.legs[0].deposit_token if self.legs else ""
    
    @property
    def borrow(self) -> str:
        return self.legs[0].borrow_token if self.legs else ""
    
    @property
    def market(self) -> str:
        return self.legs[0].market if self.legs else ""
    
    @property
    def platform(self) -> str:
        return self.legs[0].platform if self.legs else ""
    
    @property
    def first_ltv(self) -> float:
        return self.legs[0].ltv if self.legs else 0
    
    @property
    def total_supply_apy(self) -> float:
        """Total supply APY including underlying."""
        base = self.legs[0].supply_apy if self.legs else 0
        return base + (self.underlying_apy or 0)
    
    def calculate_returns(self, leverage_levels: List[int] = None) -> Dict:
        """
        Calculate net APY at various leverage levels.
        
        For single-leg loops:
            Net = (supply * leverage) - (borrow * (leverage - 1))
        
        For cross-platform 2-leg loops:
            Net = leg1_supply + (leg2_supply * leg1_ltv) - leg1_borrow
        """
        if leverage_levels is None:
            leverage_levels = [2, 3, 4, 5, 6, 8]
        
        results = {}
        
        if self.is_cross_platform:
            # Cross-platform calculation
            return self._calc_cross_platform()
        else:
            # Single-platform loop
            return self._calc_single_platform(leverage_levels)
    
    def _calc_single_platform(self, leverage_levels: List[int]) -> Dict:
        """Calculate returns for single-platform loop."""
        if not self.legs:
            return {}
        
        leg = self.legs[0]
        supply = self.total_supply_apy
        borrow = leg.borrow_apy
        max_lev = leg.max_leverage
        
        results = {}
        best_net = float('-inf')
        best_lev = '2x'
        
        for lev in leverage_levels:
            actual = min(lev, max_lev * 0.9)  # 90% of max for safety
            if actual < 1:
                continue
            
            net = (supply * actual) - (borrow * (actual - 1))
            
            results[f'{lev}x'] = {
                'net': net,
                'actual': actual,
                'max': max_lev
            }
            
            if net > best_net:
                best_net = net
                best_lev = f'{lev}x'
        
        return {
            'lev_results': results,
            'best_lev': best_lev,
            'best_net': best_net,
            'min_net': results.get('2x', {}).get('net', 0),
            'max_net': best_net
        }
    
    def _calc_cross_platform(self) -> Dict:
        """
        Calculate returns for cross-platform loop.
        
        2-leg example:
        - Leg 1: Deposit A on Platform1 (earn supply1), Borrow B (pay borrow1)
        - Leg 2: Deposit B on Platform2 (earn supply2 * ltv1)
        
        Net = supply1 + (supply2 * ltv1/100) - borrow1
        """
        if len(self.legs) < 2:
            return {}
        
        leg1 = self.legs[0]
        leg2 = self.legs[1]
        
        # Calculate earnings and costs
        earn_leg1 = leg1.supply_apy + (self.underlying_apy or 0)
        earn_leg2 = leg2.supply_apy * (leg1.ltv / 100)
        cost_leg1 = leg1.borrow_apy
        
        total_earn = earn_leg1 + earn_leg2
        total_cost = cost_leg1
        net = total_earn - total_cost
        
        return {
            'total_earn': total_earn,
            'total_cost': total_cost,
            'best_net': net,
            'leg1_earn': earn_leg1,
            'leg2_earn': earn_leg2,
            'effective_leverage': 1 + (leg1.ltv / 100)
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        returns = self.calculate_returns()
        
        base = {
            'type': 'cross-platform' if self.is_cross_platform else 'single',
            'platform': self.platform,
            'market': self.market,
            'collateral': self.collateral,
            'borrow': self.borrow,
            'supply_apy': self.legs[0].supply_apy if self.legs else None,
            'underlying': self.underlying_apy,
            'total_supply': self.total_supply_apy,
            'borrow_apy': self.legs[0].borrow_apy if self.legs else None,
            'spread': self.legs[0].spread if self.legs else 0,
            'ltv': self.first_ltv,
        }
        
        base.update(returns)
        
        if self.is_cross_platform:
            base['num_legs'] = self.num_legs
            base['path'] = self._format_path()
            base['legs'] = [self._leg_to_dict(leg) for leg in self.legs]
        else:
            base['c_url'] = self.legs[0].deposit_url if self.legs else ''
            base['b_url'] = self.legs[0].borrow_url if self.legs else ''
        
        return base
    
    def _format_path(self) -> str:
        """Format path string like 'ONyc@kamino -> USDC@jupiter'."""
        parts = []
        for leg in self.legs:
            platform_short = 'kam' if 'kamino' in leg.platform.lower() else 'jup'
            parts.append(f"{leg.deposit_token}@{platform_short}")
        return ' -> '.join(parts)
    
    def _leg_to_dict(self, leg: LoopLeg) -> dict:
        return {
            'platform': leg.platform,
            'market': leg.market,
            'deposit': leg.deposit_token,
            'borrow': leg.borrow_token,
            'supply_apy': leg.supply_apy,
            'borrow_apy': leg.borrow_apy,
            'ltv': leg.ltv
        }
