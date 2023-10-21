
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt




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


def train_and_score(X_train, X_test, y_train, y_test):
    gnb = GaussianNB()
    model = gnb.fit(X_train, y_train)
    predictive_labels = gnb.predict(X_test)
    # print(predictive_labels)
    print(accuracy_score(y_test, predictive_labels))


def first_four_team():
    df = pd.read_csv('csv/first_four.csv')
    df["winningteam"] = df["winningteam"].apply(lambda x: 1 if x == 100 else 0)

    print("Train with level")
    X = df[["blue_level", "red_level"]]
    plt.scatter(x=df["blue_cs"], y=df["red_cs"], c=df["winningteam"])
    plt.show()
    y = df["winningteam"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    train_and_score(X_train, X_test, y_train, y_test)


    print("Train with cs")
    X = df[[ "blue_cs", "red_cs"]]
    y = df["winningteam"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    train_and_score(X_train, X_test, y_train, y_test)

    print("Train with level and cs")
    X = df[["blue_level", "red_level", "blue_cs", "red_cs"]]
    y = df["winningteam"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    train_and_score(X_train, X_test, y_train, y_test)


first_four_team()

print("FIRST FOUR PLAYER")
df = pd.read_csv('csv/first_four_player.csv')

X = df[
    [
        "level_1",
        "cs_1",
        "level_2",
        "cs_2",
        "level_3",
        "cs_3",
        "level_4",
        "cs_4",
        "level_5",
        "cs_5",
        "level_6",
        "cs_6",
        "level_7",
        "cs_7",
        "level_8",
        "cs_8",
        "level_9",
        "cs_9",
        "level_10",
        "cs_10",
    ]
]
df["winningteam"] = df["winningteam"].apply(lambda x: 1 if x == 100 else 0)

y = df["winningteam"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
train_and_score(X_train, X_test, y_train, y_test)


from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='adam', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1, max_iter=1000)
clf.fit(X_train, y_train)
predictive_labels = clf.predict(X_test)
print(accuracy_score(y_test, predictive_labels))

