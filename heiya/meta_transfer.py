
from PIL import Image
import piexif

from os.path import dirname, basename, join

def img_meta_transfer(source_image, target_image, replace_original=False, postpend="_tagged", lens_model=""):
    """
    Used to tag EXIF information onto a scanned JPG (Digitalizing film photographs).
    Only works for JPG and TIFFs (Due to dependent on piexif)

    Takes a source image and transplant the date and gps information to a target image.
    """
    # Extract EXIF information from the source image.
    exif_dict = piexif.load(source_image)

    # Construct useful information to be transplanted.
    new_exif_ifd = {piexif.ExifIFD.DateTimeOriginal: exif_dict["Exif"][36867],
    piexif.ExifIFD.LensModel: lens_model}
    new_gps_ifd = exif_dict["GPS"]

    # Separate target path into directory, file name, and extension.
    directory = dirname(target_image)
    file_name  = basename(target_image).split(".")[0] 
    extension = basename(target_image).split(".")[1]

    # Construct output image.
    new_exif_dict = {"Exif":new_exif_ifd, "GPS":new_gps_ifd}
    new_exif_bytes = piexif.dump(new_exif_dict)

    # Save output image.
    img = Image.open(target_image)
    if replace_original:
        img.save(target_image, exif=new_exif_bytes)
    else:
        new_path = join(directory, file_name + postpend + "." + extension)
        img.save(new_path, exif=new_exif_bytes)


def batch_img_meta_transfer(source_image, target_image, replace_original=False, postpend="_tagged", lens_model=""):
    """
    Enables feeding in a list of target images in order to batch convert images in the same location.
    """
    if type(target_image) == "str":
        img_meta_transfer(source_image, target_image, replace_original, postpend, lens_model)
    elif isinstance(target_image, list):
        for image in target_image:
            img_meta_transfer(source_image, image, replace_original, postpend, lens_model)
    else:
        raise ValueError("Unknown type target image.")