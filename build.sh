#!/bin/sh

# Go to repository
cd /Users/hongjunwu/Documents/GitHub/heiya

# Build package
python3 setup.py sdist bdist_wheel

# Push package to PyPi
python3 -m twine upload dist/*

# Workspace cleanup
rm -r ./dist