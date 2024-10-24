import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


BASE_URL = "https://api.github.com"


def create_user_csv():
    search_url = f"""{
        BASE_URL}/search/users?q=location:Tokyo&followers:>200&per_page=100"""
    response = requests.get(search_url, auth=HTTPBasicAuth(
        GITHUB_USERNAME, GITHUB_TOKEN))
    # print(response.text)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")

    required_data = ["login", "name", "company", "location", "email",
                     "hireable", "bio", "public_repos", "followers", "following", "created_at"]

    data = response.json()
    items = data.get('items', [])

    with open("user.csv", "w") as user_file:

        for field in required_data:
            user_file.write(f"{field},")
        user_file.write("\n")

        for user in items:
            # print(user)
            user_data_url = f"{BASE_URL}/users/{user['login']}"
            user_info = requests.get(user_data_url, auth=HTTPBasicAuth(
                GITHUB_USERNAME, GITHUB_TOKEN)).json()

            # print(user_info)
        # users.append(user_info)
            for field in required_data:
                try:
                    if (field == "company"):
                        value = str(user_info[field]).strip(
                            ' \t\n\r\n@').strip().upper()
                        user_file.write(
                            f'"{value}",')
                    elif user_info[field] == None:
                        user_file.write(",")
                    elif user_info[field] == True:
                        user_file.write("true,")
                    elif user_info[field] == False:
                        user_file.write("false,")
                    else:
                        user_file.write(f'"{user_info[field]}",')
                except:
                    user_file.write(f",")
            user_file.write("\n")


def create_repo_csv():
    df = pd.read_csv("user.csv")
    users = df["login"]
    for user in users:
        repo_data = get_user_repos(user)
        print(repo_data)


def get_user_repos(username):
    repos_url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(repos_url, auth=HTTPBasicAuth(
        GITHUB_USERNAME, GITHUB_TOKEN))

    if response.status_code == 200:
        return response.json()
    else:
        return []


def scrape_tokyo_users_and_repos():
    # create_user_csv()

    create_repo_csv()


scrape_tokyo_users_and_repos()
