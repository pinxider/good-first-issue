import requests
import os

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"} if token else {}

def get_repo_metadata(repo_name: str) -> dict[str, any] | None:
    
    url = f"https://api.github.com/repos/{repo_name}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data['full_name'],
                'stars': data['stargazers_count'],
                'language': data['language'],
                'description': data['description'],
                'forks': data['forks_count'],
                'open_issues': data['open_issues_count'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at']
            }
        else:
            print(f"Failed to fetch {repo_name}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {repo_name}: {e}")
        return None

# def get_contributors(repo_name):
#     
#     url = f"https://api.github.com/repos/{repo_name}/stats/contributors"
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except requests.RequestException as e:
#         print(f"Error fetching contributors for {repo_name}: {e}")
#         return None

# def get_commit_activity(repo_name):
#     
#     url = f"https://api.github.com/repos/{repo_name}/stats/commit_activity"
#     response = requests.get(url, headers=headers)
#     
#     if response.status_code == 200:
#         return response.json()
#     return None

def get_issues(repo_name: str, labels: str | None = None, since: str | None = None) -> list[dict[str, any]]:
    url = f"https://api.github.com/repos/{repo_name}/issues"
    params = {"state": "open"}
    
    if labels:
        params["labels"] = labels
    if since:
        params["since"] = since
        
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get issues for {repo_name}: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching issues for {repo_name}: {e}")
        return []

def get_readme_file(repo_name: str) -> str | None:
    """Check if repository has a README.md file."""
    url = f"https://api.github.com/repos/{repo_name}/contents/README.md"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("html_url")
        return None
    except requests.RequestException:
        return None

def get_contributing_file(repo_name: str) -> str | None:
    """Check if repository has a CONTRIBUTING.md file."""
    url = f"https://api.github.com/repos/{repo_name}/contents/CONTRIBUTING.md"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("html_url")
        return None
    except requests.RequestException:
        return None

repos = [
    "facebook/react",
    "microsoft/vscode", 
    "python/cpython"
]

# for repo in repos:
#     info = get_repo_metadata(repo)
#     contributors = get_contributors(repo)
#     activity = get_commit_activity(repo)
#     issues = get_issues(repo, "good first issue")
#     if info:
#         print(f"{info['name']}: {info['stars']} stars ({info['language']})")
#         print(f"  {info['description']}")
#         print()
#     if contributors:
#         print(f"{len(contributors)} contributors")
#     if activity:
#         print(activity)
#     if issues: 
#         print(issues)