import requests
import send_email
from freshdesk_ticket import create_freshdesk_ticket
import settings_mapper
import repositories
import error_handler

# GitHub repository info
GITHUB_API_URL  = "https://api.github.com/repos/{owner}/{repo}/commits"

def github_repository_validation() -> bool:
    
    """
    Validates the presence and correctness of essential GitHub-related environment variables.

    This function checks the `.env` file for the following:
    - The `GITHUB_TOKEN`, which is necessary for authentication.
    - The `OWNER`, which specifies the GitHub account owner.
    - The `GITHUB_API_URL`, which defines the GitHub API endpoint.

    If any of these variables are missing or invalid, it raises a `KeyError` with an appropriate message and logs the error using the `error_handler` module.

    Returns:
        bool: True if all validations pass, otherwise False.

    Exceptions:
        KeyError: Raised if any required environment variable is not set.
        Exception: Catches and handles any unexpected errors during validation.
    """

    try:
        
        if not settings_mapper.GITHUB_CONSTANTS["GITHUB_TOKEN"]:
            raise KeyError("GITHUB_TOKEN is not set. Please set the environment variable.")
        
        if not settings_mapper.GITHUB_CONSTANTS["OWNER"]:
            raise KeyError("GITHUB owner is not set. Please set the environmental variable.")
        
        if not GITHUB_API_URL:
            raise KeyError("Please specify a GitHub API URL to continue.")
               
    except AttributeError as e:
        error_handler.report_error("We do not have a GITHUB_CONSTANTS attribute.",f"{e}")
        return False
    
    except KeyError as e:
        error_handler.report_error("Github Repository Validation Failure", f"{e}")
        return False

    except Exception as e:
        error_handler.report_error("Github Repository Validation Failure", f"{e}")
        return False

    return True

# Function to get the latest commit hash from GitHub
def get_latest_commit(changed_local_repos:list) -> list:
    
    """
    Retrieves the latest commits from remote GitHub repositories via the GitHub API.

    This function performs the following steps:
    1. Validates essential GitHub environment variables using the `github_repository_validation` function,
    2. Initializes an empty `remote_repo_list` to store details about repositories and their latest commits.
    3. Constructs request headers using the GitHub token from the `.env` file.
    4. Fetches a list of remote repositories from the `repositories` module.
    5. Builds the GitHub API URL for each repository to retrieve commit data.
    6. Sends an email summarizing the changes in remote repositories to the user.

    For each remote repository:
    - Sends a GET request to the GitHub API to retrieve commit details.
    - Handles request exceptions gracefully, logging errors using `error_handler`.
    - If the response status is 200, extracts commit details such as SHA, author ID, date, and message.
    - Appends these commit details to the `remote_repo_list`.

    Args:
        changed_local_repos (list): List of locally changed repositories.

    Returns:

        list: A list containing details of remote GitHub repositories with the latest commits.

    Exceptions:

        - requests.exceptions.RequestException: Raised when a network request fails, and errors are logged.
        - Other exceptions are caught and logged using `error_handler`.

    Notes:
        - The function sends an email notification summarizing repository changes if `remote_repo_list` is populated.
    """
   
    
    if github_repository_validation():
                    
        remote_repo_list    = []
        headers             = {"Authorization": f"token {settings_mapper.GITHUB_CONSTANTS['GITHUB_TOKEN']}"}
        repos               = repositories.remote_repositories()

        for repo in repos:

            url = GITHUB_API_URL.format(owner = settings_mapper.GITHUB_CONSTANTS["OWNER"], repo=repo) 
            
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
    
    else:
        return[]