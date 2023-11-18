import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image

directory_path = "W:\photographs"


def yearfiles():
#check is the directory existent and create it if not
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

#create mutiple files in the specied directory

    for year in range(2002, 2025):
        year_directory = os.path.join(directory_path, str(year))

    #check if the year directory existed, and create it if not
    if not os.path.exists(year_directory):
        os.makedirs(year_directory)


def get_creation_year(file_path):
     try:
         with Image.open(file_path) as img:
             exif_data = img._getexif()
             if exif_data is not None and 36867 in exif_data:
                 # Extract the creation date (format: 'YYYY:MM:DD HH:MM:SS')
                 date_str = exif_data[36867]
                 year = int(date_str.split(':')[0])
                 return year
     except Exception as e:
         print(f"Error extracting creation year from {file_path}: {e}")
     return None

def get_creation_year(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data is not None and 36867 in exif_data:
                # Extract the creation date (format: 'YYYY:MM:DD HH:MM:SS')
                date_str = exif_data[36867]
                year = int(date_str.split(':')[0])
                return year
    except Exception as e:
        print(f"Error extracting creation year from {file_path}: {e}")
    return None

def sort_files(source_directory, target_directory):
    # Check if the target directory exists, and create it if not
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Create an "Unsorted" directory within the target directory
    unsorted_directory = os.path.join(target_directory, "Unsorted")
    if not os.path.exists(unsorted_directory):
        os.makedirs(unsorted_directory)

    # Keep track of moved files to avoid duplicates
    moved_files = set()

    # Recursively iterate through files in the source directory and subdirectories
    for root, _, files in os.walk(source_directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if the file is an image or video
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.img', '.heic']
            video_extensions = ['.mov', '.mp4', '.avi', '.mkv']

            if any(filename.lower().endswith(ext) for ext in image_extensions + video_extensions):
                # Get the creation year from the photo/video metadata
                if any(filename.lower().endswith(ext) for ext in image_extensions):
                    year = get_creation_year(file_path)
                else:
                    year = None  # For videos, we won't use creation year

                # Create a target directory based on the year (if available) or "Videos" for videos
                target_subdirectory = os.path.join(target_directory, str(year) if year is not None else "Videos")

                # Check if the target subdirectory exists, and create it if not
                if not os.path.exists(target_subdirectory):
                    os.makedirs(target_subdirectory)

                # Check if the file is not a duplicate
                if filename not in moved_files:
                    # Move the file to the target subdirectory
                    target_path = os.path.join(target_subdirectory, filename)
                    shutil.move(file_path, target_path)
                    print(f"Moved {filename} to {target_subdirectory}")

                    # Add the moved file to the set to avoid duplicates
                    moved_files.add(filename)
                else:
                    print(f"Skipped duplicate file: {filename}")
            else:
                # For unrecognized file types, move them to the "Unsorted" directory
                target_path = os.path.join(unsorted_directory, filename)
                shutil.move(file_path, target_path)
                print(f"Moved unrecognized file {filename} to {unsorted_directory}")

# Create a simple GUI
root = tk.Tk()
root.withdraw()  # Hide the main window

# Ask the user to select the source directory
source_directory = filedialog.askdirectory(title="Select Source Directory")
if not source_directory:
    print("Source directory selection canceled.")
else:
    # Set the target directory
    target_directory = "W:/photographs"

    # Call the function to sort files
    sort_files(source_directory, target_directory)


























































