import json as j
import requests as r
import os
from dotenv import load_dotenv
import settings_mapper

load_dotenv()

FRESHDESK_CREDENTIALS = {
    "FRESHDESK_DOMAIN" : os.getenv("FRESHDESK_DOMAIN"),
    "FRESHDESK_API_KEY": os.getenv("FRESHDESK_API_KEY")
}

def create_freshdesk_ticket(exception_or_error_message:str, subject:str, group_id:int = 201000039106, responder_id:int = 201002411183) -> int:
    
    """
    Creates a Freshdesk support ticket in the event of an error of Exception occuring. 

    Args:
        exception_or_error_message (str): Customized error message or exception. If this is called 
        by an exception handling block, it will denote the exception message, otherwise it will 
        be the custom message provided by the user,
        subject (str): Denotes the subject of the support ticket,
        group_id (int, optional): Denotes the technical team to whom the support ticket is sent to. Defaults to `201000039106`,
        responder_id (int, optional): Denotes the support agent to whom the support ticket is sent. Defaults to `201002411183`.

    Returns:
        ticket_id (int): A support ticket number is generated; otherwise, it will return `None`. 
            If `None` is returned, the `send_email` module will be executed, sending an email to 
            the user notifying them that it was unable to generate a support ticket.

    Exceptions:
        TypeError: Raised when there is a conflict of type errors.
        KeyError: Raised if any credentials are missing.
        RequestException: Raised when the API request fails.
        Exception: Catches any other error that may occur.
    """
    
    try:
    
        if not settings_mapper.MESSAGING_METADATA["REQUESTER_NAME"] or not settings_mapper.MESSAGING_METADATA["REQUESTER_EMAIL"]:
            raise KeyError("Messaging metadata is missing in your  file. Please verify it and try again.")
    
        if not FRESHDESK_CREDENTIALS["FRESHDESK_API_KEY"] or not FRESHDESK_CREDENTIALS["FRESHDESK_DOMAIN"]:
            raise KeyError("Some of your Freshdesk credentials are missing. Please provide them and try again.")
        
        API_URL = f'https://{FRESHDESK_CREDENTIALS["FRESHDESK_DOMAIN"]}.freshdesk.com/api/v2/tickets/'

        description = f"""
        Dear {settings_mapper.MESSAGING_METADATA["REQUESTER_NAME"]}<br>
        A support ticket has been automatically generated because of the following error or exception message:<br><br>
        {exception_or_error_message}<br><br>
        ===================================================
        """

        ticket_data = {
            "subject"       : subject,
            "description"   : description, 
            'priority'      : 1,
            'status'        : 2,
            'group_id'      : group_id,
            'responder_id'  : responder_id,
            'name'          : settings_mapper.MESSAGING_METADATA["REQUESTER_NAME"],
            'email'         : settings_mapper.MESSAGING_METADATA["REQUESTER_EMAIL"]

        }

        custom_message  = None
        ticket_id       = None
                    
        response = r.post(
            API_URL,
            auth    = (FRESHDESK_CREDENTIALS["FRESHDESK_API_KEY"], 'X'),
            json    = j.dumps(ticket_data),
            timeout = 30,
            headers = {'Content-Type' : 'application/json'}
        )

        if response.status_code == 201:
            
            ticket_info = response.json
            ticket_id   = ticket_info.get("id")
            return ticket_id

        else:
            custom_message = f"Error code: {response.status_code} Error HTTP response: {response.text} Error response {response.content}"
            print(custom_message)
            return response.status_code

    except AttributeError as e:
        custom_message = f"Unfortunatley there was an attribute error {e}"
    
    except TypeError as e:
        custom_message = f"Type Error Exception: {e}"
    
    except r.RequestException as e:
        custom_message = f"Requests Exception: {e}"

    except KeyError as e:
        custom_message = f"{e}"

    except Exception as e:
        custom_message = f"General Exception: {e}"

    if custom_message:
        print(custom_message)
        return -1