import os
import error_handler

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

        if not os.path.exists(gitignore_path):

            with open(gitignore_path, "w") as write:

                write.write("*\n")
                write.write("!*.mq5\n")
                write.write("!*.ex5\n")
                write.write("!*.mqh\n")
                write.write("!*.py\n")
 
                print(".gitignore file successfully added!")

                return gitignore_path

        else:

            print(".gitignore file exists already.")

            return None
        
    except Exception as e:
        
        error_handler.report_error("Unexpected error on writing .gitignore file", f"{e}")