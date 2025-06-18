import requests
import os

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

def get_repo_metadata(repo_name):
    
    url = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['full_name'],
            'stars': data['stargazers_count'],
            'language': data['language'],
            'description': data['description']
        }
    else:
        print(f"Failed to fetch {repo_name}: {response.status_code}")
        return None

def get_contributors(repo_name):
    
    url = f"http://api.github.com/repos/{repo_name}/stats/contributors"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def get_commit_activity(repo_name):
    
    url = f"https://api.github.com/repos/{repo_name}/stats/commit_activity"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# def code_frequency(repo_name)

repos = [
    "facebook/react",
    "microsoft/vscode", 
    "python/cpython"
]

for repo in repos:
    info = get_repo_metadata(repo)
    contributors = get_contributors(repo)
    activity = get_commit_activity(repo)
    if info:
        print(f"{info['name']}: {info['stars']} stars ({info['language']})")
        print(f"  {info['description']}")
        print()
    if contributors:
        print(f"{len(contributors)} contributors")
    if activity:
        print(activity)