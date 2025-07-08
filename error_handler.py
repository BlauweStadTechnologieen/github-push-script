from freshdesk_ticket import create_freshdesk_ticket
import logging
import sys

# DON'T disable logging unless absolutely necessary
# logging.disable(logging.CRITICAL)

def report_error(subject: str, error_message: str, logging_level=logging.DEBUG, error_log_file = "error.log") -> None:

    # Reset logging handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging
    logging.basicConfig(

        level=logging_level,
        filename= error_log_file,
        filemode='a',
        format='%(levelname)s: %(message)s'

    )

    log_message = f"{subject} - {error_message}"

    # Log the message dynamically
    logging.log(logging_level, log_message)

    if logging_level <= logging.WARNING:
        
        return

    if logging_level >= logging.ERROR:

        create_freshdesk_ticket(error_message, subject)

        sys.exit("The script has encountered a critical error and will now exit. Please check the error log for details.")