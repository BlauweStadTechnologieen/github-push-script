import logging

# Configure logging once, at program start
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("log.log", mode='a'),
        #logging.StreamHandler()  # optional: prints to console too
    ]
)

def status_logger(subject: str, message: str, logging_level=logging.INFO):
    log_message = f"Status Subject: {subject} -> Status Message: {message}"
    logging.log(logging_level, log_message)

if __name__ == "__main__":
    status_logger("Test Error", "This is a test error message.")