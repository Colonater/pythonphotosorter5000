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

def sort_photos():
    # Ask the user to select the source directory
    source_directory = filedialog.askdirectory(title="Select Source Directory")
    if not source_directory:
        print("Source directory selection canceled.")
        return
    
    # Set the target directory
    target_directory = "W:/photographs"

    # Check if the target directory exists, and create it if not
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Iterate through files in the source directory
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        
        # Check if the file is an image (you can add more extensions if needed)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.img', '.heic']
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            # Get the creation year from the photo metadata
            year = get_creation_year(file_path)
            
            if year is not None:
                # Create a target directory based on the year
                target_subdirectory = os.path.join(target_directory, str(year))
                
                # Check if the target subdirectory exists, and create it if not
                if not os.path.exists(target_subdirectory):
                    os.makedirs(target_subdirectory)
                
                # Move the file to the target subdirectory
                target_path = os.path.join(target_subdirectory, filename)
                shutil.move(file_path, target_path)
                print(f"Moved {filename} to {target_subdirectory}")

# Create a simple GUI
root = tk.Tk()
root.withdraw()  # Hide the main window

# Call the function when the GUI is running
sort_photos()





















































