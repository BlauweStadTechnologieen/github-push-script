import os
import error_handler
from validate_directory import is_existing_directory
from settings import repositories_to_bypass_commit_messages
import logging

logging = logging.getLogger(__name__)

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

                    status_message = f"Created .gitignore file for {remote_repo_name} with entries to ignore all files except .png files."
                    error_handler.status_logger("Gitignore File Created", status_message)
    
                    return gitignore_path
            
            else:
            
                with open(gitignore_path, "w") as write:

                    write.write("*\n")
                    write.write("!*.mq5\n")
                    write.write("!*.ex5\n")
                    write.write("!*.mqh\n")
                    write.write("!*.py\n")

                    status_message = f"Created .gitignore file for {remote_repo_name} with entries to ignore all files except .mq5, .ex5, .mqh, and .py files."
                    error_handler.status_logger("Gitignore File Created", status_message)
    
                    return gitignore_path

        else:

            error_handler.status_logger("Gitignore File Already Exists", f"A .gitignore file already exists in {cwd}. No new file was created.")
            
            return None
        
    except Exception as e:
        
        error_handler.status_logger("Unexpected error on writing .gitignore file", f"{e}", logging_level=logging.ERROR)