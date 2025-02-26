import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import uuid
import requests as r
import json as j
from pathlib import Path
import time
from commit_notify import monitor_commits, get_latest_commit

SMTP_SERVER     = "smtp-relay.brevo.com"
SMTP_PORT       = 587
SMTP_USER       = "448c41002@smtp-brevo.com"
SMTP_PASSWORD   = "hSg19RUfw6QIcV7b"

receiver_name   = "Synergex Systems"
sender_name     =  "Blue City Capital Technologies Inc"

sender_email    = "notifications@bluecitycapital.com"
receiver_email  = "todd.gilbey@synergex-systems.com" 
tech_department = "hello@bluecitycapital.com"

directory_code  = "390295C323775C4285AE93D9818F5103"

# Logs Workspace Information
LOGS_WORKSPACE_ID           =   "e30d973a-e8ad-4c66-8c0b-59f86e781b6d"
LOGS_WORKSPACE_KEY          =   "MjbHEQvhnBnxmf7btH20hVPXi8Db+i6+4V4fMbq9DL5pswnyvka6q9V64G3PEmRdJoQeUW0GmGOV81d4I+Xhcw=="   
LOGS_API_ENDPOINT_REGION    =   "uksouth"

# Data Collection Endpoint
DATA_COLLECTION_ENDPOINT    =   f"https://vmstatusdce-o0w0.{LOGS_API_ENDPOINT_REGION}-1.ingest.monitor.azure.com"
  
def assign_log_number(func) -> str:
    @wraps(func)
    def wrapper(*args, **kwargs):
        assign_log_number = generate_incident_ref()
        try:
            return func(*args, **kwargs, assign_log_number = assign_log_number)
        except Exception as e:
            raise e
    return wrapper

def create_freshdesk_ticket(logging_incident_number:str, exception_or_error_message:str, group_id:int = 201000039106, responder_id:int = 201002411183, subject:str = "Github is a true Git sometimes!") -> None:
    """
    Creates a Freshdesk ticket on behalf of the end user. This will be sent straight to the users inbox, where the user can add further information if they need to/
    
    This function must be called within a function which utulizes the assign_log_number decorator.

    This function will only be called when an exception is thrown. The exception message will be passed to the 'exception' parameter.
    """
    
    FRESHDESK_DOMAIN    = "bluecitycapitaltechnologies"
    API_KEY             = "RTBtMGlwfVik2cuaj1"
    API_URL             = f'https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2/tickets/'

    description = f"This support ticket has been automatically generated because of the following error or exception message {exception_or_error_message}. Log number {logging_incident_number}"

    ticket_data = {
        "subject"     : subject,
        "description" : description, 
        'priority'    : 1,
        'status'      : 2,
        'group_id'    : group_id,
        'responder_id': responder_id,
        'requester'   : {
            'name'    : receiver_name,
            'email'   : receiver_email  
        } 
    }

    custom_message  = None
    ticket_id       = None
    
    try:
        response = r.post(
            API_URL,
            auth    = (API_KEY, 'X'),
            json    = j.dumps(ticket_data),
            timeout = 30,
            headers = {'Content-Type' : 'application/json'}
        )

    except TypeError as e:
        custom_message = f"Type Error Exception: {e}"
    
    except r.RequestException as e:
        custom_message = f"Requests Exception: {e}"

    except Exception as e:
        custom_message = f"General Exception: {e}"

    else:
    
        if response.status_code == 201:
            
            ticket_info = response.json
            ticket_id   = ticket_info.get("id")

            print(ticket_id)

        elif response.status_code == 429:
            custom_message = f"API request limit exceeded: {response.status_code}"
        
        else:
            custom_message = f"Support Ticket Creation Error. Error code: {response.status_code} Error HTTP response: {response.text} Error response {response.content}"

    if custom_message:
        print(custom_message)

    return ticket_id

def send_message(custom_message:str, sender_name:str, receiver_name:str, incident_ref:str) -> None | str:
    """Sends a message which collects an incident number from the 'assign_log_number' decorator & passes it to the 'message_body' function."""
    msg             = MIMEMultipart()
    msg['Subject']  = "Github Push Incident"
    msg['From']     = f'"{sender_name}" <{sender_email}>'
    msg['To']       = receiver_email
    body            = MIMEText(email_body(custom_message, sender_name, receiver_name, incident_ref), 'html')
    msg.attach(body)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"{e} {incident_ref}.")
      
    return
    
