


import pandas as pd


wins = pd.read_csv('wins.csv')

rolling_avg = pd.read_csv("kd_rolling_avg.csv")



rolling_avg = wins.merge(rolling_avg, on="platformgameid")

print(rolling_avg)


# Import libraries and classes required for this example:
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

X = rolling_avg[["avg_kills", "avg_deaths", "avg_win", "side"]]
y = rolling_avg["winningteam"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


gnb = GaussianNB()
# Train the classifier:
model = gnb.fit(X_train, y_train)
# Make predictions with the classifier:
predictive_labels = gnb.predict(X_test)
print(predictive_labels)
# Evaluate label (subsets) accuracy:
print(accuracy_score(y_test, predictive_labels))