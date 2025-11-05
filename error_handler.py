import logging

logging.basicConfig(filename="log.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def report_error(subject: str, error_message: str, debug: bool = False) -> None:
    
    logging.debug(f"{subject} - {error_message}")

    return

if __name__ == "__main__":
    report_error("Test Error", "This is a test error message.")