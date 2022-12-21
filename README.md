# Heiya

> **A one-line solution for photographers to simply convert JPEG into High Efficiency Image (AVIF/HEIC) and preserve all the metadata.**

## Website
The official website of Heiya has been launched!!!!! Visit the website [here](https://heiya.hongjunwu.com/) for everything about it.

## Announcement
Heiya is iterating quickly under active development. 
Function calls and arguments will change, so please keep your version updated and refer to the newest examples in the documentation.

## Introduction
Heiya allows you to easily translate between JPG/TIFF and AVIF/HEIC, without losing image metadata such as geotag and lens information. All the common operations can be done using one line of code.

It is developed for photographers with a storage budget (like myself, lol) to build an automatic and efficient image storage pipeline.

***

JPEG was invented six years before my existence.
I'm now 24, graduating from my double Master's degree next summer.

And yet, the majority of cameras in the current age still shoot JPEG.

AVIF and HEIC are what are called "High-Efficiency Images" (You can read about them here: [AVIF vs HEIC](https://www.winxdvd.com/ios-android-mobile/avif-vs-heic.htm)). 
* These are the future of media formats, JPEG is getting deprecated.
* They can result in a file size of as much as 100x less than traditional JPEGs.
* Devices and operating systems now have good support for both formats.
* However, there are no free and easy-to-use tools out there to simply encode all the JPEGs my camera took into AVIFs while preserving metadata.

## Install Heiya from PyPI
Heiya is developed and tested on macOS and hasn't been tested on Linux, it doesn't support Windows for now.
  
```python
pip install heiya
```

## Examples
```python
"""
JPG to HEIF/AVIF
Convert JPG shoot by camera to High Efficiency Images with metadata to import to iCloud photo library.
Find this notebook in https://github.com/wu-hongjun/heiya/blob/main/jpg_hei.ipynb

How To:
Step 1: Run "pip install heiya" from Terminal (If you have not already done so).
Step 2: Copy the folder directory where all the JPGs are stored.
    Windows: File Explorer -> Go to your target folder -> Single Click address bar -> Copy the file path in address bar.
    macOS: Finder -> Go to your target folder -> Hold Alt (File path should apper in bottom left) -> Right click on folder and copy file path.
Step 3: Run this cell and wait for it to finish, it will print out progress below.
"""

import heiya
import pyperclip as clip

# Custom file path override, usually just leave it blank if you use pyperclip
source_dir = ""

# Get the image location directly from the clipboard
if source_dir == "":
    source_dir = clip.paste()
    
# This will convert all the JPG in source_dir to HEI.
# source_format = 0 -> JPG. (You don't need to change this for most of the time, you can also set to 1 for PNG.)
# target_format = 0 -> AVIF (For smaller file size but less compatible, requires iOS 16/macOS Ventura or higher).
# target_format = 1 -> HEIF (For best compatibility but slightly larger file size, requires additional extension to open on Windows).
heiya.to_hei.convert_image_in_dir_to_hei(source_dir, source_format=0, target_format=1)
```
* Some basic operations can be found in [Heiya Basic Demo Notebook](https://github.com/wu-hongjun/heiya/blob/main/heiya_basic_demo.ipynb).
* A complete set of heiya examples can be found in the [Heiya Full Demo Notebook](https://github.com/wu-hongjun/heiya/blob/main/heiya_full_demo.ipynb).

## To-Do & Help Needed
* Attempt an implementation using `imagemagick` to enable bitrate higher than the current 8 bit.

## What does the name mean?

* HEI - High Efficiency Image.
* Ya - In Chinese, 压(yā) means "to compress".

But mostly just a reference to uncle Roger's "Heiya" when he saw the BBC host rinse and drain cooked rice with tap water (smh... here's the [video](https://youtu.be/53me-ICi_f8)).

## Update History

A complete update log can be found in the [HISTORY.md](https://github.com/wu-hongjun/heiya/blob/main/HISTORY.md).

## License
Heiya is distributed with the license in [LICENSE.txt](https://github.com/wu-hongjun/heiya/blob/main/LICENSE.txt).
