import requests
import time
import send_email

# GitHub repository info
OWNER           = "blauwestadtechnologieen"
GITHUB_TOKEN    = "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"
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/commits"

# Function to get the latest commit hash from GitHub
def get_latest_commit():
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    repos   = ["Experts", "Include", "Scripts", "Files"]
    
    for repo in repos:
                
        url = GITHUB_API_URL.format(owner=OWNER, repo=repos)
        print(url)
        
        response = requests.get(url, headers = headers)

    if response.status_code == 200:
        commits = response.json()
        return commits[0]['sha']
    else:
        print(f"Error fetching commits.{response.status_code}")
        return None

# Function to monitor GitHub for new commits and send email
def monitor_commits():
    
    print("This is a testing print")
    
    last_commit_sha = None
    
    while True:
        current_commit_sha = get_latest_commit()
        
        if current_commit_sha != last_commit_sha:
            last_commit_sha = current_commit_sha
            send_email.send_message(current_commit_sha)
            print(current_commit_sha)
        
        
        # Check for new commits every 10 minutes
        time.sleep(600)

# Run the monitor function
if __name__ == "__main__":
    monitor_commits()
