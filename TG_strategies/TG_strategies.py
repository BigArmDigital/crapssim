from crapssim.strategy import Strategy

from crapssim.bet import Place, DontCome
from TG_strategies.TG_custom_bets import LayOdds

class DontCome2Odds(Strategy):
    """
    Places 6 and 8 every roll (when point is on)
    Adds a single DC bet
    Adds 2x odds behind the DC after it travels
    """

    def __init__(self, base_amount=10):
        super().__init__()
        self.base = base_amount

    def make_bets(self, player, table):
        point = table.point_number

        # 1. Place 6 & 8 when point is ON
        if point is not None:
            for num in (6, 8):
                if not player.has_bet(Place, number=num):
                    player.add_bet(Place(num, amount=self.base))

        # 2. Add DC if point is ON and none exists
        if point is not None:
            if not player.has_bet(DontCome):
                player.add_bet(DontCome(self.base))

        # 3. Add 2x lay odds if DC has traveled
        for bet in player.get_bets(DontCome):
            if bet.number is not None:  # DC is working behind a number
                if not player.has_bet(LayOdds, number=bet.number):
                    odds_amount = self.base * 2
                    player.add_bet(LayOdds(bet, odds_amount))

    def update_bets(self, player):
        """
        No post-resolution behavior needed for this strategy.
        """
        pass

    def completed(self, player):
        """
        Strategy runs until the table says the session ends.
        """
        return False
