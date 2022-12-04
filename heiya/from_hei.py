# High Efficiency Image (AVIF/HEIF) to JPG Converter 

from PIL import Image

import pillow_heif

import heiya.extensions as extensions

import os
from os import listdir
from os.path import dirname, basename


def convert_hei_to_image(source_hei, target_format=0):

    """
    Convert a HEI file into jpg or png.
    This conversion preserves all the image metadata.
    
    Args:
        source_hei (str): A full file path of an image.
        target_format (int): The target format you want to convert to. 0 = JPG, 1 = PNG
        
    Returns:
        (str) Full file path of the generated file.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_hei)
    file_name  = basename(source_hei).split(".")[0] 
    extension = basename(source_hei).split(".")[-1]

    if extension in extensions.EXT_AVIF:
        pillow_heif.register_avif_opener()
    elif extension in extensions.EXT_HEIF:
        pillow_heif.register_heif_opener()
    else:
        pass

    meta = Image.open(source_hei).getexif()

    heif_file = pillow_heif.read_heif(source_hei)

    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",

    )

    # Register the pillow HEI opener
    if target_format == 0:
        output_file = directory + "/" + file_name + ".JPG"
    elif target_format == 1:
        output_file = directory + "/" + file_name + ".PNG"
    else:
        raise ValueError("No codec is selected, try pass in target_format=0 as an argument.")

    image.save(output_file, exif=meta)
    
    return output_file
    
    
def convert_hei_in_dir_to_image(source_dir, source_format=0, target_format=0, fix_rotation=True):
    """
    Convert all the HEI files into normal image (JPG/TIF).
    Args:
        source_dir (str): A directory that contain tif files.
        source_format (int): The type of files to convert from. 0 = AVIF, 1 = HEIF.
        target_format (int): The target format you want to convert to. 0 = JPG, 1 = TIF.
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    """
    try:
        # Get all HEI files
        if source_format == 0:
            hei_format = extensions.EXT_AVIF
        elif source_format == 1:
            hei_format = extensions.EXT_HEIF
        else:
            raise ValueError("Not a valid source format.")

        if target_format == 0:
            target_ext = ".jpg"
        elif target_format == 1:
            target_ext = ".tif"
        else:
            raise ValueError("Not a valid target format.")
            
        hei_file_list = [file for file in listdir(source_dir) if file.endswith(hei_format) and not file.startswith("._")]  

        # Keep track of image count for displaying progress
        image_count = len(hei_file_list)
        image_counter = 0

        # Manipulate each tif image
        for hei_file in hei_file_list:
            hei_file_path = os.path.join(source_dir, hei_file)
            output_file = convert_hei_to_image(hei_file_path, target_ext, fix_rotation=fix_rotation)

            image_counter += 1
            progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
            log = source_format + " -> " + target_ext + " " + progress + ": " + output_file
            print(log)
    
    except Exception as e:
        print("Error with exception: " + str(e)) 
        
        
def convert_hei_in_dir_to_jpg(source_dir, source_format=0, fix_rotation=True):
    """
    Call method from the user to specify which file format in a directory to convert to JPG.
    Kinda useless at this point to be honest since now the function call for convert_hei_in_dir_to_image is simple.
    Args:
        source_dir (str): A directory that contain tif files.
        source_heif (boolean): If true, convert all the HEIF formats inside the directory into JPG
        source_avif (boolean): If true, convert all the AVIF formats inside the directory into JPG
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    """
    
    convert_hei_in_dir_to_image(source_dir, source_format=source_format, target_format=0, fix_rotation=fix_rotation)
