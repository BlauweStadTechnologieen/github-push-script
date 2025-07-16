import os
from run_command import run_command
from error_handler import report_error
import logging

def convert_to_ssh(github_username:str, github_remote_repo_name:str, cwd:str) -> str | None:

    try:
    
        clone_result = run_command(["git", "remote", "set-url", "origin", f"git@github.com:{github_username}/{github_remote_repo_name}.git"], cwd)

        if clone_result.returncode != 0:

            raise Exception(f"Error in converting from HTTPS to SSH. Please refer to error code {clone_result.returncode} {clone_result.stderr}")
        
        return clone_result.stdout
        
    except Exception as e:

        error_subject = "HTTPS Conversion Error"
        error_message = str(e)

        report_error(error_subject, error_message, logging_level=logging.ERROR)

        return None