#!/bin/bash

# 1. Empty the output directory
rm -rf dist/*

# 2. Build the app
pyinstaller src/main.py --onedir --noconfirm --name appraiser-geo