import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RECEIVER_DOMAIN     =   "@synergex-systems.com"
SENDER_DOMAIN       =   "@bluecitycapital.us"

#SMTP Authentication 
SMTP_SERVER         =   "smtp-relay.brevo.com"
SMTP_EMAIL          =   "448c41002@smtp-brevo.com"
SMTP_PASSWORD       =   "hSg19RUfw6QIcV7b"
SMTP_PORT           =   587

#User Information
receiver_name       =   "Synergex Systems Limited"
receiver_email      =   f"comms{RECEIVER_DOMAIN}"
sender_name         =   "Blue City Capital Technologies, Inc"
sender_email        =   f"notifications{SENDER_DOMAIN}"

def smtp_auth(message_body:str, subject:str, mime_text:str = "html") -> None:
    
    msg             = MIMEMultipart()
    msg['Subject']  = subject
    msg['From']     = f'"{sender_name}" <{sender_email}>'
    msg['To']       = receiver_email
    body            = message_body
    msg.attach(MIMEText(body, mime_text))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
