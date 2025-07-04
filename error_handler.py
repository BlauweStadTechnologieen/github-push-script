from freshdesk_ticket import create_freshdesk_ticket
import logging
import sys

# DON'T disable logging unless absolutely necessary
# logging.disable(logging.CRITICAL)

def report_error(subject: str, error_message: str, logging_level=logging.DEBUG) -> None:

    # Reset logging handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure logging
    logging.basicConfig(

        level=logging_level,
        filename='error.log',
        filemode='a',
        format='%(levelname)s: %(message)s: %(funcName)s'

    )

    if logging_level <= logging.WARNING:

        print(f"{logging.getLevelName(logging_level)}: {subject} - {error_message}")
        
        return

    if logging_level >= logging.ERROR:

        create_freshdesk_ticket(error_message, subject)

        sys.exit(f"Exiting due to incident: " + subject)