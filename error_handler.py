import logging


def status_logger(subject:str, message:str, logging_level = logging.INFO) -> None:
    """
    Handles and processes the reporting of all error and exceptions via the Freshdesk system.
    Args:
        subject(str): Denotes the subject of the support ticket.
        message(str): Denotes the description of the error or exception. 
    """

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(

        level=logging_level,
        filename="log.log",
        filemode='a',
        format='%(levelname)s: %(message)s'

    )

    log_message = f"Status Subject: {subject} -> Status Message: {message}"

    logging.log(logging_level, log_message)

    return None

if __name__ == "__main__":
    status_logger("Test Error", "This is a test error message.")