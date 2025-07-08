import os
import error_handler
from validate_directory import is_existing_directory
import logging

def add_gitignore_entries(cwd:str, name: str = ".gitignore") -> str | None:
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

            with open(gitignore_path, "w") as write:

                write.write("*\n")
                write.write("!*.mq5\n")
                write.write("!*.ex5\n")
                write.write("!*.mqh\n")
                write.write("!*.py\n")
 
                error_handler.report_error("Gitignore File Successfully Created", f".gitignore file created at {gitignore_path}", logging_level=logging.INFO)

                return gitignore_path

        else:

            return None
        
    except Exception as e:
        
        error_handler.report_error("Unexpected error on writing .gitignore file", f"{e}", logging_level=logging.WARNING)