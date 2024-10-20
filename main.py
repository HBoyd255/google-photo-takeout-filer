import os
import re


INPUT_FOLDER = "Photos\\180SampleFiles"
OUTPUT_FOLDER = "Photos\\Output"


def add_metadata(file_path, json_file):
    print("Adding metadata to", file_path, "from", json_file)


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
        add_metadata(file_path, json_file)
        
    else:
        # print("No JSON file for", file_path, ":", json_file)
        return 


# Iterate through all non json files in the folder.
def iterate(folder_path, function):
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            function(file_path)


# Main function
def main():

    iterate(INPUT_FOLDER, remove_live_photos)
    iterate(INPUT_FOLDER, perfect_match_json)


# Execute the main function
if __name__ == "__main__":
    exit_code = 0
    try:
        main()
    except Exception as e:
        print(e)
        exit_code = 1

    exit(exit_code)
