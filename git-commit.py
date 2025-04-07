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
    """
    Checks for any differences between the local and the remote repos. 

    Args:
        cwd(str): Denoted the current working directory.
    Returns:
        bool: True if there is a mismatch between the remoted and the local repo, else it returns False.

    Raises:
        Exceptions: Catches any error if any issues are detected. The the exception block is called, the `error_handler` function is called, and processed.
    """
    print("checking for changes....")
    
    custom_message = None
    custom_subject = "An error occured when checking for changes in a local directory"
    
    try:
        
        os.chdir(cwd)
        
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
    
    except Exception as e:
        custom_message = f"{{type{e}}} {e}"

    if custom_message:
        error_handler.report_error(custom_subject, custom_message)
        return False

def parent_directory_validation() -> str:
    
    """
    Checkes to ensure that the specified parent directory has bother been specified and that it is valid, this is retrieved from the `.env` constant.

    Returns:
        parent_directory(str): Returns the parent directory as a string format, else it will return `None` if the parent directory is either missing or invalud.

    Raises:
        KeyError: A `KeyError` is raised if no parent directory has been specigied.
        ValyeError: A `ValueError` is raised of the parent directory is invalid.

    """
    
    
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
    Check to ensure that the specified directory is valid

    Args:
        cwd(str): Denotes the Current Working Directory.

    Returns:
        bool: True of the cwd is valid, ensure returns `False`.

    Raises:
        ValueError: A `ValueError` will be raised if the directory is not valid. If the exception handing block is exected, the `error_hander` module will catch and processes the error. 
    """    
    
    
    try:
        
        if not os.path.isdir(cwd):
            """Checks to ensure that the entire directory is valid.
            'cwd' represents the entire directory path: parnet + base + subdir"""
            raise ValueError(f"The resulting directory {cwd} is not valid, please check and try again")

    except ValueError as e:
        error_handler.report_error("Directory Validation Incident", f"{e}")
        return False
        
    return True

def is_git_repo(cwd:str) -> bool:
    
    """Checks to ensure that the specified directory is a valid git repositiry by checking for the presece of a `.git` folder. 
    
    Args:
        cwd(str): Denoted the full directory.

    Returns:
        bool: Returns `True` if the `cwd` contains a `.git` folder. Else it returns `False` if ano `.git` folder is present.

    Notes:
    -
        Please be aware that this directory *NOT* check to ensure that this, if true, it is pointing to the corrector remote repo. This simple checks to ensure that a `.git` folder is present. 
    
    """
    
    git_path        =   os.path.join(cwd, '.git')
    custom_subject  =   "Invalid Git Repository"
    
    if os.path.isdir(git_path):
        return True
    else:
        custom_message = f"{cwd} is not a Git Repository. Navigate do {cwd}, then run 'git init' from the command shell "
        error_handler.report_error(custom_subject, custom_message)
        return False
    
def push_to_github() -> None:
    """Adds, commits and pucshed the comntect of each directory to the remote repo.

    - First, it checks to ensure that the parent directory is valid. This will return `NONE` if the if an exception is raised.
    - Second, it will access each directory in the list of dorectories specified in the `local_repository_structure()` method, located in the `repositore` module.
    - On each iteration throgun the loop, it will check the following:
        - the validitiry of the working directory
        - that the working directory is a valid local repostiry
        - checks for any changed between the local and the remote repo's
        - any changes, it will `.append()` them to a list, in preparation to send to email.
    - Third, it will run the `git add .`, `git commit` and `git push` if changes were detected.

    If there are any items in the `changed_dirs` list, these will be send, via email, to the user.  
    
    """
    
    parent_dir          = parent_directory_validation()
    directory_structure = repositories.local_repository_structure()
    changed_dirs        = []

    if parent_dir is None:
                
        return None
    
    for base, sub_dirs in directory_structure.items():
        
        for sub_dir in sub_dirs:
            
            cwd = os.path.join(parent_dir, base, sub_dir)
                    
            if not is_valid_directory(cwd):
                continue

            if not is_git_repo(cwd):
                continue
                                                
            """if not check_for_changes(cwd):
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
            
    return
        
if __name__ == "__main__":
    push_to_github()