import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.development")

MESSAGING_METADATA = {
     "SENDER_DOMAIN"        : os.getenv("SENDER_DOMAIN"), 
     "SENDER_NAME"          : os.getenv("SENDER_NAME"),
     "SENDER_DEPARTMENT"    : os.getenv("SENDER_DEPARTMENT"),
     "SENDER_EMAIL"         : os.getenv("SENDER_EMAIL"),
     "REQUESTER_NAME"       : os.getenv("REQUESTER_NAME"),
     "REQUESTER_EMAIL"      : os.getenv("REQUESTER_EMAIL")
}

GITHUB_CONSTANTS={
    "OWNER"                 : os.getenv("OWNER"),
    "GITHUB_TOKEN"          : os.getenv("GITHUB_TOKEN")
}

DIRECTORY_CONSTANTS = {
    "PARENT_DIRECTORY"      : os.getenv("PARENT_DIRECTORY"),
    "DEV_BASE_DIR"          : os.getenv("DEV_BASE_DIR")
}