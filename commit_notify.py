import requests
import send_email, respository_list
from freshdesk_ticket import create_freshdesk_ticket

# GitHub repository info
OWNER           = "Blauwestadtechnologieen"
GITHUB_TOKEN    = "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"
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set. Please set the environment variable.")

# Function to get the latest commit hash from GitHub
def get_latest_commit(changed_local_repos:list) -> list:
        
    remote_repo_list   = []
    headers     = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos       = respository_list.remote_repositories()
    
    for repo in repos:

        try:
            url = GITHUB_API_URL.format(owner=OWNER, repo=repo)
            response = requests.get(url,headers = headers)
            print(response)
        except requests.exceptions.RequestException as e:
            custom_message = f"Request failed for {repo}: {e}"
            custom_subject = f"Repo retrieval failure"
            create_freshdesk_ticket(custom_message, custom_subject)
            print(custom_message)
            
            continue

        if response.status_code == 200:
            commits = response.json()
            latest_commit_sha = commits[0]["sha"]
            latest_commit_date = commits[0]["commit"]["author"]["date"]
            latest_commit_id = commits[0]["author"]["id"]
            
            remote_repo_list.append({
                "repo"  : repo,
                "sha"   : latest_commit_sha,
                "url"   : url,
                "date"  : latest_commit_date,
                "id"    : latest_commit_id   
            })
            
        else:
            print(f"Error fetching commits for {repo}: {response.status_code}")
            print(f"Error details: {response.text}")
            create_freshdesk_ticket(response.text, response.status_code)

            continue

    if remote_repo_list:
        send_email.send_message(remote_repo_list, changed_local_repos, OWNER)
    
    return remote_repo_list