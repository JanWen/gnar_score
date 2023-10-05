from chalicelib import match_elo

elo, _ = match_elo.calculate_elo()
for i,j  in elo.items():
    print(j)