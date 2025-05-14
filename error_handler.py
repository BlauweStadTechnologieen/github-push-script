from freshdesk_ticket import create_freshdesk_ticket

def report_error(subject:str, error_message:str) -> None:
    """This method will be called whenever an error or Exception occurs. 
    A support ticket will be generated via the FreshDesk system. Please ensure that you regularly check your FreshDesk dashboard for any emergent issues. 
    Args:
        subject(str): Denotes the subject of the error, which will be send to Freshdesk.
        error_message(str): Denoted the message and description of the error, which will be sent to Freshdesk.
    Notes:
    -
        The Freshdesk system has not currently been rolled out, therefore, you will only see print statements in the command window. 
    """
    print(f"{subject} - { error_message}")
    create_freshdesk_ticket(error_message, subject)
    return