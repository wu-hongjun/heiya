import heiya.to_hei as to_hei
import heiya.from_hei as from_hei
import heiya.extensions as extensions
import heiya.tools as tools

from PIL import Image

import os
import shutil
from os.path import dirname, basename

def preserve_original(source_img, backup_folder_name="original"):
    """
    Save a copy of the input source_img into a folder in the same directory with the name backup_folder_name.
    Args:
        source_img (str): The path of an image to make backup of (can be other files too).
        backup_folder_name (str): The name of the folder to put the replicated file in.
    """
    # Separate a full file path into directory, file name, and extension
    directory = dirname(source_img)
    full_file_name = basename(source_img)

    backup_dir_path = os.path.join(directory, backup_folder_name)
    if not os.path.exists(backup_dir_path):
        os.makedirs(backup_dir_path)

    backup_file_path = os.path.join(backup_dir_path, full_file_name)
    output_file = shutil.copy(source_img, backup_file_path)

    return output_file


def preserve_all_original_in_dir(source_dir, extension=".JPG", backup_folder_name="original"):
    """
    Take all the items with specified extension and back them up in ./original folder.
    Args:
        source_dir (str): A directory that contain files.
        extension (str): Extension of files you desire to back up of.
        backup_folder_name (str): The name of the back up folder, by default "original".
    """
    if extension in extensions.EXT_JPG:
        target_format = extensions.EXT_JPG
    elif extension in extensions.EXT_TIF:
        target_format = extensions.EXT_TIF
    elif extension in extensions.EXT_HEIF:
        target_format = extensions.EXT_HEIF
    elif extension in extensions.EXT_AVIF:
        target_format = extensions.EXT_AVIF
        
    original_file_list = [file for file in os.listdir(source_dir) if file.endswith(target_format) and not file.startswith("._")]
    
    backup_dir_path = os.path.join(source_dir, backup_folder_name)
    if not os.path.exists(backup_dir_path):
        os.makedirs(backup_dir_path)
    
    # Keep track of image count for displaying progress
    image_count = len(original_file_list)
    image_counter = 0
    
    for original_file in original_file_list:
        original_path = os.path.join(source_dir, original_file)
        backup_path = os.path.join(source_dir, backup_folder_name, original_file)
        output_file = shutil.copy(original_path, backup_path)
        image_counter += 1
        progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
        log = "Backup " + progress + ": " + output_file
        
        print(log)
        

def convert_img_to_he_img(source_image, target_format=".JPG", use_heif=False, use_avif=False, preserve_original_img=True, backup_folder_name="original"):
    """
    (Deprecated)
    Convert one image to High Efficiency Image.
    That is, take an image (probably a JPG), encode it using one of the HEI codec, and encode it back to JPG.
    Args:
        source_image (str): The location of the input image.
        target_format (str): The target format you desire to convert the input to.
        use_heif (boolean): Use the HEIC codec to encode the image.
        use_avif (boolean): Use the AV1 codec to encode the image.
        preserve_original_img (boolean): Whether to save a backup of the original image in case it gets overwritten.
    """
    if preserve_original_img:
        preserve_original(source_image, backup_folder_name=backup_folder_name)
     
    if use_avif:
        new_hei = to_hei.convert_image_to_hei(source_image, target_format=0)

    elif use_heif:
        new_hei = to_hei.convert_image_to_hei(source_image, target_format=1)
    
    new_img = from_hei.convert_hei_to_image(new_hei, target_format=target_format, fix_rotation=True)
    os.remove(new_hei)

    return new_img

def convert_img_in_dir_to_he_img(source_dir, target_format=".JPG", use_heif=False, use_avif=False, preserve_original_img=True, backup_folder_name="original"):
    """
    (Deprecated)
    Convert JPG to JPG using high efficiency codec.
    Args:
        source_dir (str): A directory that contain jpg files.
        target_format (str): The target format you desire to convert the input to.
        use_heif (boolean): Use the HEIC codec to encode the image.
        use_avif (boolean): Use the AV1 codec to encode the image.
        preserve_original_img (boolean): Whether to save a backup of the original image in case it gets overwritten.
    """
    if not use_heif and not use_avif:
        raise ValueError("No codec is selected, please use a codec to proceed.")
    elif use_heif and use_avif:
        raise ValueError("Cannot encode using both codec, please use one codec to proceed.")
    
    source_list = []
    
    if target_format in extensions.EXT_TIF:
        source_list.extend(list(extensions.EXT_TIF))

    if target_format in extensions.EXT_JPG:
        source_list.extend(list(extensions.EXT_JPG))
        
    source_format = tuple(source_list)

    # Filter out hidden cache files starts with "._" created by Capture One
    source_file_list = [file for file in os.listdir(source_dir) if file.endswith(source_format) and not file.startswith("._")] 

    # Keep track of image count for displaying progress
    image_count = len(source_file_list)
    image_counter = 0

    for source_file in source_file_list:
        source_file_path = os.path.join(source_dir, source_file)
        output_file = convert_img_to_he_img(source_file_path, target_format=target_format, 
                                use_heif=use_heif, use_avif=use_avif, 
                                preserve_original_img=preserve_original_img, 
                                backup_folder_name=backup_folder_name)
        image_counter += 1
        progress = str(image_counter) + "/" + str(image_count) + "(" + str(int((image_counter / image_count)*100)) + "%)"
        log = "Encoding " + target_format + " using" + str(" HEIF " if use_heif else " AVIF ") + progress + ": " + output_file
        print(log)


def normal_img_convertion(source_image, target_format=0, preserve_original_img=True):
    """
    Simple function to convert normal images.
    Note that this currently does not maintain metadata.

    source_image (str): The location of the input image.
    target_format (int): The target format you desire to convert the input to. 0, 1, 2, 3 = JPG, TIF, PNG, WEBP
    preserve_original_img (boolean): If False, delete the source image.
    """
    # Separate a full file path into directory, file name, and extension.
    directory = dirname(source_image)
    file_name  = basename(source_image).split(".")[0] 
    extension = basename(source_image).split(".")[1]

    # Check input type is valid for this function.
    valid_ext_list = [extensions.EXT_JPG, extensions.EXT_PNG, extensions.EXT_JPG]
    is_valid = False
    for valid_ext in valid_ext_list:
        if extension in valid_ext:
            is_valid=True
    if not is_valid:
        raise ValueError(extension + " is not a supported input type.")
    
    if target_format == 0:
        target_ext = ".JPG"
    elif target_format == 1:
        target_ext = ".TIF"  # Untested
    elif target_format == 2:
        target_ext = ".PNG"
    elif target_format == 3:
        target_ext = ".WEBP"

    # Use PIL to convert image
    im = Image.open(source_image).convert("RGB")
    output_file = directory + "/" + file_name + target_ext
    im.save(output_file, target_ext.replace(".", ""))

    # Delete source image (Might not be a good idea but adding a feature doesn't hurt)
    if not preserve_original_img:
        os.remove(source_image)