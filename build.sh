#!/bin/sh

# This script automates the package and publish process to PyPI.
# For developer use only, you should not attempt to build your own package.

# Go to the repository location
cd /Users/hongjunwu/Documents/GitHub/heiya

# Build package
python3 setup.py sdist bdist_wheel

# Push package to PyPi
python3 -m twine upload dist/*

# Workspace cleanup
rm -r ./dist
