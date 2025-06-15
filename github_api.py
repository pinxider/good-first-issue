import requests
import os

token = os.getenv("GITHUB_TOKEN")

repo = "facebook/react"
url = f"https://api.github.com/repos/{repo}"
headers = {"Authorization": f"token {token}"} if token else {}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Success: ", response.status_code)
    data = response.json()
    print(data)
else:
    print(f"Failed: {response.status_code}")