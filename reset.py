# import os
# import shutil
# 
# # Define the directories
# TARGET_DIR = "Photos\\Input"
# OUTPUT_DIR = "Photos\\Output"
# REJECT_FOLDER = "Photos\\Rejects"
# # TEMPLATE_DIR = "Photos\\SpecialCases1"
# TEMPLATE_DIR = "Photos\\PhotosFrom2018"
# 
# # Delete all files in input directory.
# for filename in os.listdir(TARGET_DIR):
#     file_path = os.path.join(TARGET_DIR, filename)
#     print("Deleting", file_path)
#     os.remove(file_path)
# 
# # Delete all the files in the output directory.
# for filename in os.listdir(OUTPUT_DIR):
#     file_path = os.path.join(OUTPUT_DIR, filename)
#     print("Deleting", file_path)
#     os.remove(file_path)
# 
# 
# # Delete all the files in the reject directory.
# for filename in os.listdir(REJECT_FOLDER):
#     file_path = os.path.join(REJECT_FOLDER, filename)
#     print("Deleting", file_path)
#     os.remove(file_path)
# 
# list_of_files = os.listdir(TEMPLATE_DIR)
# number_of_files = len(list_of_files)
# 
# # Copy all files from directory C to directory A
# for x, filename in enumerate(list_of_files):
# 
#     file_path = os.path.join(TEMPLATE_DIR, filename)
#     if os.path.isfile(file_path):
#         shutil.copy(
#             file_path, TARGET_DIR
#         )  # files only, directories are not copied
#         print(x, "/", number_of_files, "- Copying", file_path, "to", TARGET_DIR)
