import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server     = "smtp-relay.brevo.com"
smtp_port       = 587
USERNAME_EMAIL  = "448c41002@smtp-brevo.com"

SENDER_PASSWORD = "hSg19RUfw6QIcV7b"
RECIPIENT_EMAIL = "todd.gilbey@synergex-systems.com"
SMTP_PORT       = 587

receiver_name   = "Synergex Systems"
sender_name     =  "Blue City Capital Technologies, Inc"

sender_email    = "notifications@bluecitycapital.com"
receiver_email  = "todd.gilbey@synergex-systems.com" 
tech_department = "hello@bluecitycapital.com"

GITHUB_URL      =   "https://github.com/{hub_owner}"

def send_message(latest_commit_data:dict, github_owner:str) -> None:
    
    github_url = GITHUB_URL.format(owner=github_owner)
    
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
            </table>
        """
    
    message_body = f"""
    Dear {receiver_name}<br><br>
    We are writing to you because you have a new commit that has just been uploaded into your GitHub repository.
    You have a new commit.<br><br>
    Check it out by visiting your GitHib at {github_url}<br><br>
    {resource_data_table}
    ========================================================================<br><br>

    * You must be logged into the GitHub Repository in order to see the list of commits within the API call. <br><br>
    Yours sincerely<br>
    <b>{sender_name}</b><br>
    Engineering Team<br><br>
    """
    
    msg             = MIMEMultipart()
    msg['Subject']  = f"New Commit Notificstion"
    msg['From']     = f'"{sender_name}" <{sender_email}>'
    msg['To']       = receiver_email
    body            = message_body
    msg.attach(MIMEText(body, "html"))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(USERNAME_EMAIL, SENDER_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")