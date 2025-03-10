import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import freshdesk_ticket

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

def smtp_auth(message_body:str, subject:str, mime_text:str = "html") -> bool:
    
    custom_subject = "SMTP Authentication Error"
    
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
            return True
    except Exception as e:
        custom_message = f"Error sending email: {e}"
        print(custom_message)
        freshdesk_ticket.create_freshdesk_ticket(custom_message, custom_subject)
        return False

    return False
