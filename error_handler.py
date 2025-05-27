from freshdesk_ticket import create_freshdesk_ticket

def report_error(subject:str, error_message:str, debug:bool = False) -> None:
    """This method will be called whenever an error or Exception occurs. 
    A support ticket will be generated via the FreshDesk system. Please ensure that you regularly check your FreshDesk dashboard for any emergent issues. 
    Args:
        subject(str): Denotes the subject of the error, which will be sent to Freshdesk.
        error_message(str): Denoted the message and description of the error, which will be sent to Freshdesk.
    """
    print(f"{subject} - { error_message}")

    if debug:
        
        print("Debug mode is enabled. A support ticket will not be created whilst in debug mode.")

        return
    
    create_freshdesk_ticket(error_message, subject)

    return