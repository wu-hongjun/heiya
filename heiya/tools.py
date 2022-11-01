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

        
def delete_image_in_dir(source_dir, tif=False, jpg=False, heif=False, avif=False, fpn=False):
    """
    For batch deleting a certain file type in a directory.
    Args:
        source_dir (str): A directory that contain files.
        tif (boolean): Delete all TIF files in the given directory.
        jpg (boolean): Delete all JPG files in the given directory.
        heif (boolean): Delete all HEIF (HEIC) files in the given directory.
        avif (boolean): Delete all AVIF files in the given directory.
    """
    # Delete all TIFF files
    if tif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_TIF)
    
    # Delete all JPEG files
    if jpg: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_JPG)
    
    # Delete all HEIC files
    if heif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_HEIF)
    
    # Delete all AVIF files
    if avif: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_AVIF)

    # Delete all FP2, FP3 files
    if fpn: delete_all_ext_in_dir(source_dir, extension=extensions.EXT_FPN)

        
def find_sub_dirs(path, depth=0):
    """
    Find all the folders of the source folder with a given depth.
    Reference: https://stackoverflow.com/a/69123246
    """
    path = Path(path)
    assert path.exists(), f'Path: {path} does not exist'
    depth_search = '*/' * depth
    search_pattern = os.path.join(path, depth_search)
    return list(glob(f'{search_pattern}'))


def delete_all_psd_by_depth(source_dir, depth=0):
    """
    Automatically delete all psd files for a given depth.
    Args:
        source_dir (str): A directory that contain image files.
        depth (int): The layer of sub directory to run the program in.
    """
    sub_dirs = find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_PSD)
        except Exception as e:
            print("Error:", e)


def delete_all_but_psd_by_depth(source_dir, depth=0):
    """
    Automatically delete all the content extensions except psd for a given depth.
    Args:
        source_dir (str): A directory that contain image files.
        depth (int): The layer of sub directory to run the program in.
    """
    sub_dirs = find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_JPG)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_PNG)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_WEBP)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_TIF)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_AVIF)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_HEIF)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_H264)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_H265)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_RAW)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_COMPRESSED)
        except Exception as e:
            print("Error:", e)

def delete_all_img_by_depth(source_dir, depth=0):
    """
    Automatically delete all JPG/PNG/TIF for a given depth.
    Args:
        source_dir (str): A directory that contain image files.
        depth (int): The layer of sub directory to run the program in.
    """
    sub_dirs = find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_JPG)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_PNG)
            delete_all_ext_in_dir(sub_dir, extension=extensions.EXT_TIF)
        except Exception as e:
            print("Error:", e)