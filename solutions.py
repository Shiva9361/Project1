import pandas as pd

users = pd.read_csv("user.csv")
# repos = pd.read_csv("repos.csv")
print(users.describe())
