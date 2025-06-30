from run_command import run_command
import os
from error_handler import report_error
from create_git_ignore_file import add_gitignore_entries

def init_git_pull_command(cwd:str, remote_repo_name:str, github_username:str) -> str | None:
    """
    Clones a GitHub repository into the specified working directory and integrates .gitignore entries.
    Args:
        cwd (str): The current working directory where the repository will be cloned.
        remote_repo_name (str): The name of the remote GitHub repository to clone.
        github_username (str): The GitHub username owning the repository.
    Returns:
        str | None: The standard output from the git clone command if successful, or the error message if cloning fails. Returns None if an exception occurs.
    Raises:
        NotADirectoryError: If the specified working directory is invalid.
        FileNotFoundError: If a required file or directory does not exist.
        Exception: For any other unexpected errors.
    Side Effects:
        - Calls `report_error` to log or notify about errors.
        - Calls `add_gitignore_entries` to update .gitignore in the cloned repository.
        - Prints a success message upon successful integration.
    """

    try:
        
        git_repo_url = f"https://github.com/{github_username}/{remote_repo_name}.git"
        
        git_pull_result = run_command(["git", "clone","--quiet", git_repo_url,"."], cwd)

        if git_pull_result.returncode != 0:
            
            error_subject = "Error on pulling the repos from Git"
            error_message = f"{git_pull_result.stderr}"

            report_error(error_subject, error_message)
            
            return git_pull_result.stderr
        
        add_gitignore_entries(cwd)
        
        print(f"Repo {remote_repo_name} has been successully integrated!")
        
        return git_pull_result.stdout

    except NotADirectoryError as e:

        error_subject = "This is not a directory"
        error_message = f"You are attempting to pull into an invalid directory - {e}"

        report_error(error_subject, error_message)

        return None

    except FileNotFoundError as e:
        
        error_subject = "This is not a file"
        error_message = f"The file you are looking for does not exist = {e}"
        
        report_error(error_subject, error_message)

        return None

    except Exception as e:

        error_subject = "Exception Error"
        error_message = f"There was an unexpected error whilst attemptig to do a pull from the Hub of Git! - {e}"

        report_error(error_subject, error_message)

        return None