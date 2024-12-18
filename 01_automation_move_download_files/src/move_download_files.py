import os
import datetime
import shutil
from typing import Tuple, Optional
from src.email_sender import EmailSender

class MoveItems:
    def __init__(self, email_sender: EmailSender):
        self.origin_folder, self.destination_folder = self.get_folders()
        self.email_sender = email_sender

    def get_folders(self) -> Tuple[str, str]:
        origin_folder = os.path.expanduser('~/Downloads')
        actual_date = datetime.datetime.now().strftime('%Y-%m-%d')
        destination_folder = os.path.join(os.path.expanduser('~/Documents'), f'check_{actual_date}')
        return origin_folder, destination_folder

    def create_folder_if_not_exists(self,folder: str) -> None:
        if not os.path.exists(folder):
            os.makedirs(folder)

    def move_item(self, item: str) -> Optional[str]:
        item_route = os.path.join(self.origin_folder, item)
        destination_item_route = os.path.join(self.destination_folder, item)
        if os.path.isfile(item_route) or os.path.isdir(item_route):
            shutil.move(item_route, destination_item_route)
            return item
        return None

    def move_files_and_folders(self) -> None: 
        self.create_folder_if_not_exists(self.destination_folder) 
        items = os.listdir(self.origin_folder) 
        moved_items = [] 
        for item in items: 
            moved_item = self.move_item(item)
            if moved_item: 
                moved_items.append(moved_item) 
        amount_items = len(moved_items) 
        self.email_sender.send_email_report(amount_items, moved_items, self.destination_folder)





