import os
import re
import shutil
#audit_logos(source_directory)
from os.path import split

SVG_STRING = ".svg"
SVG_DESTINATION_DIRECTORY = "/Users/miethe/Downloads/cncf-svg"
#PNG_DESTINATION_DIRECTORY = "/Users/miethe/dev/openshift-practice/logos/PNG-Logos/App Frameworks, Language, IDE/Languages"

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
    file_name = cleanup_filename(file_name)
    return os.path.join(destination_directory, file_name)

def cleanup_filename(file_name):
    #file_name = replace_text(file_name, '_', '')
    file_name = remove_extra_filepaths(file_name)
    if '_' in file_name:
        file_name = file_name.split('_')[1]

    return file_name

def remove_extra_filepaths(file_name):
    file_name_pieces = file_name.split('.')
    return file_name_pieces[0]+'.svg'

def replace_text(file_name, replace, replacing=''):
    return file_name.replace(replace, replacing)

def handle_name_collision(file_name, destination_path, destination_directory):
    # Handle possible name collision in the destination directory
    counter = 1
    while os.path.exists(destination_path):
        destination_path = os.path.join(destination_directory, f"{file_name[:-4]}_{counter}{file_name[-4:]}")
        counter += 1
    return destination_path

def move_files(source_directory, pattern, destination_directory):
    if not os.path.exists(source_directory):
        return
    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            # Check if the file does not match the pattern
            destination_path = get_full_path(file_name, pattern, destination_directory)
            if not destination_path:
                continue
            file_path = os.path.join(root, file_name)

            destination_path = handle_name_collision(file_name, destination_path, destination_directory)

            # Move the file
            shutil.move(file_path, destination_path)
            print(f"Moved: {file_name} -> {destination_path}")

def rename_files(root_path:str, patterns:list, replacements:list):
    """
    Recursively rename files based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    patterns (list): List of strs to match file names.
    replacements (list): List of replacement strings to rename files.
    """
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            replacement_index = 0
            new_file_name = file_name
            for pattern in patterns:
                if pattern in file_name:
                    new_file_name = replace_text(new_file_name, pattern, replacements[replacement_index])
                replacement_index+=1

            # If file changed, rename
            if new_file_name != file_name:
                src = os.path.join(root, file_name)
                dest = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(src, dest)
                print(f"Renamed: {file_name} -> {new_file_name}")

def rename_files_split(root_path:str, patterns:list, split_indices:list):
    """
    Recursively rename files based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    patterns (list): List of strs to split file names.
    split_indices (list): List of indices to keep after split.
    """
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            split_index = 0
            new_file_name = file_name
            for pattern in patterns:
                if pattern in file_name:
                    new_file_name = new_file_name.split(pattern)[split_indices[split_index]]
                split_index+=1

            # If file changed, rename
            if new_file_name != file_name:
                src = os.path.join(root, file_name)
                dest = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(src, dest)
                print(f"Renamed: {file_name} -> {new_file_name}")

def add_filepath(root_path, filepath):
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if filepath not in file_name:
                new_file_name = file_name + filepath

                src = os.path.join(root, file_name)
                dest = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(src, dest)
                print(f"Renamed: {file_name} -> {new_file_name}")

def rename_dirs(root_path, pattern, replacement=''):
    """
    Recursively rename directories based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    pattern (str): Regular expression pattern to match directory names.
    replacement (str): The replacement string to rename directories.
    """
    for root, dirs, _ in os.walk(root_path):
        for dir_name in dirs:
            if pattern in dir_name:
                new_dir_name = replace_text(dir_name, pattern, replacement)
                src = os.path.join(root, dir_name)
                dest = os.path.join(root, new_dir_name)

                # Rename the directory
                os.rename(src, dest)
                print(f"Renamed directory: {dir_name} -> {new_dir_name}")

def remove_files(root_path, pattern):
    """
    Recursively remove files based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    pattern (str): Regular expression pattern to match file names.
    """
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if pattern in file_name:
                file_path = os.path.join(root, file_name)

                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_name}")

def remove_files_except(root_path, pattern):
    """
    Recursively remove files based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    pattern (str): Regular expression pattern to match file names.
    """
    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            if pattern not in file_name:
                file_path = os.path.join(root, file_name)

                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_name}")

def remove_dirs(root_path, pattern):
    """
    Recursively remove files based on a specific pattern.

    Parameters:
    root_path (str): The root directory to start scanning.
    pattern (str): Regular expression pattern to match file names.
    """
    for root, dirs, _ in os.walk(root_path):
        for dir_name in dirs:
            if pattern not in dir_name:
                dir_path = os.path.join(root, dir_name)

                # Remove the file
                #os.rmdir(dir_path)
                # Recursively remove
                shutil.rmtree(dir_path)
                print(f"Removed: {dir_name}")

def audit_logos(source_directory):
    if not os.path.exists(source_directory):
        return

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_directory):
        for file_name in files:
            try:
                logo_name = file_name.split(".")[0]
                print(f"{logo_name},", end =" ")
            except:
                continue

# Source directory to search
source_directory = '/Users/miethe/Downloads/cncf-artwork-master'

# Regex pattern to match files that should not be moved
#pngImagePattern = r"[0-9]*x[0-9]*\.png"

# Call the function to move files
move_files(source_directory, SVG_STRING, SVG_DESTINATION_DIRECTORY)
#rename_files_split(source_directory, ['_', '.'], [1,0])
#add_filepath(source_directory, ".svg")
#remove_files_except(source_directory, ".svg")
#rename_files(source_directory, ["Arch_","_64"], ['',''])
#remove_dirs(source_directory, "Arch")
#rename_dirs(source_directory, "Res_48_")
