import os
from dotenv import load_dotenv

load_dotenv()

MESSAGING_METADATA = {
     "SENDER_DOMAIN"            : os.getenv("SENDER_DOMAIN"), 
     "SENDER_NAME"              : os.getenv("SENDER_NAME"),
     "SENDER_DEPARTMENT"        : os.getenv("SENDER_DEPARTMENT"),
     "SENDER_EMAIL"             : f"{os.getenv("SENDER_DEPARTMENT").lower()}{os.getenv("SENDER_DOMAIN")}",
     "REQUESTER_NAME"           : os.getenv("REQUESTER_NAME"),
     "REQUESTER_EMAIL"          : os.getenv("REQUESTER_EMAIL")
}

GITHUB_CONSTANTS={
    "OWNER"             : os.getenv("OWNER"),
    "GITHUB_TOKEN"      : os.getenv("GITHUB_TOKEN")
}

DIRECTORY_CONSTANTS = {
    "DIRECTORY_CODE"    : os.getenv("DIRECTORY_CODE"),
    "BASE_DIR"          : os.getenv("BASE_DIR")
}