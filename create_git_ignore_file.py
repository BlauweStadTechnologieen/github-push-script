import os
import error_handler
from validate_directory import is_existing_directory
from settings import repositories_to_bypass_commit_messages
from message import success_logging

def add_gitignore_entries(cwd:str, remote_repo_name:str, name: str = ".gitignore") -> str | None:
    """
    Creates a .gitignore file with default entries if it does not already exist in the specified directory.
    Parameters:
        cwd (str): The directory in which to create or check for the .gitignore file.
        name (str, optional): The name of the gitignore file. Defaults to ".gitignore".
    Returns:
        str | None: The path to the newly created .gitignore file if it was created, otherwise None.
    Raises:
        Reports any unexpected exceptions using the error_handler.
    """

    try:
    
        gitignore_path = os.path.join(cwd, name)

        if not is_existing_directory(gitignore_path):

            if remote_repo_name in repositories_to_bypass_commit_messages():
                
                with open(gitignore_path, "w") as write:

                    write.write("*\n")
                    write.write("!*.png\n")
    
                    success_logging("Gitignore Created", f".gitignore file created in {cwd} for repository {remote_repo_name}.")

                    return gitignore_path
            
            else:
            
                with open(gitignore_path, "w") as write:

                    write.write("*\n")
                    write.write("!*.mq5\n")
                    write.write("!*.ex5\n")
                    write.write("!*.mqh\n")
                    write.write("!*.py\n")
    
                    success_logging("Gitignore Created", f".gitignore file created in {cwd} for repository {remote_repo_name}.")

                    return gitignore_path

        else:

            success_logging("Gitignore Exists", f".gitignore file already exists in {cwd}, no action taken.")

            return None
        
    except Exception as e:
        
        error_handler.report_error("Unexpected error on writing .gitignore file", f"{e}")