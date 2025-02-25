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
sender_name     =  "Blue City Capital Technologies Inc"

sender_email    = "notifications@bluecitycapital.com"
receiver_email  = "todd.gilbey@synergex-systems.com" 
tech_department = "hello@bluecitycapital.com"

def send_message(commit_sha:str = None, repository_name:str = None, api_url:str = None):
    
    resource_data_table = f"""
        <table border="0" cellpadding="5" cellspacing="0" style="border-collapse: collapse; text-align: left;">
            <tr>
                <th>Secure Hash Algorithm:</th>
                <td>{commit_sha}</td>
            </tr>
            <tr>
                <th>Repository Name:</th>
                <td>{repository_name}</td>
            </tr>
            <tr>
                <th>API URL:</th>
                <td>{api_url}</td>
            </tr>
        </table>
    """
    
    message_body = f"""
    Dear {receiver_name}<br>
    We are writing to you because you have a new commit that has just been uploaded into your GitHub repository.<br>
    You have a new commit, with a commit SHA of {commit_sha[:7]} for the repo name {repository_name}, check it out on The Hub of The Git!<br>
    ========================
    {resource_data_table}
    ========================<br>
    Yours sincerly<br>
    {sender_name}
    <br><br>
    """
    
    msg             = MIMEMultipart()
    msg['Subject']  = "Git Commit Notification | You have a new commit."
    msg['From']     = f'"{sender_name}" <{sender_email}>'
    msg['To']       = receiver_email
    body            = message_body
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(USERNAME_EMAIL, SENDER_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")