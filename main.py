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

    while offset < 10:

        if offset != 0:
            print("tyring offset", offset)

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

            break

        offset += 1

    if offset != 0:
        print("Capped out at", file_path)


# Look for a corresponding json file.
def calculate_json_file_name(file_path):
    json_file = file_path + ".json"

    pattern = r"\(\d+\)"  # Matches a digit or more between brackets
    match = re.search(pattern, file_path)
    if match:
        dupe_indicator = match.group(0)
        with_no_dupe = re.sub(pattern, "", file_path)
        json_file = with_no_dupe + dupe_indicator + ".json"

    return json_file


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
    if file_extension == ".mp4" and os.path.exists(file_base + ".HEIC"):
        os.remove(file_path)
        print("Removing", file_path)
        return


def perfect_match_json(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # Skip JSON files
    if file_extension == ".json":
        return

    json_file = calculate_json_file_name(file_path)

    if os.path.exists(json_file):

        print(file_path)

        process(file_path, json_file)

    else:
        print("JSON file not found: ", json_file)


def fuzzy_match_json(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # Skip JSON files
    if file_extension == ".json":
        return
    # IMG_0410.MP4
    json_file = calculate_json_file_name(file_path)

    if os.path.exists(json_file):

        print(file_path)

        process(file_path, json_file)

    else:
        print("JSON file not found: ", json_file)


# Iterate through all non json files in the folder.
def iterate(folder_path, function):
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            function(file_path)


# Main function
def main():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if not os.path.exists(REJECT_FOLDER):
        os.makedirs(REJECT_FOLDER)

    # iterate(INPUT_FOLDER, separate_extensionless_files)

    # iterate(INPUT_FOLDER, remove_live_photos)

    # iterate(INPUT_FOLDER, perfect_match_json)


# Execute the main function
if __name__ == "__main__":

    main()
