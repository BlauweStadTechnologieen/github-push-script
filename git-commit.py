import os
import subprocess
from pathlib import Path
from commit_notify import get_latest_commit
import settings_mapper
import repositories
import error_handler

#def assign_log_number(func) -> str:
#    @wraps(func)
#    def wrapper(*args, **kwargs):
#        assign_log_number = generate_incident_ref()
#        try:
#            return func(*args, **kwargs, assign_log_number = assign_log_number)
#        except Exception as e:
#            raise e
#    return wrapper

def run_command(command:str, cwd:str = None) -> str:
    """Run a command in the terminal and capture the output. An email will be sent in the event of an error, stating the nature of the error. No message will be printed if there are no errors."""
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    
    custom_message = None
    custom_subject = "Run Command Error"
    
    if result.returncode != 0:
        custom_message =  result.stderr.strip() if result.stderr else "Unknown error occured - check repo directory as a possible solution"
        error_handler.report_error(custom_subject, custom_message)
        return custom_message
    else:
        print(f"Command Output: {result.stdout}") 
        return result.stdout
    
def check_for_changes(cwd:str) -> bool:
    """Checks for both staged and unstaged changes in your local repo.
    """
    print("checking for changes....")
    
    custom_message = None
    custom_subject = "An error occured when checking for changes in a local directory"
    
    try:
        result = run_command(["git", "status", "--short"], cwd).strip()

        if result.strip():
            print(f"Tracked Files Git Status Output: {result}") 
            return True
        
        # If nothing was detected, check for untracked files.
        untracked_files = run_command(["git", "ls-files", "--others", "--exclude-standard"], cwd).strip()
        if untracked_files.strip():
            print(f"Untracked Files Git Status Output: {result}") 
            return True
        
        print("There were no changes to the working tree detected.")
        return False
    
    except TypeError as e:
        custom_message = f"{{type{e}}} {e}"
    
    except Exception as e:
        custom_message = f"{{type{e}}} {e}"

    if custom_message:
        return error_handler.report_error(custom_subject, custom_message)

def parent_directory_validation() -> bool:
    
    custom_subject = "Parent Directory Validation Error"
    
    try:

        parent_directory = settings_mapper.DIRECTORY_CONSTANTS["PARENT_DIRECTORY"]

        if not parent_directory:
            """Checks to ensure that a parent directory is specified"""
            raise KeyError("PARENT_DIRECTORY key is missing from the DIRECTORY_CONSTANTS variables environment.")
        
        if not os.path.isdir(parent_directory):
            """If a parent directory is specified, it will then check that this is valid."""
            raise ValueError(f"The specified parent directory in the PARENT_DIRECTORY key - {parent_directory} is invalid. Please verify the path and try again.")
            
    except KeyError as e:
        return error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")

    except ValueError as e:
        return error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
    
    except Exception as e:
        return error_handler.report_error(f"{type(e)} - {custom_subject}", f"{e}")
        
    return True

def is_valid_directory(cwd:str) -> bool:
        
    try:
        
        if not os.path.isdir(cwd):
            """Checks to ensure that the entire directory is valid.
            'cwd' represents the entire directory path: parnet + base + subdir"""
            raise ValueError(f"The resulting directory {cwd} is not valid, please check and try again")

    except ValueError as e:
        return error_handler.report_error("Directory Validation Incident", f"{e}")
        
    return True

def is_git_repo(cwd:str) -> bool:
    
    git_path        =   os.path.join(cwd, '.git')
    custom_subject  =   "Invalid Git Repo in the local directory"
    
    if os.path.isdir(git_path):
        return True
    else:
        custom_message = f"{cwd} is not a Git Repository. Navigate do {cwd}, then run 'git init' from the command shell "
        return error_handler.report_error(custom_subject, custom_message)
    
def push_to_github() -> None:
    """Adds, commits and pushes all files to the Git repo.
    Each 'run_command' will be individually checked, 
    and will log an incident when any return an error."""
    
    parent_dir          = settings_mapper.DIRECTORY_CONSTANTS["PARENT_DIRECTORY"]
    directory_structure = repositories.local_repository_structure()

    changed_dirs = []

    if parent_directory_validation():
    
        for base, sub_dirs in directory_structure.items():
            
            for sub_dir in sub_dirs:
                
                cwd = os.path.join(parent_dir, base, sub_dir)
                        
                if not is_valid_directory(cwd):
                    continue

                """if not is_git_repo(cwd):
                    continue
                                                    
                if not check_for_changes(cwd):
                    continue

                changed_dirs.append(cwd)
                
                run_command(["git", "add", "."], cwd)

                commit_message = f"<b>New Commit: {sub_dir.capitalize()}</b>"

                commit_result = run_command(["git", "commit", "-m", commit_message], cwd)

                if "nothing to commit, working tree clean" in commit_result:
                    continue
                
                run_command(["git", "push"], cwd)

    if changed_dirs:
        get_latest_commit(changed_dirs)  """
        
if __name__ == "__main__":
    push_to_github()