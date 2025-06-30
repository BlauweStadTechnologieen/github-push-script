from error_handler import report_error
import os

def is_existing_directory(cwd: str) -> bool:
    """
    Checks if the given directory exists.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """

    if os.path.exists(cwd) and os.path.isdir(cwd):
        
        return True     
    
    return False

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
        
        if not os.path.exists(cwd):
            
            raise ValueError(f"The directory path: {cwd} is not valid, please check and try again")

    except ValueError as e:

        custom_subject = "Invalid Directory Path"
        custom_message = f"{type(e)} - {e}"
        
        report_error(custom_subject, custom_message)
        
        return False
    
    return True