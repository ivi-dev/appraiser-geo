pyinstaller src/main.py --onedir --noconfirm --name appraiser-geo
Compress-Archive -Path dist/appraiser-geo -Destination dist/appraiser-geo -Force