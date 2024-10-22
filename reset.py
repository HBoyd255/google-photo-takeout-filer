import os
import shutil

# Define the directories
TARGET_DIR = "Photos\\Input"
OUTPUT_DIR = "Photos\\Output"
REJECT_FOLDER = "Photos\\Rejects"
# TEMPLATE_DIR = "Photos\\SpecialCasesC"
TEMPLATE_DIR = "Photos\\GooglePhotosFrom2023"

# Delete all files in input directory.
for filename in os.listdir(TARGET_DIR):
    file_path = os.path.join(TARGET_DIR, filename)
    print("Deleting", file_path)
    os.remove(file_path)

# Delete all the files in the output directory.
for filename in os.listdir(OUTPUT_DIR):
    file_path = os.path.join(OUTPUT_DIR, filename)
    print("Deleting", file_path)
    os.remove(file_path)


# Delete all the files in the reject directory.
for filename in os.listdir(REJECT_FOLDER):
    file_path = os.path.join(REJECT_FOLDER, filename)
    print("Deleting", file_path)
    os.remove(file_path)

# Copy all files from directory C to directory A
for filename in os.listdir(TEMPLATE_DIR):
    file_path = os.path.join(TEMPLATE_DIR, filename)
    if os.path.isfile(file_path):
        shutil.copy(
            file_path, TARGET_DIR
        )  # files only, directories are not copied
        print("Copying", file_path, "to", TARGET_DIR)
