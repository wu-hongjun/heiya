import heiya.to_hei as to_hei
import heiya.from_hei as from_hei
import heiya.extensions as extensions
import heiya.tools as tools

import os
import shutil
from os.path import dirname, basename

def preserve_original(source_img, backup_folder_name="original"):
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
    elif extension in extensions.EXT_HIF:
        target_format = extensions.EXT_HIF
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
        

def convert_img_to_he_img(source_image, target_format=".JPG", use_hif=False, use_avif=False, preserve_original_img=True, backup_folder_name="original"):
    if preserve_original_img:
        preserve_original(source_image, backup_folder_name=backup_folder_name)

    if use_hif:
        new_hei = to_hei.convert_image_to_hei(source_image, target_format=".HIF")
        
    elif use_avif:
        new_hei = to_hei.convert_image_to_hei(source_image, target_format=".AVIF")
    
    new_img = from_hei.convert_hei_to_image(new_hei, target_format=target_format, fix_rotation=True)
    os.remove(new_hei)

    return new_img

def convert_img_in_dir_to_he_img(source_dir, target_format=".JPG", use_hif=False, use_avif=False, preserve_original_img=True, backup_folder_name="original"):
    """
    Convert JPG to JPG using high efficiency codec.
    Args:
        source_dir (str): A directory that contain jpg files.
        use_codec (int): 0 will use HIF. 1 will use AVIF.
    """
    if not use_hif and not use_avif:
        raise ValueError("No codec is selected, please use a codec to proceed.")
    elif use_hif and use_avif:
        raise ValueError("Cannot encode using both codec, please use one codec to proceed.")
    
    source_list = []
    
    if target_format in extensions.EXT_TIF:
        source_list.extend(list(extensions.EXT_TIF))

    if target_format in extensions.EXT_JPG:
        source_list.extend(list(extensions.EXT_JPG))
        
    source_format = tuple(source_list)

    # Filter out hidden cache files starts with "._" created by Capture One
    source_file_list = [file for file in os.listdir(source_dir) if file.endswith(source_format) and not file.startswith("._")] 

    for source_file in source_file_list:
        source_file_path = os.path.join(source_dir, source_file)
        convert_img_to_he_img(source_file_path, target_format=target_format, 
                                use_hif=use_hif, use_avif=use_avif, 
                                preserve_original_img=preserve_original_img, 
                                backup_folder_name=backup_folder_name)

    