from celery import shared_task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace these with your own Postmarkapp SMTP server credentials
SMTP_SERVER = "smtp-broadcasts.postmarkapp.com"
SMTP_PORT = 2525
SMTP_USERNAME = "431bf003-7e6d-485b-8412-8aec9e2f2565"
SMTP_PASSWORD = "431bf003-7e6d-485b-8412-8aec9e2f2565"
SMTP_HEADER = "X-PM-Message-Stream: broadcast"


@shared_task
def send_email(email, token):
    # Create the email message
    sender_email = "mohi@falahiardakani.com"
    recipient_email = email
    subject = "Token for Change Password"
    message = f"Token: {token}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent:", str(e))
