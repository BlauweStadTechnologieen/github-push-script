from freshdesk_ticket import create_freshdesk_ticket
from send_email import send_error_report_by_email
import logging

logging.basicConfig(filename="logger.log", filemode='a', format='%(asctime)s - %(funcName)s')

logging.disable(logging.CRITICAL)
logging.disable()

def report_error(subject:str, error_message:str, debug:bool = False) -> None:
    """This method will be called whenever an error or Exception occurs. 
    A support ticket will be generated via the FreshDesk system. Please ensure that you regularly check your FreshDesk dashboard for any emergent issues. 
    Args:
        subject(str): Denotes the subject of the error, which will be sent to Freshdesk.
        error_message(str): Denoted the message and description of the error, which will be sent to Freshdesk.
    """
    logging.debug(f"{subject} - { error_message}")

    if debug:
        
        print("Debug mode is enabled. A support ticket will not be created whilst in debug mode.")

        return
    
    send_error_report_by_email(subject, error_message)
    
    create_freshdesk_ticket(error_message, subject)

    return