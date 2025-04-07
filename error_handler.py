from freshdesk_ticket import create_freshdesk_ticket

def report_error(subject:str, error_message:str) -> None:
    """The master error handing method. This with both print and and call the `create_freshdesk_ticket` method, which will process the creation of a support ticket.
    Args:
        subject(str): Denotes the subject of the error, which will be send to Freshdesk.
        error_message(str): Denoted the message and description of the error, which will be sent to Freshdesk.
    Notes:
    -
        The Freshdesk system has not currently been rolled out, therefore, you will only see print statements in the command window. 
    """
    print(f"{subject} - { error_message}")
    #create_freshdesk_ticket(error_message, subject)
    return