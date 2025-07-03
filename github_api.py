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

def analyze_repository(repo_name: str, updated_after) -> dict[str, any]:
    """Complete repository analysis including metadata, issues, and files."""
    from time_utils import seconds_since_update, SECONDS_IN_30_DAYS
    import pandas as pd

    metadata = get_repo_metadata(repo_name)
    if metadata is None:
        return {"error": "Repository not found or private", "metadata": None}
    
    good_first_issues = get_issues(repo_name, "good first issue", updated_after.isoformat())
    good_first_count = len(good_first_issues) if good_first_issues else 0
    
    # Convert to Panda DataFrame
    if good_first_issues:
        good_first_issues_df = pd.DataFrame([{
            'title': issue['title'],
            'url': issue['html_url'],
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at'],
            'comments': issue['comments']
        } for issue in good_first_issues])
    else:
        good_first_issues_df = pd.DataFrame()
    
    secs_since_update = seconds_since_update(metadata['updated_at'])
    readme_link = get_readme_file(repo_name)
    contributing_link = get_contributing_file(repo_name)
    

    readme_status = {"icon": "✅", "color": "green"} if readme_link else {"icon": "❌", "color": "red"}
    contributing_status = {"icon": "✅", "color": "green"} if contributing_link else {"icon": "❌", "color": "red"}
    good_first_status = {"icon": "✅", "color": "green"} if good_first_count > 0 else {"icon": "❌", "color": "red"}
    update_status = {"icon": "✅", "color": "green"} if secs_since_update <= SECONDS_IN_30_DAYS else {"icon": "❌", "color": "red"}

    formatted_metadata = {
        'Full Name': metadata['name'],
        'Primary Language': metadata['language'],
        'Stars': metadata['stars'],
        'Forks': metadata['forks'],
        'Description': metadata['description']
    }
    
    return {
        "metadata": formatted_metadata,
        "good_first_issues_df": good_first_issues_df,
        "good_first_count": good_first_count,
        "secs_since_update": secs_since_update,
        "readme_link": readme_link,
        "contributing_link": contributing_link,
        "status": {
            "readme": readme_status,
            "contributing": contributing_status,
            "good_first": good_first_status,
            "update": update_status
        }
    }