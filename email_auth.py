import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import settings_mapper
import error_handler

load_dotenv()

SMTP_CREDENTIALS = {
    "SMTP_SERVER"       : os.getenv("SMTP_SERVER"),
    "SMTP_EMAIL"        : os.getenv("SMTP_EMAIL"),
    "SMTP_PASSWORD"     : os.getenv("SMTP_PASSWORD"),
    "SMTP_PORT"         : os.getenv("SMTP_PORT")
}

def smtp_auth(message_body:str, subject:str, mime_text:str = "html") -> bool:
    """Authenticate the SMTP credentials, if False, it will terminate the programme"""
    try:
        if not SMTP_CREDENTIALS["SMTP_EMAIL"] or not SMTP_CREDENTIALS["SMTP_PASSWORD"] or not SMTP_CREDENTIALS["SMTP_PORT"] or not SMTP_CREDENTIALS["SMTP_SERVER"]:
            raise ValueError("One or nore of your SMTP credentials are mising, please chek these details.")
        
    except ValueError as e:
        error_handler.report_error("Missing SMTO Credentials", f"{e}")
        return False
    
    except Exception as e:
        error_handler.report_error("SMTO Authentication Error", f"{e}")
        return False
    
    else:
    
        msg             = MIMEMultipart()
        msg['Subject']  = subject
        msg['From']     = f'"{settings_mapper.MESSAGING_METADATA["SENDER_NAME"]}" <{settings_mapper.MESSAGING_METADATA["SENDER_EMAIL"]}>'
        msg['To']       = settings_mapper.MESSAGING_METADATA["REQUESTER_EMAIL"]
        body            = message_body
        msg.attach(MIMEText(body, mime_text))

        try:
            
            with smtplib.SMTP(SMTP_CREDENTIALS["SMTP_SERVER"], SMTP_CREDENTIALS["SMTP_PORT"]) as server:

                server.starttls()

                server.login(SMTP_CREDENTIALS["SMTP_EMAIL"], 
                            SMTP_CREDENTIALS["SMTP_PASSWORD"]
                )
                server.sendmail(settings_mapper.MESSAGING_METADATA["SENDER_EMAIL"],
                                settings_mapper.MESSAGING_METADATA["REQUESTER_EMAIL"], 
                                msg.as_string()
                )

                return True
        
        except ValueError as e:
            error_handler.report_error("Missing SMTO Credentials", f"{e}")
            return False
        
        except Exception as e:

            custom_message = f"Error sending email: {e}"
            custom_subject  = "SMTP Authentication Error"

            error_handler.report_error(custom_subject, custom_message)
            return False