import fnmatch
import hashlib
import os
import re


INPUT_FOLDER = "Photos/180SampleFiles"
OUTPUT_FOLDER = "Photos/Output"


def process_file(file_path):

    file_name, file_extension = os.path.splitext(file_path)

    # Convert the file extension to lower case.
    file_extension = file_extension.lower()

    # Skip JSON files
    if file_extension == ".json":
        return

    # print(file_path,file_name,file_extension)

    print(file_name)


# Iterate through all non json files in the folder.
def iterate(folder_path):
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            process_file(file_name)


# Main function
def main():

    iterate(INPUT_FOLDER)


# Execute the main function
if __name__ == "__main__":
    exit_code = 0
    try:
        main()
    except Exception as e:
        print(e)
        exit_code = 1

    exit(exit_code)
