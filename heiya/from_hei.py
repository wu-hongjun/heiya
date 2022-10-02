# High Efficiency Image (AVIF/HIF) to JPG Converter 

from PIL import Image
import piexif
import pyheif

import heiya.extensions as extensions

import os
from os import listdir
from os.path import dirname, basename

def convert_hei_to_image(source_hei, target_format=".JPG", fix_rotation=True):
    """
    Convert a HEI (High Efficiency Image) file (.AVIF or .HIF) into .JPG
    
    Args:
        source_tif (str): A full file path of a .HIF image.
        target_format (str): The target format you want to convert to, by default use ".JPG"
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    Returns:
        (str) Full file path of the generated file.
    """
    
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_hei)
    file_name  = basename(source_hei).split(".")[0] 
    extension = basename(source_hei).split(".")[1]
    
    # Read HEI file
    # Note: pillow_heif can handle both heif and avif
    hei_file = pyheif.read(source_hei)  
    
    # Construct Image object
    # Creation of image 
    image = Image.frombytes(
        hei_file.mode,
        hei_file.size,
        hei_file.data,
        "raw",
        hei_file.mode,
        hei_file.stride,
    )
    
    # Retrive the metadata
    # Reference: https://stackoverflow.com/a/65054622
    for metadata in hei_file.metadata or []:
        if metadata['type'] == 'Exif':
            exif_dict = piexif.load(metadata['data'])

    # PIL rotates the image according to exif info, so it's necessary to remove the orientation tag otherwise the image will be rotated again (1° time from PIL, 2° from viewer).
    if fix_rotation:
        exif_dict['0th'][274] = 1
        
    meta = piexif.dump(exif_dict)
    
    # Construct output file name
    output_file = directory + "/" + file_name + target_format

    # Save new image
    if meta:
        image.save(output_file, exif=meta)
    else:
        image.save(output_file)
    
    return output_file
    
    
def convert_hei_in_dir_to_image(source_dir, source_format=".AVIF", target_format=".JPG", fix_rotation=True):
    """
    Convert all the files with an extension of ".tif" into target format.
    Args:
        source_dir (str): A directory that contain tif files.
        source_format (str): The type of files to convert from. 
                            This will convert all related files (i.e. ".HIF" will convert all .HIF .HEIC .HEIF)
                            Not very elegant, to be improved in the future.
        target_format (str or tuple): The target format you want to convert to, by default use ".AVIF"
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    """
    try:
        # Get all HIF files
        if source_format in extensions.EXT_AVIF:
            hei_format = extensions.EXT_AVIF
        elif source_format in extensions.EXT_HIF:
            hei_format = extensions.EXT_HIF
        else:
            raise ValueError("Not a valid source format.")
            
        hei_file_list = [file for file in listdir(source_dir) if file.endswith(hei_format) and not file.startswith("._")]  

        # Keep track of image count for displaying progress
        image_count = len(hei_file_list)
        image_counter = 0

        # Manipulate each tif image
        for hei_file in hei_file_list:
            hei_file_path = os.path.join(source_dir, hei_file)
            output_file = convert_hei_to_image(hei_file_path, target_format, fix_rotation=fix_rotation)

            image_counter += 1
            progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
            log = source_format + " -> " + target_format + " " + progress + ": " + output_file
            print(log)
    
    except Exception as e:
        print("Error with exception: " + str(e)) 
        
        
def convert_hei_in_dir_to_jpg(source_dir, source_hif=False, source_avif=False, fix_rotation=True):
    """
    Call method from the user to specify which file format in a directory to convert to JPG.
    Args:
        source_dir (str): A directory that contain tif files.
        source_hif (boolean): If true, convert all the HIF formats inside the directory into JPG
        source_avif (boolean): If true, convert all the AVIF formats inside the directory into JPG
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    """
    if source_hif:
        convert_hei_in_dir_to_image(source_dir, source_format=".HIF", target_format=".JPG", fix_rotation=fix_rotation)
    if source_avif:
        convert_hei_in_dir_to_image(source_dir, source_format=".AVIF", target_format=".JPG", fix_rotation=fix_rotation)
