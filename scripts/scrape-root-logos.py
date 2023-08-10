import os
import re
import shutil

SVG_STRING = ".svg"
SVG_DESTINATION_DIRECTORY = "/Users/miethe/dev/openshift-practice/logos/SVG-Logos/App Frameworks, Language, IDE/Languages"
PNG_DESTINATION_DIRECTORY = "/Users/miethe/dev/openshift-practice/logos/PNG-Logos/App Frameworks, Language, IDE/Languages"

def get_full_path_regex(file_name, regex, dest_dir, secondary_flag=None, secondary_dir=None):
    if not regex.search(file_name):
        # Construct the full path of the file
        # Construct the destination path
        if secondary_flag and secondary_flag in file_name:
            destination_directory = secondary_dir
        else:
            destination_directory = dest_dir

        return os.path.join(destination_directory, file_name)

def get_full_path(file_name, pattern, dest_dir, secondary_flag=None, secondary_dir=None):
    if pattern in file_name:
        # Construct the full path of the file
        # Construct the destination path
        if secondary_flag and secondary_flag in file_name:
            destination_directory = secondary_dir
        else:
            destination_directory = dest_dir
    else:
        return None
    return os.path.join(destination_directory, file_name)

def move_files(source_directory, pattern, destination_directory):
    # Compile the regex pattern
    #regex = re.compile(pattern)
    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            # Check if the file does not match the pattern
            destination_path = get_full_path(file_name, pattern, destination_directory)
            file_path = os.path.join(root, file_name)
            if not destination_path:
                continue

            # Handle possible name collision in the destination directory
            counter = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(destination_directory, f"{file_name[:-4]}_{counter}{file_name[-4:]}")
                counter += 1

            # Move the file
            shutil.move(file_path, destination_path)
            print(f"Moved: {file_path} -> {destination_path}")

# Source directory to search
source_directory = '/Users/miethe/Downloads/abrahamcalf'

# Regex pattern to match files that should not be moved
#pngImagePattern = r"[0-9]*x[0-9]*\.png"

# Call the function to move files
move_files(source_directory, SVG_STRING, SVG_DESTINATION_DIRECTORY)
