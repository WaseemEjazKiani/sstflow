import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env
sender_email = os.getenv("EMAIL_USER")
sender_password = os.getenv("EMAIL_PASS")



def send_404_report(report_list, coming_soon_list=None):
    receiver_email = "waseemejazkiani@gmail.com"

    subject = "Products Automation Report"

    # Prepare email body
    body = ""

    if report_list:
        body += "❌ The following products returned 404:\n\n"
        for item in report_list:
            body += f"- {item}\n"
        body += "\n"

    if coming_soon_list:
        body += "⚠️ The following products are showing Coming Soon on Avalability:\n\n"
        for item in coming_soon_list:
            body += f"- {item}\n"

    if not body:
        body = "No 404 or Coming Soon products found."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
