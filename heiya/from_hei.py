# High Efficiency Image (AVIF/HEIF) to JPG Converter 

from PIL import Image
import piexif
import pyheif  # Deprecating

import pillow_heif

import heiya.extensions as extensions

import os
from os import listdir
from os.path import dirname, basename

def convert_hei_to_image(source_hei, target_format=0, fix_rotation=True):
    """
    Convert a HEI (High Efficiency Image) file (.AVIF or .HEIF) into .JPG
    
    Args:
        source_hei (str): A full file path of an image.
        target (int): 0=JPG 1=TIF
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
    if target_format == 0:
        output_file = directory + "/" + file_name + ".JPG"
    elif target_format == 1:
        output_file = directory + "/" + file_name + ".TIF"
    else:
        raise ValueError("Not a valid target type. For target: 0=JPG 1=TIF.")

    # Save new image
    if meta:
        image.save(output_file, exif=meta)
    else:
        image.save(output_file)
    
    return output_file


def convert_hei_to_image_new(source_hei, target_format=0, fix_rotation=True):
    """
    Convert a HEI (High Efficiency Image) file (.AVIF or .HEIF) into (JPG/TIF)
    
    Args:
        source_hei (str): A full file path of an image.
        target_format (int): The target format you want to convert to. 0 = JPG, 1 = TIF.
        fix_rotation (boolean): The conversion might mess up the rotation of the image, this can help fix the issue.
    Returns:
        (str) Full file path of the generated file.
    """
    
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_hei)
    file_name  = basename(source_hei).split(".")[0] 
    extension = basename(source_hei).split(".")[1]

    # Register the pillow HEI opener
    if extension in extensions.EXT_HEIF:
        pillow_heif.register_heif_opener()
    elif extension in extensions.EXT_AVIF:
        pillow_heif.register_avif_opener()
    else:
        raise ValueError(str(extension) + " is not a valid input format. Please use .HEIF or .AVIF.")

    
    # Read HEI file
    # Note: pillow_heif can handle both heif and avif
    image = Image.open(source_hei)  
    image.verify()
    meta = image.getexif()
    
    # Construct output file name
    if target_format == 0:
        output_file = directory + "/" + file_name + ".JPG"
    elif target_format == 1:
        output_file = directory + "/" + file_name + ".TIF"
    else:
        raise ValueError("Not a valid target type. For target: 0=JPG 1=TIF.")

    # Save new image
    if meta:
        image.save(output_file, exif=meta)
    else:
        image.save(output_file)
    
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
