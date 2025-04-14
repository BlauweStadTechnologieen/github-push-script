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
    """Authenticate the SMTP credentials.
    
    Args:
        message_body(str): Denotes the body of the message.
        subject(str)`: Denotes the subject line of the message.
        mime_text(str, optional): Denotes the email format. Defauls to "html".
    
    Returns:
        bool: Returns `True` if the SMTP credentilas are authenticated, else it will return `False`, and send a Freshdesk support ticket with the details of the error
    
    Exceptions:
        KeyError: Raised if any SMTP credential is missing.
        Exception: Catches & handles any unexpected errors during validations.

    Notes:
        Any error or caught Exception will he handled by the error hander module whereby a support ticket will be generated.  

    """
    try:
        if not SMTP_CREDENTIALS["SMTP_EMAIL"] or not SMTP_CREDENTIALS["SMTP_PASSWORD"] or not SMTP_CREDENTIALS["SMTP_PORT"] or not SMTP_CREDENTIALS["SMTP_SERVER"]:
            raise KeyError("One or nore of your SMTP credentials are mising, please check these details.")
        
        msg             = MIMEMultipart()
        msg['Subject']  = subject
        msg['From']     = f'"{settings_mapper.MESSAGING_METADATA["SENDER_NAME"]}" <{settings_mapper.MESSAGING_METADATA["SENDER_EMAIL"]}>'
        msg['To']       = settings_mapper.MESSAGING_METADATA["REQUESTER_EMAIL"]
        body            = message_body
        msg.attach(MIMEText(body, mime_text))

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
    
    
    except KeyError as e:
        error_handler.report_error("Missing SMTP Credentials", f"{e}")
        return False
    
    except smtplib.SMTPAuthenticationError as e:
        error_handler.report_error("SMTP Authentication Error", f"{e}")

    except smtplib.SMTPConnectError as e:
        error_handler.report_error("SMTP Connection Error",f"{e}")

    except smtplib.SMTPResponseException as e:
        error_handler.report_error("SMTP Response Exception",f"{e}")
    
    except Exception as e:
        error_handler.report_error("SMTP Exception Error", f"{e}")
        
    return False
    
    
    
        

        