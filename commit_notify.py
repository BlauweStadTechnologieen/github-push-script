import requests
import send_email
from freshdesk_ticket import create_freshdesk_ticket
import shared_config
import repositories

# GitHub repository info
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"

if not shared_config.GITHUB_CONSTANTS["GITHUB_TOKEN"]:
    token_invalid_subject = "Invalid GitHug Token"
    token_invalid_message = "Your Github toekn in either invalud or expired. Please contact your administrator."
    create_freshdesk_ticket(token_invalid_message, token_invalid_subject)
    raise ValueError("GITHUB_TOKEN is not set. Please set the environment variable.")

# Function to get the latest commit hash from GitHub
def get_latest_commit(changed_local_repos:list) -> list:
        
    remote_repo_list    = []
    headers             = {"Authorization": f"token {shared_config.GITHUB_CONSTANTS['GITHUB_TOKEN']}"}
    repos               = repositories.remote_repositories()
    
    for repo in repos:

        try:
            url = GITHUB_API_URL.format(owner=shared_config.GITHUB_CONSTANTS["OWNER"], repo=repo)
            response = requests.get(url, headers = headers)
            print(response)
        except requests.exceptions.RequestException as e:
            print(custom_message)
            custom_message = f"Request failed for {repo}: {e}"
            custom_subject = f"Repository fetch failure."
            create_freshdesk_ticket(custom_message, custom_subject)
            
            continue

        from datetime import datetime

        if response.status_code == 200:
            commits = response.json()
            latest_commit_sha = commits[0]["sha"]
            latest_commit_date = commits[0]["commit"]["author"]["date"]
            latest_commit_id = commits[0]["author"]["id"]
            latest_commit_msg = commits[0]["commit"]["message"]
            
            remote_repo_list.append({
                "repo"  : repo,
                "sha"   : latest_commit_sha,
                "url"   : url,
                "date"  : latest_commit_date,
                "id"    : latest_commit_id,
                "msg"   : latest_commit_msg   
            })
            
        else:
            print(f"Error fetching commits for {repo}: {response.status_code}{response.text}{response.content}")
            custom_message = f"{response.content}{response.text}{response.status_code}"
            custom_subject = f"Error {response.status_code}"
            create_freshdesk_ticket(custom_message, custom_subject)

            continue

    if remote_repo_list:
        send_email.send_message(remote_repo_list, changed_local_repos, shared_config.GITHUB_CONSTANTS["OWNER"])
    
    return remote_repo_list