import pytest
from email.mime.multipart import MIMEMultipart

from src.email_sender import EmailSender

@pytest.fixture
def email_sender():
    return EmailSender('smtp.gmail.com', 465, 'email@gmail.com', 'password')

def test_create_email_message(email_sender):
    subject = "Test Subject"
    body = "<h1>Test Body</h1>"
    message = email_sender.create_email_message(subject, body)
    
    assert isinstance(message, MIMEMultipart)
    assert message["From"] == 'email@gmail.com'
    assert message["To"] == 'email@gmail.com'
    assert message["Subject"] == subject
    assert body in message.as_string()

def test_generate_email_body(email_sender):
    amount_items = 3
    moved_items = ['file1.txt', 'file2.jpg', 'file3.pdf']
    destination_folder = '/some/destination/folder'
    body = email_sender.generate_email_body(amount_items, moved_items, destination_folder)
    
    assert f"They have moved {amount_items} items to the folder {destination_folder}." in body
    for item in moved_items:
        assert f"<li>{item}</li>" in body
