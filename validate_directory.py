from error_handler import status_logger
import os
import logging

logger = logging.getLogger(__name__)

def is_existing_directory(cwd: str) -> bool:
    """
    Checks if the given directory exists.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """

    if os.path.exists(cwd) and os.path.isdir(cwd):
                
        status_logger("Directory Validation", f"The directory path: {cwd} is valid.")
        
        return True     
    
    status_logger("Directory Validation", f"The directory path: {cwd} is not valid.", logging_level=logging.ERROR)
    
    return False

def is_valid_directory(cwd:str) -> bool:
    """
    Checks and validates the full directory. The full directory is constructed from the parent directory, & appending each sub-directory which is attained by looping through all of the sub-directories listed in the `repositories` module.

    Args:
        cwd(str): Denotes the Current Working Directory.

    Returns:
        bool: True if the cwd is valid, else returns `False`.

    Raises:
        ValueError: A `ValueError` will be raised if the directory is not valid. If the exception handling block is executed, the `error_handler` module will catch and process the error. 
    """    
    
    try:
        
        if not os.path.exists(cwd):
            
            raise ValueError(f"The directory path: {cwd} is not valid, please check and try again")

    except ValueError as e:

        custom_subject = "Invalid Directory Path"
        custom_message = f"{type(e)} - {e}"
        
        status_logger(custom_subject, custom_message, logging_level=logging.ERROR)
        
        return False
        
    status_logger("Directory Validation", f"The directory path: {cwd} is valid.")
    
    return True