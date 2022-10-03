# Image to High Efficiency Image (AVIF/HIF) Converter 

from PIL import Image
import piexif
import pillow_heif

import heiya.extensions as extensions
import heiya.tools as tools

import os
from os import listdir
from os.path import dirname, basename


def convert_image_to_hei(source_image, target_format=".AVIF"):
    """
    Convert a TIF file into a AVIF file.
    This conversion preserves all the image metadata.
    
    Args:
        source_image (str): A full file path of an image.
        target_format (str): The target format you want to convert to, by default use ".AVIF"
        
    Returns:
        (str) Full file path of the generated file.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_image)
    file_name  = basename(source_image).split(".")[0] 
    extension = basename(source_image).split(".")[1]

    # Register the pillow HEI opener
    if target_format in extensions.EXT_HIF:
        pillow_heif.register_heif_opener()
    elif target_format in extensions.EXT_AVIF:
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
 
    
def convert_image_in_dir_to_hei(source_dir, source_tif=False, source_jpg=True, target_hif=False, target_avif=False):
    """
    Convert all the files with an extension of ".tif" or ".jpg" into target format.
    Args:
        source_dir (str): A directory that contain image files.
        source_tif (boolean): Use all the TIF files in the directory as input.
        source_jpg (boolean): Use all the JPG files in the directory as input.
        target_hif (boolean): Convert the input image to HIF.
        target_avif (boolean): Convert the input image to AVIF.
    """
    try:
        # Filter out hidden cache files starts with "._" created by Capture One
        source_list = []
        
        if source_tif:
            source_list.extend(list(extensions.EXT_TIF))

        if source_jpg:
            source_list.extend(list(extensions.EXT_JPG))
            
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
                print(log)

            if target_avif:
                output_file = convert_image_to_hei(source_file_path, ".AVIF")
                if source_tif:
                    log = "TIF -> AVIF " + progress + ": " + output_file
                if source_jpg:
                    log = "JPG -> AVIF " + progress + ": " + output_file
                print(log)
    
    except Exception as e:
        print("Error with exception: " + str(e))  


def convert_all_sub_folders_to_hei(source_dir, source_tif=False, source_jpg=False, 
                            target_hif=False, target_avif=False, depth=0):
    """
    Automatically run the conversion script for a given depth.
    Args:
        source_dir (str): A directory that contain image files.
        source_tif (boolean): Use all the TIF files in the directory as input.
        source_jpg (boolean): Use all the JPG files in the directory as input.
        target_hif (boolean): Convert the input image to HIF.
        target_avif (boolean): Convert the input image to AVIF.
        depth (int): The layer of sub directory to run the program in.
    """
    sub_dirs = tools.find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            convert_image_in_dir_to_hei(sub_dir, source_tif=source_tif, source_jpg=source_jpg, 
                                 target_hif=target_hif, target_avif=target_avif)
        except Exception as e:
            print("Error:", e)

