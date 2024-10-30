import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import os
import csv
from dotenv import load_dotenv

load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"


def create_user_csv():
    required_data = ["login", "name", "company", "location", "email",
                     "hireable", "bio", "public_repos", "followers", "following", "created_at"]

    with open("user.csv", "w", newline='', encoding='utf-8') as user_file:
        writer = csv.DictWriter(user_file, fieldnames=required_data)
        writer.writeheader()

        for page in range(1, 7):
            search_url = f"{BASE_URL}/search/users?q=location:Tokyo&followers:>200&per_page=100&page={page}"
            response = requests.get(search_url, auth=HTTPBasicAuth(
                GITHUB_USERNAME, GITHUB_TOKEN))

            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                continue

            items = response.json().get('items', [])

            for user in items:
                user_data_url = f"{BASE_URL}/users/{user['login']}"
                user_info = requests.get(user_data_url, auth=HTTPBasicAuth(
                    GITHUB_USERNAME, GITHUB_TOKEN)).json()

                row = {field: user_info.get(field, "")
                       for field in required_data}
                if "company" in row:
                    row["company"] = str(
                        row["company"]).strip().upper().lstrip("@")
                writer.writerow(row)


def create_repo_csv():
    df = pd.read_csv("user.csv")
    users = df["login"]
    required_data = ["login", "full_name", "created_at", "stargazers_count",
                     "watchers_count", "language", "has_projects", "has_wiki", "license_name"]

    with open("repositories.csv", "w", newline='', encoding='utf-8') as repo_file:
        writer = csv.DictWriter(repo_file, fieldnames=required_data)
        writer.writeheader()

        for user in users:
            repo_datas = get_user_repos(user)
            for repo_data in repo_datas:
                row = {
                    "login": user,
                    "full_name": repo_data.get("full_name", ""),
                    "created_at": repo_data.get("created_at", ""),
                    "stargazers_count": repo_data.get("stargazers_count", 0),
                    "watchers_count": repo_data.get("watchers_count", 0),
                    "language": repo_data.get("language", ""),
                    "has_projects": "true" if repo_data.get("has_projects") else "false",
                    "has_wiki": "true" if repo_data.get("has_wiki") else "false",
                    "license_name": repo_data.get("license", {}).get("key", "")
                }
                writer.writerow(row)


def get_user_repos(username):
    repos_url = f"{BASE_URL}/users/{username}/repos?per_page=500&page=1"
    response = requests.get(repos_url, auth=HTTPBasicAuth(
        GITHUB_USERNAME, GITHUB_TOKEN))
    return response.json() if response.status_code == 200 else []


def scrape_tokyo_users_and_repos():
    create_user_csv()
    # create_repo_csv()


scrape_tokyo_users_and_repos()
