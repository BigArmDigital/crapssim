import typing

from crapssim.bet import Come, DontCome, DontPass, Field, Odds, PassLine, Place
from crapssim.strategy.odds import (
    DontPassOddsMultiplier,
    OddsMultiplier,
    PassLineOddsMultiplier,
)
from crapssim.strategy.single_bet import (
    BetCome,
    BetDontPass,
    BetField,
    BetPassLine,
    BetPlace,
    StrategyMode,
)
from crapssim.strategy.tools import (
    AddIfNotBet,
    AddIfPointOff,
    AddIfPointOn,
    AddIfTrue,
    AggregateStrategy,
    CountStrategy,
    Player,
    RemoveByType,
    RemoveIfTrue,
    Strategy,
    WinProgression,
)

class DontCome1xOdds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off and adds 1x Odds to the DontCome bet."""

    def __init__(
        self, dont_come_amount: float
    ) -> None:
        """Place a Don't Come bet with 2x odds.

        Parameters
        ----------
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.dont_come_amount = float(dont_come_amount)
        super().__init__(
            AddIfTrue(
                DontCome(dont_come_amount),
                lambda p: len(p.get_bets_by_type((DontCome,))) == 0,
            ),
            OddsMultiplier(DontCome, 1),
        )

    def __repr__(self) -> str:
        return (
            f"dont_come_amount={self.dont_come_amount})"
        )


class DontCome2xOdds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off and adds 2x Odds to the DontCome bet."""

    def __init__(
        self, dont_come_amount: float
    ) -> None:
        """Place a Don't Come bet with 2x odds.

        Parameters
        ----------
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.dont_come_amount = float(dont_come_amount)
        super().__init__(
            AddIfTrue(
                DontCome(dont_come_amount),
                lambda p: len(p.get_bets_by_type((DontCome,))) == 0,
            ),
            OddsMultiplier(DontCome, 2),
        )

    def __repr__(self) -> str:
        return (
            f"dont_come_amount={self.dont_come_amount})"
        )

class DontCome3xOdds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off and adds 3x Odds to the DontCome bet."""

    def __init__(
        self, dont_come_amount: float
    ) -> None:
        """Place a Don't Come bet with 2x odds.

        Parameters
        ----------
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.dont_come_amount = float(dont_come_amount)
        super().__init__(
            AddIfTrue(
                DontCome(dont_come_amount),
                lambda p: len(p.get_bets_by_type((DontCome,))) == 0,
            ),
            OddsMultiplier(DontCome, 3),
        )

    def __repr__(self) -> str:
        return (
            f"dont_come_amount={self.dont_come_amount})"
        )


class VariableOddsMultiplier(Strategy):
    """A strategy that applies variable odds multiplier based on the DontCome number."""
    
    def __init__(self, bet_type):
        self.bet_type = bet_type
        
    def get_multiplier(self, number: int) -> int:
        """Get the odds multiplier for a given number.
        
        Parameters
        ----------
        number : int
            The point number to check
            
        Returns
        -------
        int
            The odds multiplier to apply (1, 2, or 3)
        """
        if number in (6, 8):
            return 1
        elif number in (5, 9):
            return 2
        elif number in (4, 10):
            return 3
        return 1  # Default if no number is set yet
        
    def update_bets(self, player: Player) -> None:
        """Apply variable odds to the bet based on its number."""
        bets = player.get_bets_by_type((self.bet_type,))
        for bet in bets:
            if hasattr(bet, "number") and bet.number is not None:
                multiplier = self.get_multiplier(bet.number)
                # Check for existing odds bet
                odds_bets = [b for b in player.bets if isinstance(b, Odds) and 
                           b.base_type == self.bet_type and 
                           b.number == bet.number]
                if not odds_bets:
                    player.add_bet(Odds(self.bet_type, bet.number, bet.amount * multiplier))
                
    def completed(self, player: Player) -> bool:
        """Strategy is complete when all eligible bets have odds placed."""
        bets = player.get_bets_by_type((self.bet_type,))
        for bet in bets:
            if hasattr(bet, "number") and bet.number is not None:
                # Check if this bet has corresponding odds
                odds_exists = any(isinstance(b, Odds) and 
                                b.base_type == self.bet_type and 
                                b.number == bet.number 
                                for b in player.bets)
                if not odds_exists:
                    return False
        return True

class DontComeVariableOdds(AggregateStrategy):
    """Strategy that adds a DontCome bet when the point is Off and adds variable odds based on the DontCome number:
    - 6 or 8: 1x odds
    - 5 or 9: 2x odds
    - 4 or 10: 3x odds"""

    def __init__(
        self, dont_come_amount: float
    ) -> None:
        """Place a Don't Come bet with variable odds based on the number.

        Parameters
        ----------
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.dont_come_amount = float(dont_come_amount)
        super().__init__(
            AddIfTrue(
                DontCome(dont_come_amount),
                lambda p: len(p.get_bets_by_type((DontCome,))) == 0,
            ),
            VariableOddsMultiplier(DontCome),
        )

    def __repr__(self) -> str:
        return (
            f"dont_come_amount={self.dont_come_amount})"
        )