import crapssim as craps
from TG_strategies.TG_strategies import DontCome1xOdds, DontCome2xOdds, DontCome3xOdds, DontComeVariableOdds, DontCome1xOddsNextPoint

#table = craps.Table(seed=1234)
table = craps.Table()

#table.add_player(strategy=DontCome1xOdds(dont_come_amount=5), bankroll=300, name="Todd 1X")
#table.add_player(strategy=DontCome2xOdds(dont_come_amount=5), bankroll=300, name="Todd 2X")
#table.add_player(strategy=DontCome3xOdds(dont_come_amount=5), bankroll=300, name="Todd 3X")
#table.add_player(strategy=DontComeVariableOdds(dont_come_amount=5), bankroll=300, name="Todd 1X 2X 3X")
table.add_player(strategy=DontCome1xOddsNextPoint(dont_come_amount=5), bankroll=300, name="Todd 1X Next Point")

table.run(max_rolls=120, verbose=True)

print("\nFINAL RESULTS")
for p in table.players:
    print(f"  {p.name}: Bankroll=${p.bankroll}")