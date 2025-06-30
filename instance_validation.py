import error_handler
from dotenv import load_dotenv
import os

def is_value_none(variable) -> bool:
    """
    Check if the variable is None.
    """
    try:

        if variable is None:
            
            raise ValueError("Variable cannot be None")
        
        return False
        
    except ValueError as ve:
        
        error_handler.report_error("Value Error", str(ve))
        
        return True
    
def all_env_vars_exist() -> bool:
    """
    Check if all required environment variables are set.
    """
    load_dotenv()

    required_vars = [
        "GITHUB_USERNAME",
        "GITHUB_TOKEN",
        "PARENT_DIRECTORY",
        "VERSION_FOLDER",
        "PACKAGE_NAME",
        "SENDER_EMAIL",
        "SENDER_DOMAIN",
        "SENDER_NAME",
        "SENDER_DEPARTMENT",
        "REQUESTER_NAME",
        "REQUESTER_EMAIL",
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_EMAIL",
        "SMTP_PASSWORD",
        "FRESHDESK_DOMAIN",
        "FRESHDESK_API_KEY"
    ]

    missing_vars = [var for var in required_vars if os.getenv(var) is None]

    if missing_vars:
        error_handler.report_error("Missing Environment Variables", f"The following variables are missing: {', '.join(missing_vars)}")
        return False

    return True
        
def instance_validation(variable, instance):
    """
    Validates whether a given variable is an instance of the specified type.
    Args:
        variable: The variable to check.
        instance: The type or class to check against.
    Returns:
        bool: True if variable is an instance of instance, otherwise handles the error.
    Raises:
        TypeError: If variable is not an instance of instance.
        ValueError: If a value error occurs during validation.
        Exception: For any other unexpected errors.
    Note:
        Errors are reported using the error_handler's report_error method.
    """

    try:
        
        if not isinstance(variable, instance):

            raise TypeError(f"Expected {instance.__name__}, got {type(variable).__name__}")  
           
        return True
    
    except ValueError as ve:
        error_handler.report_error("Value Error", str(ve))    

    except TypeError as te:
        error_handler.report_error("Type Error", str(te))
    
    except Exception as e:
        error_handler.report_error("Unexpected Error", str(e))