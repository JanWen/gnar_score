import pandas as pd

shutdown = pd.read_csv('shutdown.csv')
shutdown.sort_values(by=["platformgameid", "gametime"], inplace=True)
shutdown.head()

df = shutdown#[["platformgameid", "gametime", "shutdown_held_1"]]
df.head()
df["platformgameid"].value_counts()
print(len(df["platformgameid"].unique()))

new_row = {
    "platformgameid": None,
    "gametime": None,
    "shutdown_held_1": None,
    "shutdown_held_2": None,
    "shutdown_held_3": None,
    "shutdown_held_4": None,
    "shutdown_held_5": None,
    "shutdown_held_6": None,
    "shutdown_held_7": None,
    "shutdown_held_8": None,
    "shutdown_held_9": None,
    "shutdown_held_10": None,
}

new = []
prev_row = None
for _, row in shutdown.iterrows():
    # print(row)
    if prev_row is None:
        prev_row = row
        new_row["platformgameid"] = row["platformgameid"]
        new_row["gametime"] = row["gametime"]
        for i in range(1, 11):
            new_row["shutdown_held_" + str(i)] = row["shutdown_held_" + str(i)]
        continue
    elif row["platformgameid"] != prev_row["platformgameid"]:
        new.append(new_row)
        new_row = {
            "platformgameid": row["platformgameid"],
            "gametime": row["gametime"],
            # "shutdown_held_1": row["shutdown_held_1"]
        }
        for i in range(1, 11):
            new_row["shutdown_held_" + str(i)] = row["shutdown_held_" + str(i)]
    elif row["platformgameid"] == new_row["platformgameid"]:
        for i in range(1, 11):
            if row["shutdown_held_" + str(i)] > prev_row["shutdown_held_" + str(i)]:
                new_row["shutdown_held_" + str(i)] += row["shutdown_held_" + str(i)]- prev_row["shutdown_held_" + str(i)] 


    prev_row = row

df = pd.DataFrame(new)
print(df)