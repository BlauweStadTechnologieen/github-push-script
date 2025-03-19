import os
import subprocess
from pathlib import Path
from commit_notify import get_latest_commit
from freshdesk_ticket import create_freshdesk_ticket
import settings_mapper
import repositories
from check_and_install_requirements_changes import check_and_install_requirements

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
        create_freshdesk_ticket(custom_message, custom_subject)
        return custom_message
    else:
        print(f"Command Output: {result.stdout}") 
        return result.stdout
    
def check_for_changes(cwd:str) -> bool:
    """Checks for both staged and unstaged changes in your local repo.
    """
    print("checking for changes....")

    check_and_install_requirements()
    
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
        custom_message = f"TypeError Exception {e}"
    
    except Exception as e:
        custom_message = f"General Exception {e}"

    if custom_message:
        print(custom_message)
        create_freshdesk_ticket(custom_message, custom_subject)

    return False

def is_valid_directory(cwd:str) -> bool:
    
    custom_subject = "Invalid local directory"
    
    if not os.path.isdir(cwd):
        custom_message = f"{cwd} is not a valid directory. Please check you have specified an existing directory & that this contains a .git folder."
        print(custom_subject, custom_message)
        create_freshdesk_ticket(custom_message,custom_subject)
        return False

    if is_git_repo(cwd):
        return True
    
    False

def is_git_repo(cwd) -> bool:
    
    git_path        =   os.path.join(cwd, '.git')
    custom_subject  =   "Invalid Git Repo in the local directory"
    
    if os.path.isdir(git_path):
        return True
    else:
        custom_message = f"{cwd} is not a Git Repository. Navigate do {cwd}, then run 'git init' from the command shell "
        print(custom_message, custom_subject)
        create_freshdesk_ticket(custom_message, custom_subject)
        return False
    
def push_to_github() -> None:
    """Adds, commits and pushes all files to the Git repo.
    Each 'run_command' will be individually checked, 
    and will log an incident when any return an error."""
    
    base_dir = settings_mapper.DIRECTORY_CONSTANTS["BASE_DIR"]
    sub_dirs = repositories.local_repositories()

    changed_dirs = []
    
    for sub_dir in sub_dirs:
        
        cwd = str(Path(base_dir) / sub_dir)
        
        if not is_valid_directory(cwd):
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
        get_latest_commit(changed_dirs)  
        
if __name__ == "__main__":
    push_to_github()