import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import messaging_comms
import freshdesk_ticket

#SMTP Authentication 
SMTP_SERVER         =   "smtp-relay.brevo.com"
SMTP_EMAIL          =   "448c41002@smtp-brevo.com"
SMTP_PASSWORD       =   "hSg19RUfw6QIcV7b"
SMTP_PORT           =   587

def smtp_auth(message_body:str, subject:str, mime_text:str = "html") -> bool:
    
    msg             = MIMEMultipart()
    msg['Subject']  = subject
    msg['From']     = f'"{messaging_comms.sender_name}" <{messaging_comms.sender_email}>'
    msg['To']       = messaging_comms.receiver_email
    body            = message_body
    msg.attach(MIMEText(body, mime_text))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(messaging_comms.sender_email, messaging_comms.receiver_email, msg.as_string())
            print("SMTP Successfully Authenticated")
            return True
    except Exception as e:
        custom_message = f"Error sending email: {e}"
        custom_subject  = "SMTP Authentication Error"
        print(custom_subject)
        print(custom_message)
        freshdesk_ticket.create_freshdesk_ticket(custom_message, custom_subject)
        return False

    return False
