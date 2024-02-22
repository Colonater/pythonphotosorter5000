import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ExifTags
import hashlib

directory_path = "W:\photographs"



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
                # Extract the creation date (format: 'YYYY:MM:DD HH:MM:SS')
                date_str = exif_data[36867]
    except IOError:
        print(f"Cannot open file {file_path}. Unsupported file type.")

def get_file_hash(file_path):
    # Use the SHA256 hash function
    hasher = hashlib.sha256()

    # Read the file in binary mode and update the hash
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)

    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()

def handle_duplicates(file_path, hash_to_path):
    # Get the hash of the file
    file_hash = get_file_hash(file_path)

    # If the hash is already in the dictionary, then it's a duplicate
    if file_hash in hash_to_path:
        duplicate_path = os.path.join(directory_path, 'duplicates')
        if not os.path.exists(duplicate_path):
            os.makedirs(duplicate_path)
        shutil.move(file_path, duplicate_path)
    else:
        # Otherwise, add the hash and file path to the dictionary
        hash_to_path[file_hash] = file_path

def main():
    yearfiles()
    hash_to_path = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            handle_duplicates(file_path, hash_to_path)

if __name__ == "__main__":
    main()



























































