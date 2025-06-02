import requests
import repositories
import error_handler
import os

def get_latest_commit() -> list:
    
    """
    Fetches the latest commit information for each remote GitHub repository.

    This function:
    - Validates required GitHub environment variables.
    - Iterates through all remote repositories defined in the `repositories` module.
    - For each repository, queries the GitHub API for the latest commit.
    - Compares the latest commit SHA with the previously stored SHA (in 'latest_sha.txt').
    - If a new commit is found, appends its details (repo, sha, author_id, date, message) to the result list and updates the stored SHA.
    - Handles and logs errors using the `error_handler` module.

    Args:
        changed_local_repos (list): List of locally changed repositories (currently unused).

    Returns:
        list: A list of dictionaries, each containing details of the latest commit for repositories with new commits.
    """
                    
    required_env_vars = {

        "GITHUB_TOKEN"      : os.getenv("GITHUB_TOKEN"),
        "OWNER"             : os.getenv("OWNER"),
        "PARENT_DIRECTORY"  : os.getenv("PARENT_DIRECTORY"),
        "VERSION_FOLDER"    : os.getenv("VERSION_FOLDER")

    }

    missing_vars = [key for key, value in required_env_vars.items() if not value]

    if missing_vars:

        error_handler.report_error(

            "Environment Configuration Error",
            f"The following environment variables are missing: {', '.join(missing_vars)}. Please check your configuration.",
            True

        )

        return []

    github_auth_token   = required_env_vars["GITHUB_TOKEN"]
    github_company      = required_env_vars["OWNER"]
    directory_path      = required_env_vars["PARENT_DIRECTORY"]
    mql_version         = required_env_vars["VERSION_FOLDER"]

    remote_repo_list = []
        
    headers = {

            "User-Agent"    : "GitHub Commit Notifier",
            "Authorization" : f"Bearer {github_auth_token}"

        }

    base_directory = os.path.join(directory_path, mql_version)

    if not os.path.exists(base_directory):
        
        error_handler.report_error(

            "Directory Not Found",
            f"The specified directory '{base_directory}' does not exist. Please check your configuration.",
            True

        )

        return []
    
    latest_sha_file = "latest_sha.txt"

    for repo in repositories.remote_repositories():
        
        try:

            url = f"https://api.github.com/repos/{github_company}/{repo}/commits"
                        
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                
                sha = response.json()

                if not sha:
                    
                    custom_message = (

                        f"Message: No commits found for {repo}.\n"
                        f"API Response Message: {response.text}\n"
                        f"API Response Status Code: {response.status_code}"

                    )

                    custom_subject = f"No commits found - {response.status_code}"

                    error_handler.report_error(custom_subject, custom_message, True)

                    continue
                
                cwd = os.path.join(base_directory, repo)

                if not os.path.exists(cwd):
                    
                    error_handler.report_error(

                        "Directory Not Found",
                        f"The specified directory '{cwd}' does not exist for repository '{repo}'. Please check your configuration.",
                        True

                    )

                    return []

                latest_sha_directory = os.path.join(cwd, latest_sha_file)

                if os.path.exists(latest_sha_directory):

                    with open(latest_sha_directory, "r") as file:

                        stored_sha = file.read().strip()    

                else:

                    stored_sha = None

                latest_commit_sha = sha[0]["sha"]

                if latest_commit_sha != stored_sha:
                    
                    commit_author_id    = sha[0]["author"]["id"]
                    commit_date         = sha[0]["commit"]["committer"]["date"]
                    commit_message      = sha[0]["commit"]["message"]

                    remote_repo_list.append({

                        "repo": repo,
                        "sha": latest_commit_sha,
                        "author_id": commit_author_id,
                        "date": commit_date,
                        "message": commit_message

                    }) 
                        
                    with open(latest_sha_directory, "w") as file:

                        file.write(latest_commit_sha)
                    
                    #send_email.send_message()

                else:
                    
                    print(f"No new commit found in {repo}. Latest SHA: {latest_commit_sha}")
                
        except requests.exceptions.RequestException as e:
            
            error_handler.report_error("GitHub API Request Error", f"Error fetching commits for {repo}: {e}")
        
        except Exception as e:

            error_handler.report_error("Unexpected Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":

    get_latest_commit()