import pandas as pd
import numpy as np


def f1():
    df = pd.read_csv("users.csv")
    top_5_users = df.sort_values(
        by="followers", ascending=False).head(5)["login"]
    top_5_logins = ",".join(top_5_users)
    print(top_5_logins)


def f2():
    df = pd.read_csv("users.csv")
    earliest_users = df.sort_values(by="created_at").head(5)["login"]
    earliest_logins = ",".join(earliest_users)
    print(earliest_logins)


def f4():
    df = pd.read_csv("users.csv")
    df["company"] = (
        df["company"]
        .str.strip()  # Trim whitespace
        .str.lstrip("@")  # Remove leading '@' symbol only once
        .str.upper()
        .str.split()
        .str[0]  # Convert to uppercase
    )

    most_common_company = (
        df["company"].replace("NONE", np.nan)
        .dropna()  # Remove rows with missing company information
        .value_counts()
        .idxmax()  # Get the most common company
    )
    company_counts = df["company"].value_counts().sort_values(ascending=False)
    print(list(company_counts))
    print(most_common_company)


def f5():
    df = pd.read_csv("repositories.csv")
    most_popular_language = (
        df["language"]
        .dropna()  # Remove rows with missing language information
        .value_counts()
        .idxmax()  # Get the most common programming language
    )
    print(most_popular_language)


f4()
