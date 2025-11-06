from crapssim.bet import Bet, DontCome


class LayOdds(Bet):
    """
    Custom Lay Odds bet that attaches to a DontCome bet.

    Payouts (true odds):
        - 4 or 10: pay 1:2
        - 5 or 9:  pay 2:3
        - 6 or 8:  pay 5:6
    """

    def __init__(self, base_bet: DontCome, amount: float):
        # base_bet is the DontCome bet we attach odds to
        self.base_bet = base_bet
        self.number = base_bet.number
        self.amount = amount

        # Crapssim requires: a bet must have a .number attribute
        # and derive from Bet.
        super().__init__(amount=self.amount)

    @property
    def name(self):
        return f"LayOdds({self.number})"

    def resolve(self, roll, player, table):
        """
        Called by crapssim every roll.
        We implement DC lay odds rules:

        Win condition:
            - If roll is 7 → Lay odds win

        Lose condition:
            - If roll equals number (point for DC) → Lay odds lose

        Push:
            - Otherwise no action
        """

        dice_total = roll.total

        # --- Win on 7
        if dice_total == 7:
            payout = self.calculate_payout()
            player.bankroll += payout
            player.remove_bet(self)
            return f"won ${payout} on {self}"

        # --- Lose if the number hits
        if dice_total == self.number:
            player.bankroll -= self.amount
            player.remove_bet(self)
            return f"lost ${self.amount} on {self}"

        # --- Otherwise unresolved
        return None

    def calculate_payout(self):
        """
        True lay odds: Amount at risk wins at lower odds.
        E.g., $20 lay on 4 wins $10 (1:2)
        """

        num = self.number

        if num in (4, 10):
            return self.amount / 2           # 1:2
        elif num in (5, 9):
            return self.amount * (2/3)       # 2:3
        elif num in (6, 8):
            return self.amount * (5/6)       # 5:6
        else:
            raise ValueError(f"Invalid odds number: {num}")

    def __repr__(self):
        return f"LayOdds(number={self.number}, amount={self.amount})"
