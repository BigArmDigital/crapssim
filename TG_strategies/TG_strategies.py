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
        """Place a Don't Come bet with 1x odds.

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


class DontCome1xOddsNextPoint(AggregateStrategy):
    """Strategy that adds a DontCome bet only when a point is newly established, and adds 1x Odds to the DontCome bet.
    After the Don't Come bet loses, waits for the next point to be established before placing another bet."""

    def __init__(
        self, dont_come_amount: float
    ) -> None:
        """Place a Don't Come bet with 1x odds.

        Parameters
        ----------
        dont_come_amount
            The amount of the DontCome bet.
        """
        self.dont_come_amount = float(dont_come_amount)
        self.current_point_status = "Off"  # Current point status
        self.current_point_number = None   # Current point number
        self.waiting_for_resolution = False  # True when waiting for current point to resolve
        self.initial_point = True  # True for the first point only
        super().__init__(
            AddIfTrue(
                DontCome(dont_come_amount),
                lambda p: self.should_place_bet(p)
            ),
            OddsMultiplier(DontCome, 1),
        )

    def should_place_bet(self, player: Player) -> bool:
        """Determine if we should place a new Don't Come bet."""
        print(f"[DEBUG] === starting should_place_bet ===")
        # Get current point info
        current_number = player.table.point.number if player.table.point.status == "On" else None
        
        # No new bets if we already have one
        if len(player.get_bets_by_type((DontCome,))) > 0:
            print(f"[DEBUG] Already have a Don't Come bet - not placing new bet")
            print(f"[DEBUG] === end should_place_bet already have a dontcome bet ===")
            return False
            
        # Point must be ON to place a Don't Come bet
        if player.table.point.status != "On":
            print(f"[DEBUG] Point is Off - not placing new bet")
            print(f"[DEBUG] === end should_place_bet player.table.point.status On ===")
            return False
            
        # After losing a bet, we must wait for current point to resolve
        if self.waiting_for_resolution:
            print(f"[DEBUG] Waiting for current point {current_number} to resolve")
            print(f"[DEBUG] === end should_place_bet self.waiting_for_resolution ===")
            return False
        
        # Only place bet on the initial point or after a point resolves
        if self.initial_point and player.table.point.status == "On":
            print(f"[DEBUG] Initial point {current_number} established - placing new bet")
            self.initial_point = False
            print(f"[DEBUG] === end should_place_bet self.initial_point and player.table.point.status On ===")
            return True
            
        # For subsequent bets, require point to be newly established
        point_newly_established = (player.table.point.status == "On" and
                                self.current_point_status == "Off")
        print(f"[DEBUG] point_newly_established: {point_newly_established}  because  player.table.point.status: {player.table.point.status}  and  self.current_point_status: {self.current_point_status}")                                
        if point_newly_established:
            print(f"[DEBUG] New point {current_number} established - placing new bet")
            print(f"[DEBUG] === end should_place_bet point_newly_established TRUE ===")
            return True
            
        print(f"[DEBUG] === end should_place_bet No conditions met for placing new bet (current point {current_number})")
        return False
    

    def update_bets(self, player: Player) -> None:
        """Update bets and track state changes."""
               # Get current point info for this update
        current_point_status = player.table.point.status
        current_point_number = player.table.point.number if player.table.point.status == "On" else None

        # Print current state
        print(f"[DEBUG] --- Start of update_bets ---")
        print(f"[DEBUG] Current roll: {player.table.dice.total if player.table.dice else None}")
        print(f"[DEBUG] Point status: {current_point_status} (prev: {self.current_point_status})")
        print(f"[DEBUG] Point number: {current_point_number} (prev: {self.current_point_number})")
        print(f"[DEBUG] Current state: waiting_for_resolution={self.waiting_for_resolution}")
        
        # Check for lost bets BEFORE any updates
        had_dont_come = len(player.get_bets_by_type((DontCome,))) > 0
        
        # Immediately check if we lost our Don't Come bet by checking current bets
        # This ensures waiting_for_resolution is set before any new bets are considered
        if had_dont_come:
            current_dont_come_bets = player.get_bets_by_type((DontCome,))
            if len(current_dont_come_bets) == 0:  # We lost the bet
                print(f"[DEBUG] Lost Don't Come bet - waiting for point {current_point_number} to resolve")
                self.waiting_for_resolution = True
                self.initial_point = False
        
        # Update our state after checking for losses but before processing new bets
        self.current_point_status = current_point_status
        self.current_point_number = current_point_number
        
        # Now process any new bets
        super().update_bets(player)
        print(f"[DEBUG] End state: waiting_for_resolution={self.waiting_for_resolution}, point={self.current_point_number}")
        print(f"[DEBUG] --- End of update_bets ---")
        
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