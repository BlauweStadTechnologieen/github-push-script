import messaging_comms
import email_auth
import uuid

def company_signoff() -> None:
    return f"""
    Yours sincerely<br>
    <b>{messaging_comms.sender_name}</b><br>
    The {messaging_comms.sender_department} Team<br>
    {messaging_comms.tech_department}<br><br>
    """

def send_message(latest_commit_data:dict, changed_repo_list:list, github_owner:str) -> None:
    
    GITHUB_URL      =   "https://github.com/{owner}"
    github_url      =   GITHUB_URL.format(owner=github_owner)
    custom_subject  =   "Github Commit Report"
    
    resource_data_table = ""
    for data in latest_commit_data:
            resource_data_table += f"""
            ========================================================================<br>
            <table border="0" cellpadding="5" cellspacing="0" style="border-collapse: collapse; text-align: left;">
                <tr>
                    <th>Secure Hash Algorithm (SHA):</th>
                    <td>{data["sha"][:7]}</td>
                </tr>
                <tr>
                    <th>Repository Name:</th>
                    <td>{data['repo']}</td>
                </tr>
                <tr>
                    <th>API URL:</th>
                    <td>{data['url']}</td>
                </tr>
                <tr>
                    <th>Commit Date:</th>
                    <td>{data['date']}</td>
                </tr>
                <tr>
                    <th>Author ID:</th>
                    <td>{data['id']}</td>
                </tr>
            </table>
            """    
            
    message_body = f"""
    Dear {messaging_comms.receiver_name}<br><br>
    We are writing to you because you have a new commit uploaded to your GitHub repository.
    Check it out by visiting your GitHub account at {github_url}<br><br>
    {resource_data_table}
    ========================================================================<br>
    The local directories which have been changed since the last commit are {changed_repo_list}<br><br>
    * You must be logged into the GitHub Repository in order to see the list of commits within the API call.<br><br>
    {company_signoff()}
    """
    email_auth.smtp_auth(message_body, custom_subject)

    return

def generate_incident_uuid() -> str:
    return f"""{uuid.uuid4()}"""

def freshdesk_inop_notification(custom_message:str) -> None:
      
    incident_uuid   =   generate_incident_uuid()
    custom_subject  =   "(CRMIN) CRM Inoperable Notification"
    
    freshdesk_inop_text_body = f"""
        Dear {messaging_comms.receiver_name}<br><br>
        We are writing to you because our support ticketing system is inoperable
        ========================================================================<br>
        <table border="0" cellpadding="5" cellspacing="0" style="border-collapse: collapse; text-align: left;">
            <tr>
                <th>Freshdesk Inoperative Reason:</th>
                <td>{custom_message}</td>
            </tr>
            <tr>
                <th>Incident reference Number</th>
                <td>{incident_uuid}</td>
            </tr>
        </table>
        ========================================================================<br><br>
        {company_signoff()}
    """

    print(freshdesk_inop_text_body)
    email_auth.smtp_auth(freshdesk_inop_text_body, custom_subject)

    return