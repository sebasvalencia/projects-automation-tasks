import os
import datetime
import shutil
import pytest
from unittest.mock import patch, MagicMock

from src.move_download_files import MoveItems
from src.email_sender import EmailSender

@pytest.fixture
def setup_files():
    os.makedirs('./test_downloads', exist_ok=True)
    os.makedirs('./test_documents/check_2024-12-16', exist_ok=True)
    
    with open(os.path.join('./test_downloads', 'test_file.txt'), 'w') as f:
        f.write('This is a test file.')

    yield

    shutil.rmtree('./test_downloads', ignore_errors=True)
    shutil.rmtree('./test_documents/check_2024-12-16', ignore_errors=True)

@pytest.fixture
def email_sender():
    return MagicMock()

@pytest.fixture
def move_items(email_sender):
    move_items = MoveItems(email_sender)
    move_items.origin_folder = './test_downloads'
    move_items.destination_folder = './test_documents/check_2024-12-16'
    return move_items

def test_get_folders(move_items): 
    origin, destination = move_items.get_folders() 
    assert origin.endswith('Downloads') 
    expected_destination_suffix = f'check_{datetime.datetime.now().strftime("%Y-%m-%d")}' 
    assert os.path.normpath(destination).endswith(os.path.join('Documents', expected_destination_suffix))

@patch('os.path.exists', return_value=True)
def test_create_folder_if_not_exists_folder_exists(mock_exists, move_items):
    move_items.create_folder_if_not_exists('/path/to/folder')
    mock_exists.assert_called_once_with('/path/to/folder')

@patch('os.path.exists', return_value=False)
@patch('os.makedirs')
def test_create_folder_if_not_exists_creates_folder(mock_makedirs, mock_exists, move_items):
    move_items.create_folder_if_not_exists('/path/to/new/folder')
    mock_exists.assert_called_once_with('/path/to/new/folder')
    mock_makedirs.assert_called_once_with('/path/to/new/folder')

@patch('shutil.move')
@patch('os.path.isfile', return_value=True)
def test_move_item_file(mock_isfile, mock_move, move_items, setup_files):
    item = 'test_file.txt'
    moved_item = move_items.move_item(item)
    assert moved_item == item
    mock_move.assert_called_once_with(
        os.path.join(move_items.origin_folder, item),
        os.path.join(move_items.destination_folder, item)
    )

@patch('shutil.move')
@patch('os.path.isdir', return_value=True)
def test_move_item_folder(mock_isdir, mock_move, move_items, setup_files):
    os.makedirs('./test_downloads/test_folder', exist_ok=True)
    item = 'test_folder'
    moved_item = move_items.move_item(item)
    assert moved_item == item
    mock_move.assert_called_once_with(
        os.path.join(move_items.origin_folder, item),
        os.path.join(move_items.destination_folder, item)
    )

@patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
@patch.object(MoveItems, 'move_item', side_effect=lambda item: item)
def test_move_files_and_folders(mock_move_item, mock_listdir, move_items):
    move_items.move_files_and_folders()
    mock_listdir.assert_called_once_with(move_items.origin_folder)
    assert mock_move_item.call_count == 2
    move_items.email_sender.send_email_report.assert_called_once_with(
        2,
        ['file1.txt', 'file2.txt'],
        move_items.destination_folder
    )
