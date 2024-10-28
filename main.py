import datetime
import os
import re


from modules.json_manager import get_timestamp_from_json
INPUT_FOLDER = "Photos\\Input"
OUTPUT_FOLDER = "Photos\\Output"
REJECT_FOLDER = "Photos\\Rejects"


def fix_jpeg(file_path):

    paten_jpeg = r"\.jpeg"
    match_jpeg = re.search(paten_jpeg, file_path)

    if match_jpeg:

        new_file_path = re.sub(paten_jpeg, ".jpg", file_path)

        files_to_rename[file_path] = new_file_path

        return

    paten_jpe = r"\.jpe\."

    match_jpe = re.search(paten_jpe, file_path)

    if match_jpe:

        print(file_path)

        new_file_path = re.sub(paten_jpe, ".jpg.", file_path)

        files_to_rename[file_path] = new_file_path

        return

    paten_jp = r"\.jp\."
    match_jp = re.search(paten_jp, file_path)

    if match_jp:

        new_file_path = re.sub(paten_jp, ".jpg.", file_path)

        files_to_rename[file_path] = new_file_path
        return

    paten_double_dots = r"\.\."
    match_double_dots = re.search(paten_double_dots, file_path)

    if match_double_dots:

        new_file_path = re.sub(paten_double_dots, ".", file_path)

        files_to_rename[file_path] = new_file_path
        return


def process(file_path, json_file):

    timestamp = get_timestamp_from_json(json_file)

    # Get the file name and extension from the file path.
    file_extension = os.path.splitext(file_path)[-1].lower()

    offset = 0

    # This is a hacky way to handle duplicate timestamps.
    while offset < 1000:

        if offset != 0:
            print("trying offset", offset)

        new_base_name = datetime.datetime.fromtimestamp(timestamp).strftime(
            "%Y%m%d_%H%M%S"
        )

        if offset != 0:
            new_base_name += f"-{offset}"

        new_file_name = new_base_name + file_extension
        new_file_path = os.path.join(OUTPUT_FOLDER, new_file_name)

        if not os.path.exists(new_file_path):
            os.utime(file_path, (timestamp, timestamp))
            os.rename(file_path, new_file_path)
            os.remove(json_file)
            return

        offset += 1


# Look for a corresponding json file.
def calculate_json_file_name(file_path):

    base_name, extension = os.path.splitext(file_path)

    json_file_with_ext = base_name + extension + ".json"
    json_file_without_ext = base_name + ".json"
    dupe_not_moved = json_file_with_ext

    pattern = r"\(\d+\)"  # Matches a digit or more between brackets
    match = re.search(pattern, file_path)
    if match:
        dupe_indicator = match.group(0)
        with_no_dupe = re.sub(pattern, "", file_path)
        json_file_with_ext = with_no_dupe + dupe_indicator + ".json"

    return json_file_with_ext, json_file_without_ext, dupe_not_moved


def find_files_to_rename_supplemental_metadata(file_path):

    base_name, extension = os.path.splitext(file_path)

    # Only process json files.
    if extension != ".json":
        return

    target_key = "supplemental-metadata"

    replacement_pattern_dupe = r"(\1).json"
    replacement_pattern_no_dupe = r".json"

    for x in range(len(target_key)):

        part_target_key = target_key[:-x]

        if x == 0:
            part_target_key = target_key

        pattern_dupe = rf"\.{part_target_key}\((\d+)\)\.json"
        pattern_no_dupe = rf"\.{part_target_key}.json"

        match_dupe = re.search(pattern_dupe, file_path)
        match_no_dupe = re.search(pattern_no_dupe, file_path)

        if match_dupe:

            new_file_path = re.sub(
                pattern_dupe, replacement_pattern_dupe, file_path
            )

            files_to_rename[file_path] = new_file_path

        if match_no_dupe:
            new_file_path = re.sub(
                pattern_no_dupe, replacement_pattern_no_dupe, file_path
            )

            files_to_rename[file_path] = new_file_path


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

    # This function is only for .mp4 and .MP files.
    if file_extension != ".mp4" and file_extension != ".mp":
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

    # At one point Google Pixel decided to attempt to replicate Live Photos.
    # The formatting for the video element is filename.MP, and the Image is
    # filename.MP.jpg.

    google_pixel_live_photo = file_base + ".MP.jpg"

    if os.path.exists(google_pixel_live_photo):
        if os.path.exists(file_path):
            os.remove(file_path)
        print("Removing", file_path)


def replace_with_edited(file_path):

    edited_pattern = r"-edited."

    match = re.search(edited_pattern, file_path)

    if not match:
        return

    non_edited_file = re.sub(edited_pattern, ".", file_path)

    if os.path.exists(non_edited_file):
        files_to_replace[file_path] = non_edited_file


def perfect_match_json(file_path):

    # Get the file name and extension from the file path.
    file_base, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # Skip JSON files
    if file_extension == ".json":
        return

    json_file, json_file_no_extension, dupe_not_moved = (
        calculate_json_file_name(file_path)
    )

    if os.path.exists(json_file):
        process(file_path, json_file)

    elif os.path.exists(json_file_no_extension):
        process(file_path, json_file_no_extension)

    elif os.path.exists(dupe_not_moved):
        process(file_path, dupe_not_moved)


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


# The key is the file name, the value is the new file name.
files_to_rename = {}

# The key source, the value is the destination.
files_to_replace = {}


# Main function
def main():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if not os.path.exists(REJECT_FOLDER):
        os.makedirs(REJECT_FOLDER)

    print("Removing extensionless files")
    # Remove all files that do not have an extension.
    iterate(INPUT_FOLDER, separate_extensionless_files)

    print('Removing ".supplemental-metadata"')
    # Find all files that would match a neighboring file if they had one less
    # character in the base name.
    iterate(INPUT_FOLDER, find_files_to_rename_supplemental_metadata)

    # Rename the files.
    for old_file, new_file in files_to_rename.items():
        print("Renaming", old_file, "->", new_file)
        os.rename(old_file, new_file)

    # Merge edited photos
    print("Finding files to replace")
    # Find all files that would match a neighboring file if they had one less
    # character in the base name.
    iterate(INPUT_FOLDER, replace_with_edited)

    for src, dest in files_to_replace.items():

        print("Replacing", src, "->", dest)
        os.remove(dest)
        os.rename(src, dest)

    files_to_rename.clear()

    print("Finding files to fix JPEG")
    # Find all files that would match a neighboring file if they had one less
    # character in the base name.
    iterate(INPUT_FOLDER, fix_jpeg)

    # Rename the files.
    for old_file, new_file in files_to_rename.items():
        print("Renaming", old_file, "->", new_file)
        os.rename(old_file, new_file)

    iterate(INPUT_FOLDER, remove_live_photos)

    iterate(INPUT_FOLDER, perfect_match_json)

    files_to_rename.clear()

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

# Screenshot_20210108-184857 (1).png
