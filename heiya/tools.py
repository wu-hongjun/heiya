import heiya.extensions as extensions  # heiya library for extensions of a certain file type

import os
from glob import glob
from pathlib import Path
from os import listdir, remove
from os.path import exists

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

        
def delete_image_in_dir(source_dir, tif=False, jpg=False, hif=False, avif=False, fpn=False):
    """
    For batch deleting a certain file type in a directory.
    Args:
        source_dir (str): A directory that contain files.
        tif (boolean): Delete all TIF files in the given directory.
        jpg (boolean): Delete all JPG files in the given directory.
        hif (boolean): Delete all HIF (HEIC) files in the given directory.
        avif (boolean): Delete all AVIF files in the given directory.
    """
    # Delete all TIFF files
    if tif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_TIF)
    
    # Delete all JPEG files
    if jpg: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_JPG)
    
    # Delete all HEIC files
    if hif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_HIF)
    
    # Delete all AVIF files
    if avif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_AVIF)

    # Delete all FP2, FP3 files
    if fpn: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_FPN)

        
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
