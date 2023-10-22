
from chalicelib.elo import calculate_elo
from chalicelib.tournaments import Tournaments
tournaments = Tournaments()


errors = []
for i in range(10, 100, 5):
    K_FACTOR = i
    elo, back_test, mean_sq_er = calculate_elo(tournaments, k_factor=K_FACTOR)
    errors.append((K_FACTOR, mean_sq_er))
    # print(elo)

sorted_errors = sorted(errors, key=lambda x: x[1])
for i,j in sorted_errors[:5]:
    print(i, round(j, 3))