def email_body(custom_message:str, sender_name:str, receiver_name:str, incident_ref:str) -> str:
    
    was_ticket_generated    = create_freshdesk_ticket(incident_ref,custom_message)
    ticket_id               = was_ticket_generated if was_ticket_generated is not None else "No support ticket available."
    
    ticket_return_message = (
        "A support ticket was generated. You should receive this shortly."
        if was_ticket_generated is not None
        else "Apologies, but we encountered an internal technical issue that prevented the creation of a support ticket. You can still reach out to us by referencing the incident log number provided below. Thank you for your understanding and cooperation."
    )

    resource_data_table = f"""
        <table border="0" cellpadding="5" cellspacing="0" style="border-collapse: collapse; text-align: left;">
            <tr>
                <th>Incident Number:</th>
                <td>{incident_ref}</td>
            </tr>
            <tr>
                <th>Support Ticket ID:</th>
                <td>{ticket_id}</td>
            </tr>
            <tr>
                <th>Degradation:</th>
                <td>{custom_message}</td>
            </tr>
        </table>
    """
    return f"""Dear {receiver_name}<br><br>
    We are writing to you because we have logged an incident pertaining to your Git Repo.<br><br>
    {ticket_return_message}<br><br>
    =========================<br><br>
    {resource_data_table}<br>
    =========================<br><br>
    In the future, any error or incident will automatically generate a support ticket which will be sent - via email - to the users inbox where they will be abe to add any further information they may wish, be assigned a support engineer & to have a direct point of contact.<br><br>
    Yours sincerely,<br><br>
    {sender_name}
    """

def generate_incident_ref() -> str:
    """Generates a universally unique identifier (UUID) to be used as a log number. UUID version 4 is used."""
    return f"{uuid.uuid4()}"

@assign_log_number
def run_command(command:str, cwd:str = None, assign_log_number:str = None) -> str:
    """Run a command in the terminal and capture the output. An email will be sent in the event of an error, stating the nature of the error. No message will be printed if there are no errors."""
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    
    custom_message = None
    
    if result.returncode != 0:
        custom_message =  result.stderr.strip() if result.stderr else "Unknown error occured - check repo directory as a possible solution"
        send_message(custom_message, sender_name, receiver_name, assign_log_number)
        return custom_message
    else:
        return result.stdout
    

@assign_log_number    
def check_for_changes(cwd:str, assign_log_number:str = None) -> bool:
    """Checks for both staged and unstaged changes in your local repo.
    """
    
    custom_message = None
    
    try:
        result = run_command(["git", "status", "--short"], cwd)
         
        if result.strip():
            print("Making Changes to Repo....")
            return True
        
        print("There were no changes to the working tree detected.")
        return False
    
    except TypeError as e:
        custom_message = f"TypeError Exception {e}"
    
    except Exception as e:
        custom_message = f"General Exception {e}"

    if custom_message:
        #send_message(custom_message, sender_name, receiver_name, assign_log_number)
        print(custom_message)

    return

@assign_log_number 
def is_valid_directory(cwd:str, assign_log_number:str = None) -> bool:
    if os.path.isdir(cwd):
        os.chdir(cwd)
        print(f"{cwd} | This is a valid directory")
        if is_git_repo(cwd, assign_log_number):
            return True
        else:
            return False
    else:
        custom_message = f"{cwd} is not a valid directory. Please check you have specified an existing directory & that this contains a .git folder."
        print(custom_message)
        send_message(custom_message, sender_name, receiver_name, assign_log_number)
        return False

def is_git_repo(cwd, log_incident) -> bool:
    git_path = os.path.join(cwd, '.git')
    if os.path.isdir(git_path):
        print(f"The directory '{cwd}' is a Git repository.")
        return True
    else:
        custom_message = f"{cwd} is not a Git Repository. Run 'git init' from the command shell "
        print(custom_message)
        send_message(custom_message,sender_name, receiver_name, log_incident)
        return False
    
def push_to_github() -> None:
    """Adds, commits and pushes all files to the Git repo. Each 'run_command' will be individually checked, and will log an incident when any return an error."""
    
    base_dir = f"C:/Users/SynergexSystems/AppData/Roaming/MetaQuotes/Terminal/{directory_code}/MQL4"
    #base_dir = "C:/Users/toddg/Onedrive" ##Remove on Production
    sub_dirs = {"Scripts", "Experts", "Include", "Images", "Files"}
    #sub_dirs = {"dollsoles","workspaces","apps","apps"} ##Remove on production

    while True:
    
        for sub_dir in sub_dirs:
            
            cwd = str(Path(base_dir) / sub_dir)
            
            if is_valid_directory(cwd):
                                
                commit_message = f"GitHub Push: {sub_dir.capitalize()}"
                    
                if check_for_changes(cwd):
                    
                    #Stages changes.
                    run_command(["git", "add", "."], cwd)

                    #Commits the staged changed, saving them.
                    run_command(["git", "commit", "-m", commit_message], cwd)

                    #Pushed them to the repo
                    run_command(["git", "push"], cwd)

                    print(f"Changes to directory {cwd} have been made")

                    monitor_commits()
                
                else:
                    continue

        time.sleep(1800)

if __name__ == "__main__":
    push_to_github()