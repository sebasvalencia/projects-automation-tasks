import os
from dotenv import load_dotenv

from src.email_sender import EmailSender
from src.move_download_files import MoveItems



def main():
    load_dotenv()

    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD)
    moveItems = MoveItems(email_sender)
    moveItems.move_files_and_folders()

if __name__ == '__main__':
    main()