import os
import re
import shutil

def move_files(source_directory, destination_directory, pattern):
    # Compile the regex pattern
    regex = re.compile(pattern)

    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            # Check if the file does not match the pattern
            if not regex.match(file_name):
                # Construct the full path of the file
                file_path = os.path.join(root, file_name)
                # Construct the destination path
                destination_path = os.path.join(destination_directory, file_name)

                # Handle possible name collision in the destination directory
                counter = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(destination_directory, f"{file_name[:-4]}_{counter}{file_name[-4:]}")
                    counter += 1

                # Move the file
                shutil.move(file_path, destination_path)
                print(f"Moved: {file_path} -> {destination_path}")

# Source directory to search
source_directory = '/Users/miethe/Downloads/browser-logos-74.0.0/src/node.js'

# Destination directory to move files
destination_directory = '/Users/miethe/dev/openshift-practice/logos/SVG-Logos/Browsers'

# Regex pattern to match files that should not be moved
pattern = r'[0-9]x[0-9]\.png'

# Call the function to move files
move_files(source_directory, destination_directory, pattern)
