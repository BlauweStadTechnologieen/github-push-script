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
    
def dot_env_variables_none() -> bool:
    """
    Check if any of the variables in the list are None.
    """

    load_dotenv()

    try:
        
        git_user_name       = os.getenv("GITHUB_USERNAME")
        github_token        = os.getenv("GITHUB_TOKEN")
        parent_directory    = os.getenv("PARENT_DIRECTORY")
        version_folder      = os.getenv("VERSION_FOLDER")
        package_name        = os.getenv("PACKAGE_NAME")
        sender_email        = os.getenv("SENDER_EMAIL")
        sender_domain       = os.getenv("SENDER_DOMAIN")
        sender_name         = os.getenv("SENDER_NAME")
        sender_department   = os.getenv("SENDER_DEPARTMENT")
        requester_name      = os.getenv("REQUESTER_NAME")
        requester_email     = os.getenv("REQUESTER_EMAIL")
        smtp_server         = os.getenv("SMTP_SERVER")
        smtp_port           = os.getenv("SMTP_PORT")
        smtp_email          = os.getenv("SMTP_EMAIL")
        smtp_password       = os.getenv("SMTP_PASSWORD")
        fd_domain           = os.getenv("FRESHDESK_DOMAIN")
        fd_api_key          = os.getenv("FRESHDESK_API_KEY")

        dot_env_credentials = [
            git_user_name,
            github_token,
            parent_directory,
            version_folder,
            package_name,
            sender_email,
            sender_domain,
            sender_name,
            sender_department,
            requester_name,
            requester_email,
            smtp_server,
            smtp_port,
            smtp_email,
            smtp_password,
            fd_domain,
            fd_api_key
        ]

        if any(is_value_none(cred) for cred in dot_env_credentials):
            
            raise ValueError("One or more of your .env variables are missing. Please check these details.")
        
        return True
    
    except ValueError as ve:

        error_handler.report_error("Value Error", str(ve))

        return False
        
def instance_validation(variable, instance):

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