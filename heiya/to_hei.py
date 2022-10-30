# Image to High Efficiency Image (AVIF/HEIF) Converter 

from PIL import Image
import piexif
import pillow_heif

import heiya.extensions as extensions
import heiya.tools as tools

import os
from os import listdir
from os.path import dirname, basename


def convert_image_to_hei(source_image, target_format=0):
    """
    Convert a TIF file into a AVIF file.
    This conversion preserves all the image metadata.
    
    Args:
        source_image (str): A full file path of an image.
        target_format (int): The target format you want to convert to. 0 = AVIF, 1 = HEIF
        
    Returns:
        (str) Full file path of the generated file.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_image)
    file_name  = basename(source_image).split(".")[0] 
    extension = basename(source_image).split(".")[1]

    # Register the pillow HEI opener
    if target_format == 0:
        pillow_heif.register_avif_opener()
        output_file = directory + "/" + file_name + ".AVIF"
    elif target_format == 1:
        pillow_heif.register_heif_opener()
        output_file = directory + "/" + file_name + ".HEIF"
    else:
        raise ValueError("No codec is selected, try pass in target_format=0 as an argument.")

    # Open the image using PIL
    img = Image.open(source_image)

    # Load meta data from tif
    meta_dict = piexif.load(source_image)

    # Convert meta data into bytes so we can pass it into img.save()
    meta = piexif.dump(meta_dict)

    # Export file using the meta data information
    img.save(output_file, exif=meta)
    
    return output_file
 
    
def convert_image_in_dir_to_hei(source_dir, source_format=0, target_format=0):
    """
    Convert all the files with an extension of ".tif" or ".jpg" into target format.
    Args:
        source_dir (str): A directory that contain image files.
        source_format (int): 0 = JPG, 1 = TIF.
        target_format (int): Convert the input image to HEI. 0 = AVIF, 1 = HEIF.
    """
    try:
        # Filter out hidden cache files starts with "._" created by Capture One
            
        if source_format == 0:
            source_format_ext = extensions.EXT_JPG
        elif source_format == 1:
            source_format_ext = extensions.EXT_TIF

        source_file_list = [file for file in listdir(source_dir) if file.endswith(source_format_ext) and not file.startswith("._")]  

        # Keep track of image count for displaying progress.
        image_count = len(source_file_list)
        image_counter = 0

        # Manipulate each tif image.
        for source_file in source_file_list:
            source_file_path = os.path.join(source_dir, source_file)
            
            image_counter += 1
            progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
            
            output_file = convert_image_to_hei(source_file_path, target_format)

            # Print log.
            if source_format == 0 and target_format == 0:
                log = "JPG -> AVIF " + progress + ": " + output_file
            if source_format == 1 and target_format == 0:
                log = "TIF -> AVIF " + progress + ": " + output_file
            if source_format == 0 and target_format == 1:
                log = "JPG -> HEIF " + progress + ": " + output_file
            if source_format == 1 and target_format == 1:
                log = "TIF -> HEIF " + progress + ": " + output_file
            print(log)

    except Exception as e:
        print("Error with exception: " + str(e))  


def convert_all_sub_folders_to_hei(source_dir, source_format=0, target_format=0, depth=0):
    """
    Automatically run the conversion script for a given depth.
    Args:
        source_dir (str): A directory that contain image files.
        source_format (int): 0 = JPG, 1 = TIF.
        target_format (int): 0 = AVIF, 1 = HEIF.
        depth (int): The layer of sub directory to run the program in.
    """
    sub_dirs = tools.find_sub_dirs(source_dir, depth=depth)
    for sub_dir in sub_dirs:
        try:
            convert_image_in_dir_to_hei(sub_dir, source_format, target_format)
        except Exception as e:
            print("Error:", e)


def video_to_h265(source_video, output=None, postpend="_h265", output_extension = ".mp4", hw_acceleration=False):
    """
    Experimental feature.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_video)
    file_name  = basename(source_video).split(".")[0] 
    extension = basename(source_video).split(".")[1]

    # Register the pillow HEI opener
    if extension not in extensions.EXT_H264 and extension not in extensions.EXT_H265:
        raise ValueError("Not a valid source video format.")

    if not output:
        output = os.path.join(directory, file_name + postpend + output_extension)

    if hw_acceleration:
        encoder = "hevc_toolbox"
    else:
        encoder = "libx265"
        
    return os.system("ffmpeg -i "+ str(source_video) + " -c:v " + encoder + " -c:a copy -x265-params crf=25" + output)
