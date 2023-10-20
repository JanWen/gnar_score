
import pandas as pd



df = pd.read_csv('first_four.csv')

def explore():
    print(df)


    blue_adv = df[df["blue_level"] > df["red_level"]]
    print("Blue level > red level", len(blue_adv))
    blue_adv_win = blue_adv[blue_adv["winningteam"] == 100]
    print("Blue level > red level and blue won", len(blue_adv_win))
    print(len(blue_adv_win)/len(blue_adv))
    blue_adv = df[df["blue_cs"] > df["red_cs"]]
    print("Blue cs > red cs", len(blue_adv))
    blue_adv_win = blue_adv[blue_adv["winningteam"] == 100]
    print("Blue cs > red cs and blue won", len(blue_adv_win))
    print(len(blue_adv_win)/len(blue_adv))

# Import libraries and classes required for this example:
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

X = df[["blue_level", "red_level", "blue_cs", "red_cs"]]
y = df["winningteam"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


gnb = GaussianNB()
# Train the classifier:
model = gnb.fit(X_train, y_train)
# Make predictions with the classifier:
predictive_labels = gnb.predict(X_test)
print(predictive_labels)
# Evaluate label (subsets) accuracy:
print(accuracy_score(y_test, predictive_labels))