import logging

logging.basicConfig(filename="success.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def success_log(success_subject: str, success_message: str) -> None:
    
    logging.debug(f"{success_subject} - {success_message}")

    return

if __name__ == "__main__":
    success_log("Test Success", "This is a test success message.")