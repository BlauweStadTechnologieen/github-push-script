import json as j
import requests as r
import email_auth, send_email

def create_freshdesk_ticket(exception_or_error_message:str, subject:str, group_id:int = 201000039106, responder_id:int = 201002411183) -> int:
    """
    When an exception or error occurs during the execution of a function within this package, this will lodge a support toclet with Freshdesk. 
    A notification that a ticket has been created will be sent to the users email. When this function is called, it will return the ticket id.

    You will need to manually pass the exception_or_error_message and the subject parameters prior to calling the function. 

    The group_id and the responder_id parameters have been set to defaults, however, you may override these if necessary. 
    """
    
    FRESHDESK_DOMAIN    = "bluecitycapitaltechnologies"
    API_KEY             = "RTBtMGlwfVik2cuaj1"
    API_URL             = f'https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2/tickets/'

    description = f"""
    Dear {email_auth.receiver_name}<br>
    A support ticket has been automatically generated because of the following error or exception message:<br><br>
    {exception_or_error_message}<br><br>
    ===================================================
    """

    ticket_data = {
        "subject"     : subject,
        "description" : description, 
        'priority'    : 1,
        'status'      : 2,
        'group_id'    : group_id,
        'responder_id': responder_id,
        'requester'   : {
            'name'    : email_auth.receiver_name,
            'email'   : email_auth.receiver_email 
        } 
    }

    custom_message  = None
    ticket_id       = None
    
    try:
        response = r.post(
            API_URL,
            auth    = (API_KEY, 'X'),
            json    = j.dumps(ticket_data),
            timeout = 30,
            headers = {'Content-Type' : 'application/json'}
        )

    except TypeError as e:
        custom_message = f"Type Error Exception: {e}"
    
    except r.RequestException as e:
        custom_message = f"Requests Exception: {e}"

    except Exception as e:
        custom_message = f"General Exception: {e}"

    else:
    
        if response.status_code == 201:
            
            ticket_info = response.json
            ticket_id   = ticket_info.get("id")

        elif response.status_code == 429:
            custom_message = f"API request limit exceeded: {response.status_code}"
        
        else:
            custom_message = f"Support Ticket Creation Error. Error code: {response.status_code} Error HTTP response: {response.text} Error response {response.content}"

    if custom_message:
        print(custom_message)
        send_email.freshdesk_inop_notification(custom_message)

    return ticket_id