import requests
import send_email
from freshdesk_ticket import create_freshdesk_ticket
import settings_mapper
import repositories
import error_handler

# GitHub repository info
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"

def github_token_validation() -> bool:
    """Checks for the presence and the valitity of the user-specified GitHub token in the .env file."""
    try:
        
        if not settings_mapper.GITHUB_CONSTANTS["GITHUB_TOKEN"]:
            raise KeyError("GITHUB_TOKEN is not set. Please set the environment variable.")
               
    except KeyError as e:
        error_handler.report_error("No Github Token Specified", f"{e}")
        return False

    except Exception as e:
        error_handler.report_error("Invalid GitHub Token", f"{e}")
        return False

    return True

# Function to get the latest commit hash from GitHub
def get_latest_commit(changed_local_repos:list) -> list:
    
    """Retrieves the latest commits via the GitHub API, checks for any changes and displays them in a email sent to the user."""    
    
    if github_token_validation():
    
        remote_repo_list    = []
        headers             = {"Authorization": f"token {settings_mapper.GITHUB_CONSTANTS['GITHUB_TOKEN']}"}
        repos               = repositories.remote_repositories()
        url                 = GITHUB_API_URL.format(owner = settings_mapper.GITHUB_CONSTANTS["OWNER"], repo=repo)

        for repo in repos:

            try:
                response = requests.get(url, headers = headers)
                print(response)
            except requests.exceptions.RequestException as e:
                custom_message = f"Request failed for {repo}: {e}"
                custom_subject = f"Repository fetch failure."
                error_handler.report_error(custom_subject, custom_message)
                
                continue

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
                error_handler.report_error(custom_subject, custom_message)

                continue

        if remote_repo_list:
            send_email.send_message(remote_repo_list, changed_local_repos, settings_mapper.GITHUB_CONSTANTS["OWNER"])
    
    return remote_repo_list