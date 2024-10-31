from datetime import datetime
from collections import Counter
import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


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
    print(language_counts)


def f7():
    repos_df = pd.read_csv("repositories.csv")

    # Group by language and calculate the average number of stars
    average_stars = repos_df.groupby(
        "language")["stargazers_count"].mean().sort_values(ascending=False)

    # Get the language with the highest average stars
    highest_avg_stars_language = average_stars.idxmax()
    print(highest_avg_stars_language)


def f8():
    # Load user data
    df = pd.read_csv("users.csv")

    # Calculate leader_strength
    df["leader_strength"] = df["followers"] / (1 + df["following"])

    # Sort by leader_strength in descending order and select the top 5 users
    top_leaders = df.sort_values(
        by="leader_strength", ascending=False).head(5)["login"]
    top_leader_logins = ",".join(top_leaders)
    print(top_leader_logins)


def f9():
    df = pd.read_csv("users.csv")
    print(round(df["followers"].corr(df["public_repos"]), 3))


def f10():
    df = pd.read_csv("users.csv")

    X = df["public_repos"].values.reshape(-1, 1)
    y = df["followers"].values

    model = LinearRegression()
    model.fit(X, y)

    followers_per_repo = round(model.coef_[0], 3)
    print(followers_per_repo)


def f11():
    df = pd.read_csv("repositories.csv")
    correlation = df['has_projects'].dropna().astype(
        int).corr(df['has_wiki'].dropna().astype(int))
    print(round(correlation, 3))


def f12():
    df = pd.read_csv("users.csv")

    # Drop NaN values from the following column before calculating the mean
    hireable_avg = df[df["hireable"] == True]["following"].dropna().mean()
    non_hireable_avg = df[df["hireable"] == False]["following"].dropna().mean()

    print(f"Average following for hireable users: {round(hireable_avg, 3)}")
    print(
        f"Average following for non-hireable users: {round(non_hireable_avg, 3)}")


def f13():
    df = pd.read_csv("users.csv")
    df_with_bios = df[df["bio"].notna()]
    df_with_bios["bio_length"] = df_with_bios["bio"].str.split().str.len()
    X = df_with_bios["bio_length"].values.reshape(-1, 1)
    y = df_with_bios["followers"].values
    model = LinearRegression()
    model.fit(X, y)
    slope = round(model.coef_[0], 3)
    print(f"Slope of followers on bio word count: {slope}")


def f14():
    weekend_counts = Counter()

    with open('repositories.csv', 'r', encoding='utf-8') as repo_file:
        csv_reader = csv.DictReader(repo_file)

        for record in csv_reader:
            timestamp = record.get('created_at', '')
            if timestamp:
                creation_date = datetime.fromisoformat(timestamp[:-1])

                if creation_date.weekday() in [5, 6]:
                    login = record['login']
                    weekend_counts[login] += 1

    top_creators = weekend_counts.most_common(5)
    top_logins = [user[0] for user in top_creators]
    print(", ".join(top_logins))


def f15():
    df = pd.read_csv("users.csv")
    df_f = df[df["hireable"] == False]
    print(df_f.count())  # no value so NaN


def f16():
    df = pd.read_csv("users.csv")
    df['surname'] = df['name'].str.split().str[-1]
    common_surnames = df['surname'].value_counts()
    print(common_surnames)


f1()
f2()
f3()
f4()
f5()
f6()
f7()
f8()
f9()
f10()
f11()
f12()
f13()
f14()
f15()
f16()
