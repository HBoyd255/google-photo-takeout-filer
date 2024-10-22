import datetime
import os
import re

from modules.json_manager import get_timestamp_from_json

INPUT_FOLDER = "Photos\\Input"
OUTPUT_FOLDER = "Photos\\Output"
REJECT_FOLDER = "Photos\\Rejects"


def process(file_path, json_file):

    timestamp = get_timestamp_from_json(json_file)

    # Get the file name and extension from the file path.
    file_extension = os.path.splitext(file_path)[-1].lower()

    offset = 0

    # This is a hacky way to handle duplicate timestamps.
    while offset < 100:

        if offset != 0:
            print("trying offset", offset)

        new_timestamp = timestamp + offset

        new_base_name = datetime.datetime.fromtimestamp(new_timestamp).strftime(
            "%Y%m%d_%H%M%S"
        )
        new_file_name = new_base_name + file_extension
        new_file_path = os.path.join(OUTPUT_FOLDER, new_file_name)

        if not os.path.exists(new_file_path):
            os.utime(file_path, (new_timestamp, new_timestamp))
            os.rename(file_path, new_file_path)
            os.remove(json_file)

            return

        offset += 1

    print("Capped out at", file_path)


# Look for a corresponding json file.
def calculate_json_file_name(file_path):

    base_name, extension = os.path.splitext(file_path)

    json_file_with_ext = base_name + extension + ".json"
    json_file_without_ext = base_name + ".json"

    pattern = r"\(\d+\)"  # Matches a digit or more between brackets
    match = re.search(pattern, file_path)
    if match:
        dupe_indicator = match.group(0)
        with_no_dupe = re.sub(pattern, "", file_path)
        json_file_with_ext = with_no_dupe + dupe_indicator + ".json"

    return json_file_with_ext, json_file_without_ext


# The key is the file name, the value is the new file name.
files_to_rename = {}


def compare_files(file_a, file_b):
    # print("Comparing", file_a, "to", file_b)

    file_a_base, file_a_extension = os.path.splitext(file_a)
    file_b_base, file_b_extension = os.path.splitext(file_b)

    # If file_b would be a match, if it had one less character in the base name.
    if file_a_base == file_b_base[:-1]:
        # print("Match found", file_a, file_b)
        new_file_b_path = file_a_base + file_b_extension
        files_to_rename[file_b] = new_file_b_path


def find_files_to_rename(file_path):

    # I hate this, its O(n^2) but I blame Google Photos for throwing extra
    # characters onto random file names.

    file = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)

    # Iterate through all files in the folder
    for root, dirs, other_files in os.walk(folder_path):

        for other_file in other_files:
            if other_file == file:
                continue

            other_file_path = os.path.join(root, other_file)

            compare_files(file_path, other_file_path)


def separate_extensionless_files(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    file_name = file_base.split("\\")[-1]

    if file_extension == "":

        new_base = "NO_EXT-" + file_name
        new_path = os.path.join(REJECT_FOLDER, new_base)
        os.rename(file_path, new_path)


def remove_live_photos(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # If the file is a mp4 file, and has a corresponding heic file, then it is
    # a "live photo" and should be removed.
    if file_extension != ".mp4":
        return

    if os.path.exists(file_base + ".HEIC") or os.path.exists(
        file_base + ".JPG"
    ):
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Removing", file_path)

    for x in range(1, 10):
        if file_base[-3:] == "(" + str(x) + ")":
            og_file_base = file_base[:-3]
            if os.path.exists(og_file_base + ".HEIC") or os.path.exists(
                og_file_base + ".JPG"
            ):
                if os.path.exists(file_path):
                    os.remove(file_path)
                print("Removing", file_path)


def perfect_match_json(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # Skip JSON files
    if file_extension == ".json":
        return

    json_file, json_file_no_extension = calculate_json_file_name(file_path)

    if os.path.exists(json_file):
        process(file_path, json_file)

    elif os.path.exists(json_file_no_extension):
        process(file_path, json_file_no_extension)


# Iterate through all non json files in the folder.
def iterate(folder_path, function):
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):

        num_files = len(files)

        for x, file_name in enumerate(files):

            file_path = os.path.join(root, file_name)

            print(
                x, "/", num_files, "running", function.__name__, "on", file_path
            )
            function(file_path)


# Main function
def main():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if not os.path.exists(REJECT_FOLDER):
        os.makedirs(REJECT_FOLDER)

    print("Removing extensionless files")
    # Remove all files that do not have an extension.
    iterate(INPUT_FOLDER, separate_extensionless_files)

    print("Finding any files with an extra character")
    # Find all files that would match a neighboring file if they had one less
    # character in the base name.
    iterate(INPUT_FOLDER, find_files_to_rename)

    print("Renaming files")
    # Rename the files.
    for old_file, new_file in files_to_rename.items():
        print("Renaming", old_file, "->", new_file)
        os.rename(old_file, new_file)

    iterate(INPUT_FOLDER, remove_live_photos)

    iterate(INPUT_FOLDER, perfect_match_json)


# Execute the main function
if __name__ == "__main__":

    main()
