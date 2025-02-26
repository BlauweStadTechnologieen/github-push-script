import requests
import time
import send_email, respository_list

# GitHub repository info
OWNER           = "Blauwestadtechnologieen"
GITHUB_TOKEN    = "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"
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"
GITHUB_API      = f"https://github.com/BlauweStadTechnologieen/github-push-script.git"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set. Please set the environment variable.")

# Function to get the latest commit hash from GitHub
def get_latest_commit():
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos   = respository_list.repository_list()

    latest_commit = None
    latest_commit_data = []
    
    for repo in repos:

        try:
            url = GITHUB_API_URL.format(owner=OWNER, repo=repo)
            print(url)
            response = requests.get(url,headers = headers)
            response.raise_for_status()
            print(f"Successfully fetched data for {repo}") 
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {repo}: {e}")
            continue

        if response.status_code == 200:
            commits = response.json()
            print(f"Latest commit SHA for {repo}: {commits[0]['sha']}")
            latest_commit = commits[0]['sha']
            
            commit_information = {
                "repo"  : repo,
                "sha"   : latest_commit,
                "url"   : url   
            }

            latest_commit_data.append(commit_information)
            
        else:
            print(f"Error fetching commits for {repo}: {response.status_code}")
            print(f"Error details: {response.text}")

    if latest_commit_data:
        send_email.send_message(latest_commit_data, OWNER)
    
    print(f"Latest commit across all repos: {latest_commit}") 
    return latest_commit

# Function to monitor GitHub for new commits and send email
def monitor_commits():
        
    last_commit_sha = None
    
    while True:
        
        current_commit_sha = get_latest_commit()
        
        if current_commit_sha != last_commit_sha:
            last_commit_sha = current_commit_sha
        else:
            print("No new commits yet...")
        
        # Check for new commits every 10 minutes
        time.sleep(600)

# Run the monitor function
if __name__ == "__main__":
    monitor_commits()
