from freshdesk_ticket import create_freshdesk_ticket

def report_error(subject:str, error_message:str) -> bool:
    print(f"{subject} - { error_message}")
    #create_freshdesk_ticket(error_message, subject)
    return False