import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import messaging_comms
import freshdesk_ticket
import os
from dotenv import load_dotenv
import shared_config

load_dotenv()

SMTP_CREDENTIALS = {
    "SMTP_SERVER"       : os.getenv("SMTP_SERVER"),
    "SMTP_EMAIL"        : os.getenv("SMTP_EMAIL"),
    "SMTP_PASSWORD"     : os.getenv("SMTP_PASSWORD"),
    "SMTP_PORT"         : os.getenv("SMTP_PORT")
}

def smtp_auth(message_body:str, subject:str, mime_text:str = "html") -> bool:
    
    msg             = MIMEMultipart()
    msg['Subject']  = subject
    msg['From']     = f'"{shared_config.MESSAGING_METADATA("SENDER_NAME")}" <{shared_config.MESSAGING_METADATA("SENDER_EMAIL")}>'
    msg['To']       = shared_config.MESSAGING_METADATA("REQUESTER_EMAIL")
    body            = message_body
    msg.attach(MIMEText(body, mime_text))

    try:
        with smtplib.SMTP(SMTP_CREDENTIALS["SMTP_SERVER"], SMTP_CREDENTIALS["SMTP_PORT"]) as server:

            server.starttls()

            server.login(SMTP_CREDENTIALS["SMTP_EMAIL"], 
                         SMTP_CREDENTIALS["SMTP_PASSWORD"]
            )
            server.sendmail(shared_config.MESSAGING_METADATA("SENDER_EMAIL"),
                            shared_config.MESSAGING_METADATA("REQUESTER_EMAIL"), 
                            msg.as_string
            )

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
