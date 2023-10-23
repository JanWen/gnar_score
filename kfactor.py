
from chalicelib.elo import calculate_elo
from chalicelib.tournaments import Tournaments
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import numpy as np
from chalicelib.model import load_model

"""
Tune K_FACTOR of the elo model by calculating the mean squared error of the model for different values of K_FACTOR
"""

tournaments = Tournaments()

df, features, model = load_model()

errors = []
for i in range(10, 100, 5):
    K_FACTOR = i
    elo, back_test, mean_sq_er = calculate_elo(tournaments, k_factor=K_FACTOR, df=df, model=model)
    errors.append((K_FACTOR, mean_sq_er))
    # print(elo)

sorted_errors = sorted(errors, key=lambda x: x[1])
for i,j in sorted_errors[:5]:
    print(i, round(j, 3))