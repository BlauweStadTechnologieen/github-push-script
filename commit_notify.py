import requests
import send_email, respository_list

# GitHub repository info
OWNER           = "Blauwestadtechnologieen"
GITHUB_TOKEN    = "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"
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set. Please set the environment variable.")

# Function to get the latest commit hash from GitHub
def get_latest_commit() -> str:
    
    previous_commit_shas    = {}
    changed_repos           = []
    headers                 = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos                   = respository_list.remote_repositories()
    
    for repo in repos:

        try:
            url = GITHUB_API_URL.format(owner=OWNER, repo=repo)
            response = requests.get(url,headers = headers)
            print(response)
            print(f"Successfully fetched data for {repo}") 
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {repo}: {e}")
            continue

        if response.status_code == 200:
            commits = response.json()
            latest_commit_sha = commits[0]["sha"]
            print(f"Latest commit SHA for {repo}: {latest_commit_sha}")
            
            if repo not in previous_commit_shas or latest_commit_sha != previous_commit_shas[repo]:
                previous_commit_shas[repo] = latest_commit_sha
            
                changed_repos.append({
                    "repo"  : repo,
                    "sha"   : latest_commit_sha,
                    "url"   : url   
                })
            
        else:
            print(f"Error fetching commits for {repo}: {response.status_code}")
            print(f"Error details: {response.text}")

        if changed_repos:
            send_email.send_message(changed_repos, OWNER)
    
    return changed_repos

if __name__ == "__main__":
   get_latest_commit()