import configparser
import smtplib
import dotenv
import time
import csv
import ssl
import os
from email.message import EmailMessage
from email.utils import formataddr

dotenv.load_dotenv()
sender_email = os.getenv("EMAIL")
email_password = os.getenv("PASSWORD")
smtp_port = os.getenv("PORT")
smtp_server = os.getenv("SMTP_SERVER")

config = configparser.ConfigParser()
config.read("automail.conf")

# subject of the email
email_subject = config.get("DEFAULT", "SUBJECT").strip('"')

# attachments of the email
resume_file = config.get("DEFAULT", "RESUME_FILE").strip('"')
cover_letter_file = config.get("DEFAULT", "COVER_LETTER_FILE").strip('"')
if not os.path.exists(resume_file):
    print("❌ Oops! Resume is missing")
    exit(0)
if not os.path.exists(cover_letter_file):
    print("❌ Oops! Cover letter is missing")
    exit(0)

# body of the email
first_name = config.get("DEFAULT", "FIRST_NAME").strip('"')
last_name = config.get("DEFAULT", "LAST_NAME").strip('"')
university = config.get("DEFAULT", "UNIVERSITY").strip('"')
position = config.get("DEFAULT", "POSITION").strip('"')
company = config.get("DEFAULT", "COMPANY").strip('"')
own_body = config.get("DEFAULT", "OWN_BODY", fallback="").strip('"')

"""
option 1 : You write your own body message

option 2 : You use the default body message with the company name

option 3 : You have left the company name blank in automail.conf and you use the default message body without the company name.
"""

if own_body:  # option 1
    email_body = own_body.strip('"')
elif company:  # option 2
    email_body = f"Dear,\n\nI am writing to apply for the {position} position at {company}. I am a student at the {university} and I am very interested in the position. I have attached my resume and cover letter to this email. Thank you for considering my application. I look forward to hearing from you soon.\n\nSincerely,\n{first_name} {last_name}"
else:  # option 3
    email_body = f"Dear,\n\nI am writing to apply for the {position} position. I am a student at the {university} and I am very interested in the position. I have attached my resume and cover letter to this email. Thank you for considering my application. I look forward to hearing from you soon.\n\nSincerely,\n{first_name} {last_name}"

context = ssl.create_default_context()
with open("data/recipients.csv") as file:
    email_recipients = csv.reader(file)
    next(email_recipients)
    for email_recipient in email_recipients:
        print(f"Sending email to {email_recipient}")
        email_message = EmailMessage()
        email_message["From"] = formataddr((f"{first_name} {last_name}", sender_email))
        email_message["To"] = email_recipient
        email_message["Subject"] = email_subject
        email_message.set_content(email_body)
        
        with open(resume_file, 'rb') as content_file:
            content = content_file.read()
            email_message.add_attachment(content, maintype='application', subtype="pdf", filename=resume_file)

        with open(cover_letter_file, 'rb') as content_file:
            content = content_file.read()
            email_message.add_attachment(content, maintype='application', subtype="pdf", filename=cover_letter_file)

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(sender_email, email_password)
                server.send_message(email_message)
            print(f"✅ All good ! Email sent to {email_recipient}")
        except smtplib.SMTPAuthenticationError:
            print(f"❌ Oops! Authentication error. Please check your email credentials.")
        except smtplib.SMTPConnectError:
            print(f"❌ Oops! Connection error.")
        time.sleep(5)
