from run_command import run_command
import os
from error_handler import report_error

def init_git_pull_command(cwd:str, remote_repo_name:str, github_username:str) -> str | None:

    try:
        
        print(github_username)
        print(cwd)
        print(remote_repo_name)

        if not github_username:

            raise KeyError("You have not specified a GitHub owner, please check these credentials and try again")
        
        git_repo_url = f"https://github.com/{github_username}/{remote_repo_name}.git"

        print(git_repo_url)
        
        git_pull_result = run_command(["git", "clone","--quiet", git_repo_url,"."], cwd)

        print(git_pull_result)

        if git_pull_result.returncode != 0:
            
            error_subject = "Error on pulling the repos from Git"
            error_message = f"{git_pull_result.stderr}"

            report_error(error_subject, error_message)
            
            return git_pull_result.stderr
        
        print("Repo successully pulled!")
        
        return git_pull_result.stdout

    except KeyError as e:

        error_subject = "Github Owner was not specified"
        error_message = f"You have not secified a valid GitHub owner - {e}"

        report_error(error_subject, error_message)

        return None

    except NotADirectoryError as e:

        error_subject = "This is not a directory"
        error_message = f"You are attempting to pll into an invalid directory - {e}"

        report_error(error_subject, error_message)

        return None

    except FileNotFoundError as e:
        
        error_subject = ""
        error_message = ""
        
        report_error("Directory Not Found",f"Working directory '{cwd}' does not exist. Detail: {e}")

        return None

    except Exception as e:

        error_subject = "Exception Error"
        error_message = f"There was an unexpected error whilst attemptig to do a pull from the Hub of Git! - {e}"

        report_error(error_subject, error_message)

        return None