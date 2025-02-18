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

def send_message(commit_sha):
    """Sends a message which collects an incident number from the 'assign_log_number' decorator & passes it to the 'message_body' function."""
    
    message_body = f"""
    Dear Someone<br>
    You have a new commit, with a commit SHA of {commit_sha[:7]}, check it out on The Hub of The Git!
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