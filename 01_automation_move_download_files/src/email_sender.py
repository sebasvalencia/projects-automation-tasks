import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from typing import List
import ssl

class EmailSender:
    def __init__(self, smtp_server: str, stmp_port: int, email_user: str, email_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = stmp_port
        self.email_user = email_user
        self.email_password = email_password
    
    def create_email_message(self, subject: str, body: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.email_user
        message["To"] = self.email_user
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))
        return message
    
    def generate_email_body(self, amount_items: int, moved_items: List[str], destination_folder: str) -> str:
        return f"""
        <html>
        <body>
        <h3>They have moved {amount_items} items to the folder {destination_folder}.</h3>
        <p>List of elements:</p>
        <ul>
        {''.join(f'<li>{item}</li>' for item in moved_items)}
        </ul>
        </body>
        </html>
        """
    
    def send_email(self, message: MIMEMultipart) -> None:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.email_user, self.email_password)
            server.sendmail(self.email_user, self.email_user, message.as_string())
    
    def send_email_report(self, amount_items: int, moved_items: List[str], destination_folder: str) -> None:
        subject = 'Report moved files'
        body = self.generate_email_body(amount_items, moved_items, destination_folder)
        message = self.create_email_message(subject, body)
        self.send_email(message)
        