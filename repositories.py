from error_handler import report_error
import os
from dotenv import load_dotenv
from validate_directory import is_valid_directory, parent_directory_validation
from pathlib import Path
import requests
import logging

def git_communication_validation(git_username:str, git_token:str) -> dict | None:
    """
    Validates the existence of required local directories and checks access to corresponding GitHub repositories.

    Ensures that specific subdirectories exist within the parent directory and verifies that the provided
    GitHub username and token have access to the associated remote repositories.

    Args:
        git_username (str): GitHub username for repository validation.
        git_token (str): GitHub personal access token for authentication.

    Returns:
        dict | None: Dictionary mapping local Path objects to remote repository names if all validations succeed; otherwise, None.
    """

    load_dotenv()

    parent_directory = parent_directory_validation()

    if parent_directory is None:

        return None

    parent_directory = Path(parent_directory)

    paths = {

        parent_directory / "Experts" / "Advisors"   : "MQL5Experts",
        parent_directory / "Include" / "Expert"     : "MQL5Include",
        parent_directory / "Scripts"                : "MQL5Scripts",
        parent_directory / "Files"                  : "Screenshots"

    }

    for directory in paths.keys():
        
        if not is_valid_directory(directory):

            return None
        
        report_error("Git Repository Validation Success", f"{directory} is a valid path.", logging_level=logging.INFO)
        
    for remote_repo in paths.values():

        url         = f"https://api.github.com/repos/{git_username}/{remote_repo}"
        headers     = {"Authorization": f"token {git_token}"} 
        response    = requests.get(url, headers=headers)

        if response.status_code != 200:

            report_error("Github Repository Valid Failed",f"Unfortunately, the remote repository validation failed with an error code of {response.status_code}")

            return None

    return paths