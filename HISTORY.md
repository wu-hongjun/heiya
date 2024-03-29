# Change log

## [2.3.1] - 2023-02-18
- Minor improvement on video to H265 encoder, added `-movflags use_metadata_tags` to better preserve metadata in video.

## [2.3.0] - 2023-01-08
- Added auto H265 encoding capabilities. Updated example pipeline in `pipeline.ipynb`.

## [2.2.2] - 2022-12-5
- Added minor support to non dotted extensions in heiya.extensions.

## [2.2.1] - 2022-12-4
- Fixed a bug that registers incorrect HEI opener for pillow_heif.

## [2.2.0] - 2022-12-4
- Added initial experimental support for Windows.

## [2.1.0] - 2022-11-1
- Added tools for image to webp pipeline.

## [2.0.0] - 2022-10-30
- Refactored code for better expandability going forward.
- Note that this version is not compatible with the previous version, as many functions now have new arguments.

## [1.2.4] - 2022-10-15
- Fixed an issue for not being able to correctly start batch process for meta transfer.

## [1.2.3] - 2022-10-15
- Fixed an issue for not being able to detect type list.

## [1.2.2] - 2022-10-15
- Fixed a minor issue for meta transfer not being able to properly loaded to the machine.

## [1.2.1] - 2022-10-15
- Fixed a minor issue for meta transfer not being able to properly loaded to the machine. (Fix did not work)

## [1.2.0] - 2022-10-15
- Added `meta_transfer.batch_img_meta_transfer()` for batch film digitizing workflow.

## [1.1.0] - 2022-10-15
- Added `meta_transfer.img_meta_transfer()` for easier film digitizing workflow.

## [1.0.0] - 2022-10-04
- First official release, with all the code cleaned up and properly documented. 
  
## [0.1.4] - 2022-10-03
- Rewrote some of the old comments and docstring that doesn't make sense anymore.
  
## [0.1.3] - 2022-10-02
- Fixed minor bug where the log does not appear properly when transcoding multiple formats.
  
## [0.1.2] - 2022-10-02
- Renamed `he_jpg.py` to `he_img.py` for better file type support. 
- Fixed a potential issue that can delete all JPG when using the old `heiya.he_jpg`.
  
## [0.1.1] - 2022-10-02
- Wrote a more intuitive `READEME.md`, and updated `haiya_demo.ipynb` on Github.

## [0.1.0] - 2022-10-02
- Attempting to fix an issue of incorrect param call from `heiya.he_jpg.convert_jpg_to_he_jpg`.

## [0.0.9] - 2022-10-02
- Unsuccessful fix for an issue of incorrect param call from `heiya.he_jpg.convert_jpg_to_he_jpg`.

## [0.0.8] - 2022-10-02
- Standarized function names for `from_hei` and `to_hei`.

## [0.0.7] - 2022-10-02
- Fixed an issue of internal packages not being able to properly import.

## [0.0.6] - 2022-10-02
- Added extensions and tools to `__init__.py` to fix referencing issue.

## [0.0.5] - 2022-10-02
- Removed the requirement for `glob`.

## [0.0.4] - 2022-10-02
- Removed the requirement for `os`.

## [0.0.3] - 2022-10-02
- Code cleanup.

## [0.0.2] - 2022-10-02
- Initial upload.

## [0.0.1] - 2022-10-01
- Created the project.
