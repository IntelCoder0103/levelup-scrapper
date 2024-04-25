import config
import os
import glob
import shutil
import time

def wait_for_download():
    download_directory = config.download_directory
    timeout = config.download_timeout

    while timeout > 0:
        if any(filename.endswith(".crdownload") for filename in os.listdir(download_directory)):
            time.sleep(1)
            timeout -= 1
        else:
            break
    pass

def wait_for_save_pdf():
    download_directory = config.download_directory
    timeout = config.download_timeout

    while timeout > 0:
        if any(filename.endswith(".pdf") for filename in os.listdir(download_directory)):
            break
        else:
            time.sleep(1)
            timeout -= 1
    pass

def save_downloaded_document(name: str, subdirectory: str = ''):
    download_directory = config.download_directory
    save_directory = config.save_directory + '/' + subdirectory

    # Create the save directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Move the downloaded file (not directory) to the save directory
    files = glob.glob(download_directory + '/*')
    for f in files:
        if os.path.isfile(f):
            file = f
            ext = file.split('.')[-1]
            shutil.move(file, save_directory + '/' + name + '.' + ext)

    pass