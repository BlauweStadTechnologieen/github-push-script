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
        
    repo_list   = []
    headers     = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos       = respository_list.remote_repositories()
    
    for repo in repos:

        try:
            url = GITHUB_API_URL.format(owner=OWNER, repo=repo)
            response = requests.get(url,headers = headers)
            print(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {repo}: {e}")
            
            continue

        if response.status_code == 200:
            commits = response.json()
            latest_commit_sha = commits[0]["sha"]
            latest_commit_date = commits[0]["commit"]["author"]["date"]
            latest_commit_id = commits[0]["author"]["id"]
            
            repo_list.append({
                "repo"  : repo,
                "sha"   : latest_commit_sha,
                "url"   : url,
                "date"  : latest_commit_date,
                "id"    : latest_commit_id   
            })
            
        else:
            print(f"Error fetching commits for {repo}: {response.status_code}")
            print(f"Error details: {response.text}")

            continue

    if repo_list:
        send_email.send_message(repo_list, OWNER)
    
    return repo_list

if __name__ == "__main__":
   get_latest_commit()