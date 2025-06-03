import os
import subprocess
from commit_notify import get_latest_commit
import settings_mapper
import repositories
import error_handler
import requests
from typing import Optional

def run_command(command:str, cwd:str) -> str:
    """Runs specified commands in the local machine's terminal. The process of this is as follows:
    - It will check for the existence of the directory. 
    - If no exceptions occur, it will run the specified commands using the `subprocess` module.
    Args:
        command(str): Defines a list of git commands to run in the command window.
        cwd(str): Denotes the current working directory where the git commands are to be commanded
    Returns:
        custom_message(str): Returns a `custom_message` if there is an error, else it returns `result.stdout`.
    Exceptions:
        FileNotFoundError: If the directory is not valid, this will throw a FileNotFoundError exception.
        Exception: An excepion is raised is any other error occours.
    Notes:
    -
        If there is an error or Exception, the `error_handler` function will create a support ticket. 
    """
    
    try:

        if not os.path.isdir(cwd):
            raise FileNotFoundError(f"The directory '{cwd}' does not exist.")
        os.chdir(cwd)

    except FileNotFoundError as e:
        error_handler.report_error("Directory Error", str(e))
        return str(e)

    except Exception as e:
        error_handler.report_error("Runn Command Exception", str(e))
        return str(e)
    
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    
    custom_message = None
    custom_subject = "Run Command Error"
    
    if result.returncode != 0:
        custom_message =  result.stderr.strip() if result.stderr else "Unknown error occured - check repo directory as a possible solution"
        error_handler.report_error(custom_subject, custom_message)
        return custom_message

    return result.stdout.strip()
    
def check_for_changes(cwd:str, package:str) -> Optional[str]:
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
      
    try:

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

            return None

        github_auth_token   = required_env_vars["GITHUB_TOKEN"]
        github_company      = required_env_vars["OWNER"]

        commit_api_url = f"https://api.github.com/repos/{github_company}/{package}/commits"

        remote_repo_attrs = None

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
                
                error_handler.report_error(custom_subject, custom_message, True)
                
                return None
            
            latest_sha_file = "latest_sha.txt"
            sha_dir         = os.path.join(cwd, latest_sha_file)

            if not os.path.exists(sha_dir):

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

            error_handler.report_error(custom_subject, custom_message, True)

            return None
                
    except FileNotFoundError as e:
        
        custom_subject = "Directory Not Found Error"
        custom_message = f"Please check your configuration: {e}"
        error_handler.report_error(custom_subject, custom_message, True)

        return None
    
    except requests.exceptions.RequestException as e:

        custom_subject = "GitHub API Request Error"
        custom_message = f"An error occurred while making a request to the GitHub API: {e}"
        error_handler.report_error(custom_subject, custom_message, True)

        return None
    
    except Exception as e:
        
        custom_subject = "An error occured when checking for changes in a local directory"
        custom_message = f"{{type{e}}} {e}"
        error_handler.report_error(custom_subject, custom_message, True)

        return None
        
def parent_directory_validation() -> str:
    
    """
    Checks and validates the parent directory specified in the `.env` file.

    Returns:
        parent_directory(str): Returns the parent directory as a string format, else it will return `None` if the parent directory is either missing or invalud.

    Raises:
        KeyError: A `KeyError` is raised if a parent directory as hot been specified.
        ValyeError: A `ValueError` is raised of the parent directory is invalid.

    """
    custom_subject = "Parent Directory Validation Error"
    
    try:

        parent_directory = settings_mapper.DIRECTORY_CONSTANTS["PARENT_DIRECTORY"]

        if not parent_directory:
            # Checks to ensure that a parent directory is specified
            raise KeyError("PARENT_DIRECTORY key is missing from the DIRECTORY_CONSTANTS variables environment.")
        
        if not os.path.isdir(parent_directory):
            # If a parent directory is specified, it will then check to ensure this is valid.
            raise ValueError(f"The specified parent directory in the PARENT_DIRECTORY key - {parent_directory} is invalid. Please verify the path and try again.")
            
    except AttributeError as e:
        error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
        return None
    
    except KeyError as e:
        error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
        return None

    except ValueError as e:
        error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
        return None
    
    except Exception as e:
        error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
        return None
        
    return parent_directory

def is_valid_directory(cwd:str) -> bool:
    """
    Checks and validates the full directory. The full directory is constructed from the parent directory, & appending each sub-directory which is attained by looping through all of the sub-directories listed in the `repositories` module.

    Args:
        cwd(str): Denotes the Current Working Directory.

    Returns:
        bool: True of the cwd is valid, ensure returns `False`.

    Raises:
        ValueError: A `ValueError` will be raised if the directory is not valid. If the exception handing block is exected, the `error_hander` module will catch and processes the error. 
    """    
    
    try:
        
        if not os.path.isdir(cwd):
            raise ValueError(f"The resulting directory {cwd} is not valid, please check and try again")

    except ValueError as e:

        ticket_subject = "The specified directory is not valid"
        ticket_description = f"{type(e)} - {e}"
        
        error_handler.report_error(ticket_subject, ticket_description)
        return False
    
    return True

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
    custom_subject  = "You have not initialised a Git Repository"
    
    if os.path.isdir(git_path):
        return True
    else:
        custom_message = f"{cwd} is not an initialized Git repository. Navigate to {cwd}, then run 'git init' from the command shell."
        error_handler.report_error(custom_subject, custom_message)
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
    
    parent_dir          = parent_directory_validation()
    directory_structure = repositories.local_repository_structure()
    changed_dirs        = []

    if parent_dir is None:
                
        return None
    
    for base, sub_dirs in directory_structure.items():
        
        for sub_dir in sub_dirs:
            
            cwd = os.path.join(parent_dir, base, sub_dir)

            if not os.path.exists(cwd):

                custom_subject = "Directory Not Found Error"
                custom_message = f"The directory {cwd} does not exist. Please check your configuration."
                error_handler.report_error(custom_subject, custom_message, True)

                continue
                    
            if not is_valid_directory(cwd):
                continue

            if not is_git_repo(cwd):
                continue
                                            
            tracked_files   = run_command(["git", "status", "--short"], cwd).strip()
            untracked_files = run_command(["git", "ls-files", "--others", "--exclude-standard"], cwd).strip()

            if not (untracked_files.strip() or tracked_files.strip()):

                continue
            
            run_command(["git", "add", "."], cwd)

            commit_message = f"<b>New Commit: {sub_dir.capitalize()}</b>"

            commit_result = run_command(["git", "commit", "-m", commit_message], cwd)

            if "nothing to commit, working tree clean" in commit_result:
                
                continue
            
            run_command(["git", "push"], cwd)

            changed_package = check_for_changes(cwd, sub_dir)

            if not changed_package:
                
                continue

            changed_dirs.append(changed_package.title())

    if changed_dirs:
        get_latest_commit(changed_dirs) 
            
    return None
        
if __name__ == "__main__":
    push_to_github()