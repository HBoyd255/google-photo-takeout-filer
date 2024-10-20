# Google Photos Takeout Filer

This program organizes your photos from a Google Photos takeout export and
arranges them into east to navigate folders 

To achieve this it:
* Extracts the capture date from each photo's accompanying JSON file and
applies it to the metadata of the photo.
* Renames each photo to better reflect the capture date.
* Sorts each photo into a folder based on the month that it was captured.
