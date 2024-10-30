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


def f3():
    df = pd.read_csv("repositories.csv")

    # Filter out missing license names, count occurrences, and get the top 3
    print(df["license_name"].unique())
    popular_licenses = (
        df["license_name"]
        # .replace("other", np.nan)
        .dropna()  # Remove rows with missing license names
        .value_counts()
        .head(3)  # Get the top 3 licenses
        .index.tolist()
    )

    # Format the result as a comma-separated string
    top_licenses = ",".join(popular_licenses)
    print(top_licenses)


def f5():
    df = pd.read_csv("repositories.csv")
    most_popular_language = (
        df["language"]
        .dropna()  # Remove rows with missing language information
        .value_counts()
        .idxmax()  # Get the most common programming language
    )
    print(most_popular_language)


def f6():

    # Load and filter user data for those who joined after 2020
    users_df = pd.read_csv("users.csv")
    recent_users = users_df[pd.to_datetime(
        users_df["created_at"]) > "2020-12-31"]

    # Load repository data and filter for repositories owned by recent users
    repos_df = pd.read_csv("repositories.csv")
    filtered_repos = repos_df[repos_df["login"].isin(recent_users["login"])]

    # Find the second most popular language
    language_counts = filtered_repos["language"].dropna().value_counts()
    # Second most popular
    second_most_popular_language = language_counts.index[1]
    print(second_most_popular_language)


f2()
repos_df = pd.read_csv("repositories.csv")
repos_with_license = repos_df[repos_df['license_name'].notnull()]
top_3_licenses = repos_with_license['license_name'].value_counts().head(
    3).index.tolist()
print("Ans 3 : Top 3 most popular licenses:", ", ".join(top_3_licenses))
