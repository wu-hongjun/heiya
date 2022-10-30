# Heiya

> **A one-line solution for photographers to simply convert JPEG into High Efficiency Image (AVIF/HEIC) and preserve all the metadata.**

## Introduction
Heiya allows you to easily translate between JPG/TIFF and AVIF/HEIC, without losing image metadata such as geotag and lens information. All the common operations can be done using one line of code.

It is developed for photographers with a storage budget (like myself, lol) to build an automatic and efficient image storage pipeline.

***

JPEG was invented six years before my existence.
I'm now 24, graduating from my double Master's degree next summer.

And yet, the majority of cameras in the current age still shoot JPEG.

AVIF and HEIC are what are called "High-Efficiency Images" (You can read about them here: [AVIF vs HEIC](https://www.winxdvd.com/ios-android-mobile/avif-vs-heic.htm)). 
* These are the future of media formats, JPEG is getting deprecated.
* They can result in a file size of as much as 100x less than traditional JPEGs.
* Devices and operating systems now have good support for both formats.
* However, there are no free and easy-to-use tools out there to simply encode all the JPEGs my camera took into AVIFs while preserving metadata.

## Install Heiya from PyPI
Heiya is developed and tested on macOS and hasn't been tested on Linux, it doesn't support Windows for now.
  
```python
pip install heiya
```

## Examples
* If you just want to convert your JPG to AVIF/HEIF, check out the [Heiya Basic Demo Notebook](https://github.com/wu-hongjun/heiya/blob/main/heiya_basic_demo.ipynb).
* A complete set of heiya examples can be found in the [Heiya Full Demo Notebook](https://github.com/wu-hongjun/heiya/blob/main/heiya_full_demo.ipynb).

## To-Do & Help Needed
* Seek alternative for `pyheif` (Which is why Heiya does not support Windows).
* Attempt an implementation using `imagemagick` to enable bitrate higher than the current 8 bit.

## What does the name mean?

* HEI - High Efficiency Image.
* Ya - In Chinese, 压(yā) means "to compress".

But mostly just a reference to uncle Roger's "Heiya" when he saw the BBC host rinse and drain cooked rice with tap water (smh... here's the [video](https://youtu.be/53me-ICi_f8)).

## Update History

A complete update log can be found in the [HISTORY.md](https://github.com/wu-hongjun/heiya/blob/main/HISTORY.md).

## License
Heiya is distributed with the license in [LICENSE.txt](https://github.com/wu-hongjun/heiya/blob/main/LICENSE.txt).
