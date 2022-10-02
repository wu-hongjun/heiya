EXT_TIF = (".tif", ".tiff", ".TIF", ".TIFF")
EXT_AVIF = (".AVIF", ".avif", ".AV1F", ".av1f")
EXT_HIF = (".HIF", ".hif", ".HEIF", ".heif", ".HEIC", ".heic")
EXT_JPG = (".JPG", ".JPEG", ".jpeg", ".jpg")

from PIL import Image
import piexif
import pyheif
import pillow_heif
import pyperclip as clip

import os
from glob import glob
from pathlib import Path
import shutil
from os import listdir, remove
from os.path import isfile, join, dirname, basename, exists

def delete_all_ext_in_dir(source_dir, extension):
    """
    Deletes all the files with specified extension in the source directory.
    Args:
        source_dir (str): A directory that contain files.
        extension (str or tuple): The target format you want to delete.
    """
    try:
        # Make a list of all the files to delete based on extension
        tif_file_list = [file for file in listdir(source_dir) if file.endswith(extension)]
        
        # Keep track of image count for displaying progress
        image_count = len(tif_file_list)
        image_counter = 0
        
        # Delete all files in the directory that ends with that extension.
        for tif_file in tif_file_list:
            tif_file_path = os.path.join(source_dir, tif_file)
            if exists(tif_file_path):
                remove(tif_file_path)
                image_counter += 1
                progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
                log = "Deleted " + extension[0] + " " + progress + ": " + tif_file_path
                print(log)
    
    except Exception as e:
        print("Error with exception: " + str(e)) 

        
def delete_image_in_dir(source_dir, tif=False, jpg=False, hif=False, avif=False):
    """
    For batch deleting a certain file type in a directory.
    Args:
        source_dir (str): A directory that contain files.
        tif (boolean): Delete all TIF files in the given directory.
        jpg (boolean): Delete all JPG files in the given directory.
        hif (boolean): Delete all HIF (HEIC) files in the given directory.
        avif (boolean): Delete all AVIF files in the given directory.
    """
    if tif: delete_all_ext_in_dir(source_dir, extension=EXT_TIF)
        
    if jpg: delete_all_ext_in_dir(source_dir, extension=EXT_JPG)
        
    if hif: delete_all_ext_in_dir(source_dir, extension=EXT_HIF)
        
    if avif: delete_all_ext_in_dir(source_dir, extension=EXT_AVIF) 

        
def find_sub_dirs(path, depth=2):
    """
    Find all the folders of the source folder with a given depth.
    Reference: https://stackoverflow.com/a/69123246
    """
    path = Path(path)
    assert path.exists(), f'Path: {path} does not exist'
    depth_search = '*/' * depth
    search_pattern = os.path.join(path, depth_search)
    return list(glob(f'{search_pattern}'))