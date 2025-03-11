

SENDER_DOMAIN       =   "@bluecitycapital.com"
RECEIVER_DOMAIN     =   "@synergex-systems.com"
receiver_name       =   "Synergex Systems Limited"
receiver_email      =   f"comms{RECEIVER_DOMAIN}"
sender_name         =   "Blue City Capital Technologies, Inc"
sender_email        =   f"notifications{SENDER_DOMAIN}"
sender_department   =   "Engineering"
tech_department     =   f"{sender_department.lower()+SENDER_DOMAIN}"

print(tech_department)