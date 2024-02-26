import os
import shutil
import hashlib
import logging
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ExifTags
from concurrent.futures import ThreadPoolExecutor
import threading


# Using double backslashes
directory_path = "\\\\shedpc\\w\\photographs"



# Set up logging
logging.basicConfig(filename='photo_sorter.log', level=logging.INFO)

def yearfiles():
    # check is the directory existent and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # create multiple files in the specified directory
    for year in range(2002, 2025):
        year_directory = os.path.join(directory_path, str(year))

        # check if the year directory existed, and create it if not
        if not os.path.exists(year_directory):
            os.makedirs(year_directory)

def get_creation_year(file_path):
    # .THM - Thumbnail image file
    # .DSC - Image file created by Nikon digital cameras
    # .AAE - Sidecar file created by Apple's Photos app
    # .NEF - Nikon Electronic Format RAW image file
    # .MTS - AVCHD video file

    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data is not None and 36867 in exif_data:
                date_str = exif_data[36867]
                return date_str[:4]
    except IOError:
        logging.error(f"Cannot open file {file_path}. Unsupported file type.")

# Create a set to store the hashes of processed files
processed_files = set()

def get_file_hash(file_path):
    # Use the SHA256 hash function
    hasher = hashlib.sha256()

    # Read the file in binary mode and update the hash
    with open(file_path, 'rb') as file:
        for block in iter(lambda: file.read(4096), b""):
            hasher.update(block)

    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()


# Create a semaphore with a maximum of 20 concurrent downloads
download_semaphore = threading.Semaphore(20)

# Create a lock for accessing processed_files
processed_files_lock = threading.Lock()

def sort_and_remove_duplicates(file_paths, directory_path, operation, progress_bar, status_label):
    progress_bar['maximum'] = len(file_paths)

    with ThreadPoolExecutor() as executor:
        for file_path in file_paths:
            status_label['text'] = f"Processing file: {file_path}"
            executor.submit(handle_duplicates, file_path, directory_path, operation)
            progress_bar['value'] += 1
            progress_bar.update()

def handle_duplicates(file_path, directory_path, operation):
    try:
        # Attempt to acquire the semaphore
        with download_semaphore:
            # Attempt to open and close the file to trigger iCloud Drive to download it
            with open(file_path, 'rb'):
                pass

        # Calculate the file's hash
        file_hash = get_file_hash(file_path)

        # Use the lock when accessing processed_files
        with processed_files_lock:
            # If the file's hash is in the set of processed file hashes, skip the file
            if file_hash in processed_files:
                return

            # Add the file's hash to the set of processed file hashes
            processed_files.add(file_hash)

        year = get_creation_year(file_path)
        if year is not None:
            year_directory = os.path.join(directory_path, year)
            if not os.path.exists(year_directory):
                os.makedirs(year_directory)
            if operation == 'copy':
                shutil.copy(file_path, os.path.join(year_directory, os.path.basename(file_path)))
            else:
                shutil.move(file_path, os.path.join(year_directory, os.path.basename(file_path)))
    except Exception as e:
        logging.error(f"Error handling file {file_path}: {e}")

def create_gui():
    root = tk.Tk()

    directory_path = tk.StringVar(root)
    operation = tk.StringVar(root, 'copy')

    file_picker_button = tk.Button(root, text="Select files", command=lambda: directory_path.set(filedialog.askopenfilenames()))
    file_picker_button.pack()

    operation_radio_copy = tk.Radiobutton(root, text="Copy", variable=operation, value='copy')
    operation_radio_copy.pack()

    operation_radio_move = tk.Radiobutton(root, text="Move", variable=operation, value='move')
    operation_radio_move.pack()

    progress_bar = ttk.Progressbar(root, length=100, mode='determinate')
    progress_bar.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    button = tk.Button(root, text="Sort and remove duplicates", command=lambda: sort_and_remove_duplicates(directory_path.get(), operation.get(), progress_bar, status_label))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()




















