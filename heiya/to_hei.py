EXT_TIF = (".tif", ".tiff", ".TIF", ".TIFF")
EXT_AVIF = (".AVIF", ".avif", ".AV1F", ".av1f")
EXT_HIF = (".HIF", ".hif", ".HEIF", ".heif", ".HEIC", ".heic")
EXT_JPG = (".JPG", ".JPEG", ".jpeg", ".jpg")

"""
Tool 1 Image to High Efficiency Image (AVIF/HIF) Converter Functions
"""

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


def convert_image_to_hei(source_image, target_format=".AVIF"):
    """
    Convert a TIF file into a AVIF file.
    This conversion preserves all the image metadata.
    
    Args:
        source_tif (str): A full file path of a .TIF image.
        target_format (str): The target format you want to convert to, by default use ".HIF"
        
    Returns:
        (str) Full file path of the generated file.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_image)
    file_name  = basename(source_image).split(".")[0] 
    extension = basename(source_image).split(".")[1]

    # Register the pillow HEI opener
    if target_format in EXT_HIF:
        pillow_heif.register_heif_opener()
    elif target_format in EXT_AVIF:
        pillow_heif.register_avif_opener()
    else:
        raise ValueError("Not a valid target format. Please use .HIF or .AVIF.")

    # Open the image using PIL
    img = Image.open(source_image)

    # Load meta data from tif
    meta_dict = piexif.load(source_image)

    # Convert meta data into bytes so we can pass it into img.save()
    meta = piexif.dump(meta_dict)

    # Construct output file name
    output_file = directory + "/" + file_name + target_format

    # Export file using the meta data information
    img.save(output_file, exif=meta)
    
    return output_file
 
    
def convert_image_in_dir(source_dir, source_tif=False, source_jpg=True, target_hif=False, target_avif=False):
    """
    Convert all the files with an extension of ".tif" into target format.
    Args:
        source_dir (str): A directory that contain tif files.
        target_format (str or tuple): The target format you want to convert to, by default use ".HIF"
    """
    try:
        # Filter out hidden cache files starts with "._" created by Capture One
        source_list = []
        
        if source_tif:
            source_list.extend(list(EXT_TIF))

        if source_jpg:
            source_list.extend(list(EXT_JPG))
            
        source_format = tuple(source_list)

        source_file_list = [file for file in listdir(source_dir) if file.endswith(source_format) and not file.startswith("._")]  

        # Keep track of image count for displaying progress
        image_count = len(source_file_list)
        image_counter = 0

        # Manipulate each tif image
        for source_file in source_file_list:
            source_file_path = os.path.join(source_dir, source_file)
            
            image_counter += 1
            progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
            
            if target_hif:
                output_file = convert_image_to_hei(source_file_path, ".HIF")
                if source_tif:
                    log = "TIF -> HIF " + progress + ": " + output_file
                if source_jpg:
                    log = "JPG -> HIF " + progress + ": " + output_file
            if target_avif:
                output_file = convert_image_to_hei(source_file_path, ".AVIF")
                if source_tif:
                    log = "TIF -> AVIF " + progress + ": " + output_file
                if source_jpg:
                    log = "JPG -> AVIF " + progress + ": " + output_file
                
            print(log)
    
    except Exception as e:
        print("Error with exception: " + str(e))  



    
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


def convert_all_sub_folders_to_hei(source_dir, source_tif=False, source_jpg=False, 
                            target_hif=False, target_avif=False, depth=2):
    """
    Automatically run the conversion script for a given depth.
    """
    sub_dirs = find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            convert_image_in_dir(source_dir, source_tif=source_tif, source_jpg=source_jpg, 
                                 target_hif=target_hif, target_avif=target_avif)
        except Exception as e:
            print("Error:", e)