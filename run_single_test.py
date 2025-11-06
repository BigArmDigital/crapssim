import crapssim as craps
from TG_strategies.TG_strategies import DontCome2Odds

table = craps.Table(seed=1234)
strat = DontCome2Odds(base_amount=10)

table.add_player(strategy=strat, bankroll=200, name="Todd")
table.run(max_rolls=10, verbose=True)

print("\nFINAL BANKROLL:", table.players[0].bankroll)
