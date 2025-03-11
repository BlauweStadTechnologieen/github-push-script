import email_auth

RECEIVER_DOMAIN     =   "@synergex-systems.com"
receiver_name       =   "Synergex Systems Limited"
receiver_email      =   f"comms{RECEIVER_DOMAIN}"
sender_name         =   "Blue City Capital Technologies, Inc"
sender_email        =   f"notifications{email_auth.SMTP_DOMAIN}"
sender_department   =   "Engineering"
tech_department     =   f"{sender_department.lower()+email_auth.SMTP_DOMAIN}"