pyinstaller src/main.py --onefile --noconfirm --name appraiser-geo
Compress-Archive -Path dist/appraiser-geo.exe -Destination dist/appraiser-geo -Force