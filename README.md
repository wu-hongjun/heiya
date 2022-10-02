# Heiya

**A one line solution for photographers who are looking to replace their JPEGs with High Efficiency Images(HEIs).**

Not published yet! But we are very close :)))

# Introduction
High Efficiency Image (HEI) - Ya! 

Get it?

It is unbelieveable that JPEG is from... last century.
And the majority of cameras in the current age shoot JPG.
Some can encode using HEIC (iPhone, Fujifilm X-H2S, ...), but that codec is inside a paywall.
Most cameras do not support AVIF, but it is the future for image codec and many operating system already support AV1 (and therefore AVIF).

HEIC and AVIF are what is called "High Efficiency Images", and can result in file size 10x less than traditional JPEGs.
However, there is no easy solution to simply convert JPEG/TIFF to HEIC/AVIF and preserve all the metadata.

Heiya is an open source wrapper for easy High Efficiency Image (AVIF/HEIC) to and from JPG conversion.
It is developed for photographers to build a more automatic and space saving pipeline.

# Install Heiya
### Install from PIP
```python
pip install heiya  # Not avaliable yet
```

### System Requirements
Due to some of the current dependencies of Heiya only runs on macOS, some features might not be available in Windows.
Heiya is developed on macOS and isn't tested on Linux or other OS.

# Examples

### Getting Started
```python
import heiya
```

### Define Source Directory
```python
# Option 1: Define it by yourself
source_dir = ""

# Option 2: Get the directory directly from the clipboard
import pyperclip as clip

if source_dir == "":
    source_dir = clip.paste()
```

### Batch JPG/TIF -> HEI in directory

```python
heiya.to_hei.convert_image_in_dir(source_dir, source_tif=False, source_jpg=True, 
                                  target_hif=False, target_avif=True)
```

### Batch IMG -> HEI in directory using depth
```
Example: 
    /Photos/2022/01/20220105/img1.jpg, ...
    Then with source_dir = "/Photos":
        depth = 0 -> "/Photos"
        depth = 1 -> "/Photos/2022"
        depth = 2 -> "/Photos/2022/01"
        depth = 3 -> "/Photos/2022/01/20220105"
```

```python
heiya.to_hei.convert_all_sub_folders_to_hei(source_dir, source_tif=False, source_jpg=False, 
                                            target_hif=False, target_avif=False, depth=2)
```

### Batch HEI -> JPG in directory

```python
heiya.from_hei.convert_hei_in_dir_to_jpg(source_dir, source_hif=False, 
                                         source_avif=False, fix_rotation=True)
```

### Batch JPG -> HEI -> JPG in directory
```python
heiya.tools.convert_jpg_to_he_jpg(source_dir, use_hif=False, 
                                  use_avif=True, preserve_original_jpg=True)
```

### Delete files with a specific extension in directory
```python
heiya.tools.delete_image_in_dir(source_dir, tif=False, jpg=False, hif=False, avif=False)
```
