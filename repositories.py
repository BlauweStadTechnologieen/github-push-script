from error_handler import report_error
import os
from dotenv import load_dotenv

def git_communication_validation(master_directory:str, git_username:str, git_token:str) -> dict | None:

    import requests
    from pathlib import Path

    load_dotenv()

    version_folder  = os.getenv("VERSION_FOLDER")

    paths = {
        Path(f"{version_folder}/Experts/Advisors") : "MQL5Experts",
        Path(f"{version_folder}/Include/Expert") : "MQL5Include",
        Path(f"{version_folder}/Scripts") : "MQL5Scripts",
        Path(f"{version_folder}/Files") : "Screenshots"
    }

    for directory in paths.keys():

        existing_directory = os.path.join(master_directory, directory)
        
        if not os.path.exists(existing_directory):

            report_error("Path does not exist","Upon checking the paths, the path does not exist")

            return None
        
    if git_username is None or git_token is None:

        return None

    for remote_repo in paths.values():

        url         = f"https://api.github.com/repos/{git_username}/{remote_repo}"
        headers     = {"Authorization": f"token {git_token}"} 
        response    = requests.get(url, headers=headers)

        if response.status_code != 200:

            report_error("Github Repository Valid Failed",f"Unfortunately, the remote repository validation failed with an error code of {response.status_code}")

            return None

    return paths