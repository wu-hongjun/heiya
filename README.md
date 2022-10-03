# Heiya

> **A one-line solution for photographers to simply convert JPEG into HEIC/AVIF and preserve all the metadata.**

## Introduction
Heiya allows you to easily translate between JPG/TIFF and HEIC/AVIF, without losing image metadata such as geotag and lens information. All the common operations can be done using one line of code.

It is developed for photographers with a storage budget (like myself, lol) to build an automatic and efficient image storage pipeline.

***

JPEG was invented six years before my existence.

And yet, the majority of cameras in the current age still shoot JPEG.

HEIC and AVIF are what are called "High-Efficiency Images" (You can read about them here: [AVIF vs HEIC](https://www.winxdvd.com/ios-android-mobile/avif-vs-heic.htm)). 
* These are the future of media formats, JPEG is getting deprecated.
* They can result in a file size of as much as 100x less than traditional JPEGs.
* Devices and operating systems now have good support for both formats.
* However, there are no free and easy-to-use tools out there to simply encode all the JPEGs my camera took into AVIFs while preserving metadata.

## Install Heiya from PyPI
* Heiya is developed on macOS and hasn't been tested on Windows or other OS such as Linux.
  
```python
pip install heiya
pip install heiya --upgrade
```

## Examples

A complete set of heiya examples can be found in the [Heiya Demo Notebook](https://github.com/wu-hongjun/heiya/blob/main/heiya_demo.ipynb).

