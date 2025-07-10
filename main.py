import os
import repositories
from error_handler import report_error
import requests
import logging
from send_email import send_message
from dotenv import load_dotenv
from run_command import run_command
from git_pull import init_git_pull_command
from validate_directory import is_valid_directory, is_existing_directory, make_directory
from instance_validation import instance_validation, all_env_vars_exist, is_instance_applicable

def check_for_changes(cwd:str, package:str) -> list | None:
    """
    Checks for any differences between the local and the remote repositories. 

    Args:
        cwd(str): Denoted the current working directory.
    Returns:
        bool: True if there is a mismatch between the remote and the local repositories, else it returns False.

    Raises:
        Exceptions: Catches any error if one or more are detected. Should any exception be called, the `error_handler` function will process a support ticket, which will be sent to the FreshDesk system.
    """
    print("checking for changes....")
    load_dotenv()
    try:

        github_auth_token   = os.getenv("GITHUB_TOKEN")
        github_company      = os.getenv("GITHUB_USERNAME")

        commit_api_url = f"https://api.github.com/repos/{github_company}/{package}/commits"

        remote_repo_attrs = []

        headers = {

            "User-Agent"    : "GitHub Commit Notifier",
            "Authorization" : f"Bearer {github_auth_token}"

        }
                
        response = requests.get(commit_api_url, headers=headers)

        if response.status_code == 200:

            sha = response.json()

            if not sha:

                custom_message = (

                    f"Message: No commits found for {package}.\n"
                    f"API Response Message: {response.text}\n"
                    f"API Response Status Code: {response.status_code}"

                )

                custom_subject = f"No commits found - {response.status_code}"
                
                report_error(custom_subject, custom_message, logging_level=logging.WARNING)
                
                return None
            
            latest_sha_file = "latest_sha.txt"
            sha_dir         = os.path.join(cwd, latest_sha_file)

            if is_existing_directory(sha_dir):

                with open(sha_dir, "r") as file:

                    stored_sha = file.read().strip()

            else:

                stored_sha = None

            latest_commit_sha = sha[0]["sha"]
            
            if stored_sha != latest_commit_sha:

                commit_author_id    = sha[0]["author"]["id"]
                commit_date         = sha[0]["commit"]["committer"]["date"]
                commit_message      = sha[0]["commit"]["message"]

                remote_repo_attrs.append({

                    "repo"      : package.title(),
                    "sha"       : latest_commit_sha,
                    "author_id" : commit_author_id,
                    "date"      : commit_date,
                    "message"   : commit_message

                })

                with open(sha_dir, "w") as file:

                    file.write(latest_commit_sha)

                return remote_repo_attrs

            else:
 
                print(f"No changes detected for {package}.")
                
                return None
            
        else:

            custom_message = (
                
                f"Message: Failed to retrieve commits for {package}.\n"
                f"API Response Message: {response.text}\n"
                f"API Response Status Code: {response.status_code}"

            )
            custom_subject = f"Failed to retrieve commits - {response.status_code}"

            report_error(custom_subject, custom_message, logging_level=logging.CRITICAL)

            return None
                
    except FileNotFoundError as e:
        
        custom_subject = "Directory Not Found Error"
        custom_message = f"Please check your configuration: {e}"
        report_error(custom_subject, custom_message, logging_level=logging.CRITICAL)

        return None
    
    except requests.exceptions.RequestException as e:

        custom_subject = "GitHub API Request Error"
        custom_message = f"An error occurred while making a request to the GitHub API: {e}"
        report_error(custom_subject, custom_message, logging_level=logging.CRITICAL)

        return None
    
    except Exception as e:
        
        custom_subject = "An error occured when checking for changes in a local directory"
        custom_message = f"{{type{e}}} {e}"
        report_error(custom_subject, custom_message, logging_level=logging.CRITICAL)

        return None
        
def is_git_repo(cwd:str) -> bool:
    
    """Once the current working directory is confirmed as valid, it will then check to ensure that the specified directory is a valid git repository.
    This is achieved by checking for the presece of a `.git` folder. 
    
    Args:
        cwd(str): Denoted the full directory.

    Returns:
        bool: Returns `True` if the `cwd` contains a `.git` folder. Else it returns `False` if ano `.git` folder is present.

    Notes:
    -
        Please be aware that this does *NOT* check to ensure that the directory is pointing to the correct remote repository.
    
    """
    git_path        = os.path.join(cwd, '.git')
    
    if is_existing_directory(git_path):
                        
        return True
        
    return False
    
def run_me_them_commands(cwd:str, package_name:str) -> bool:
    """
    Executes a sequence of Git commands to add, commit, and push changes in the specified working directory.
    This function checks for any tracked or untracked file changes in the given directory. If changes are detected,
    it stages all changes, commits them with a default message, and pushes the commit to the remote repository.
    If there are no changes to commit, or if an error occurs, the function returns False.
    
    Args:
        cwd (str): The path to the working directory where Git commands will be executed.
    
    Returns:
        bool: True if changes were committed and pushed successfully, False otherwise.
    Exceptions:
        Any exceptions encountered during execution are reported via the error_handler and result in a return value of False.
    """
    
    try:
       
        git_status_porcelain =  run_command(["git", "status", "--porcelain"], cwd)
        
        if not git_status_porcelain.stdout.strip():
        
            print(f"The working tree for {package_name} is clean.")

            return False
        
        run_command(["git", "add", "."], cwd)
        
        from commit_message import commit_message_validation

        commit_message = commit_message_validation(package_name)
        
        run_command(["git", "commit", "-m", commit_message], cwd)

        run_command(["git", "push"], cwd)

        print("Changes committed to remote repository!")

        return True
    
    except Exception as e:
        
        report_error("Unexpected Error", str(e), logging_level=logging.CRITICAL)

        return False

def push_to_github() -> None:
    """Pushes all files and folders to the remote GitHib repository.

    - First, it checks to ensure that the parent directory is valid. This will return `NONE` if an error or exception occurs.
    - Second, it will access each directory in the list of directories specified in the `local_repository_structure()` method, located in the `repositories` module.
    - On each iteration through the loop, it will check the following:
        - the validity of the current working directory,
        - that the current working directory is a git repository,
        - checks for any changes made in the local repository since the previous pull from the remote repository,
        - append any changes to a list of updated local repositories.
    - Third, it will run the `git add .`, `git commit` and `git push` commands, if changes were detected.
    
    """

    if not all_env_vars_exist():

        return None
    
    github_username     = os.getenv("GITHUB_USERNAME")
    github_token        = os.getenv("GITHUB_TOKEN")
    package             = os.getenv("PACKAGE_NAME")
    changed_dirs        = []

    git_link_validation = repositories.git_communication_validation(github_username, github_token)
    
    if not instance_validation(git_link_validation, dict):

        return None
            
    for directory, remote_repo in git_link_validation.items():
        
        cwd = os.path.join(directory, package)

        if not is_existing_directory(cwd):
            
            if not instance_validation(make_directory(cwd,""), str):

                break

        if not is_git_repo(cwd):
                        
            if not instance_validation(init_git_pull_command(cwd, remote_repo, github_username), str):
            
                break
            
            continue
                
        if not run_me_them_commands(cwd, remote_repo):
            
            continue

        changed_package = check_for_changes(cwd, remote_repo)

        if not is_instance_applicable(changed_package, list):
            
            continue

        changed_dirs.extend(changed_package)

    if changed_dirs:
        
        send_message(changed_dirs)
            
    return None
        
if __name__ == "__main__":

    push_to_github()