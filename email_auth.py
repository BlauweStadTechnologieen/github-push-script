import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import error_handler
from instance_validation import is_value_none

load_dotenv()

organization_smtp_server    = os.getenv("SMTP_SERVER")
organization_smtp_email     = os.getenv("SMTP_EMAIL")
organization_smtp_password  = os.getenv("SMTP_PASSWORD")
organization_smtp_port      = os.getenv("SMTP_PORT")
organization_sender_name    = os.getenv("SENDER_NAME")
organization_sender_email   = os.getenv("SENDER_EMAIL")
client_email                = os.getenv("REQUESTER_EMAIL")

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

        
        msg             = MIMEMultipart()
        msg['Subject']  = subject
        msg['From']     = f'"{organization_sender_name}" <{organization_sender_email}>'
        msg['To']       = client_email
        body            = message_body
        msg.attach(MIMEText(body, mime_text))

        with smtplib.SMTP(organization_smtp_server, organization_smtp_port) as server:

            server.starttls()

            server.login(organization_smtp_email, organization_smtp_password)
            
            server.sendmail(organization_sender_email,client_email, msg.as_string())

            return True
    
    except AttributeError as e:
        error_handler.report_error("Missing Attribute",f"{e}")
    
    except KeyError as e:
        error_handler.report_error("Missing SMTP Credentials", f"{e}")
    
    except smtplib.SMTPAuthenticationError as e:
        error_handler.report_error("SMTP Authentication Error", f"{e}")

    except smtplib.SMTPConnectError as e:
        error_handler.report_error("SMTP Connection Error",f"{e}")

    except smtplib.SMTPResponseException as e:
        error_handler.report_error("SMTP Response Exception",f"{e}")
    
    except Exception as e:
        error_handler.report_error("SMTP Exception Error", f"{e}")
        
    return False
    
    
    
        

        