EXT_TIF = (".tif", ".tiff", ".TIF", ".TIFF")
EXT_AVIF = (".AVIF", ".avif", ".AV1F", ".av1f")
EXT_HIF = (".HIF", ".hif", ".HEIF", ".heif", ".HEIC", ".heic")
EXT_JPG = (".JPG", ".JPEG", ".jpeg", ".jpg")


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

import heiya.to_hei
import heiya.from_hei

def preserve_original(source_dir, extension=".JPG", backup_folder_name="original"):
    """
    Take all the items with specified extension and back them up in ./original folder.
    Args:
        source_dir (str): A directory that contain files.
        extension (str): Extension of files you desire to back up of.
        backup_folder_name (str): The name of the back up folder, by default "original".
    """
    if extension in EXT_JPG:
        target_format = EXT_JPG
    elif extension in EXT_TIF:
        target_format = EXT_TIF
    elif extension in EXT_HIF:
        target_format = EXT_HIF
    elif extension in EXT_AVIF:
        target_format = EXT_AVIF
        
    original_file_list = [file for file in listdir(source_dir) if file.endswith(target_format) and not file.startswith("._")]
    
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
        

def convert_jpg_to_he_jpg(source_dir, use_hif=False, use_avif=False, preserve_original_jpg=True):
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
    
    if preserve_original_jpg:
        preserve_original(source_dir, extension=".JPG")
        
    if use_hif:
        convert_image_in_dir(source_dir, source_jpg=True, target_hif=True)
        convert_hei_in_dir_to_jpg(source_dir, hif=True,fix_rotation=True)
        delete_image_in_dir(source_dir, hif=True)
    elif use_avif:
        convert_image_in_dir(source_dir, source_jpg=True, target_avif=True)
        convert_hei_in_dir_to_jpg(source_dir, avif=True,fix_rotation=True)
        delete_image_in_dir(source_dir, avif=True)