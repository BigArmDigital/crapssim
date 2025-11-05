import crapssim as craps
from crapssim.strategy import BetPassLine

table = craps.Table(seed=1234)
strat = BetPassLine(bet_amount=10)

table.add_player(strategy=strat)
table.run(max_rolls=20, verbose=True)