import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DOMAIN              =   "@bluecitycapital.com"
GITHUB_URL          =   "https://github.com/{owner}"

#SMTP Server Information
SMTP_SERVER         =   "smtp-relay.brevo.com"
SMTP_EMAIL          =   "448c41002@smtp-brevo.com"
SMTP_PASSWORD       =   "hSg19RUfw6QIcV7b"
SMTP_PORT           =   587

#Recipient Information
receiver_name       =   "Synergex Systems"
receiver_email      =   "todd.gilbey@synergex-systems.com"

#Sender Information
sender_name         =   "Blue City Capital Technologies, Inc"
sender_email        =   f"notifications{DOMAIN}"
sender_department   =   "Engineering"

#Support Information
tech_department     =   f"{sender_department.lower()}{DOMAIN}"

def send_message(latest_commit_data:dict, github_owner:str) -> None:
    
    github_url = GITHUB_URL.format(owner=github_owner)
    
    resource_data_table = ""
    for data in latest_commit_data:
            resource_data_table += f"""
            ========================================================================<br>
            <table border="0" cellpadding="5" cellspacing="0" style="border-collapse: collapse; text-align: left;">
                <tr>
                    <th>Secure Hash Algorithm (SHA):</th>
                    <td>{data["sha"][:7]}</td>
                </tr>
                <tr>
                    <th>Repository Name:</th>
                    <td>{data['repo']}</td>
                </tr>
                <tr>
                    <th>API URL:</th>
                    <td>{data['url']}</td>
                </tr>
            </table>
        """
    
    message_body = f"""
        Dear {receiver_name}<br><br>
        We are writing to you because you have a new commit uploaded to your GitHub repository.
        Check it out by visiting your GitHub account at {github_url}<br><br>
        {resource_data_table}
        ========================================================================<br><br>
        * You must be logged into the GitHub Repository in order to see the list of commits within the API call.<br><br>
        Yours sincerely<br>
        <b>{sender_name}</b><br>
        {sender_department} Team<br>
        {tech_department}<br><br>
    """
    
    msg             = MIMEMultipart()
    msg['Subject']  = f"New Commit Notificstion"
    msg['From']     = f'"{sender_name}" <{sender_email}>'
    msg['To']       = receiver_email
    body            = message_body
    msg.attach(MIMEText(body, "html"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")